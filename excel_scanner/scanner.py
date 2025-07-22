import pandas as pd
from openpyxl import load_workbook
from .core import normalize_text
from .exceptions import ExcelScannerError
from typing import Optional, Union, List, Tuple
from pathlib import Path


class ExcelScanner:
    """A scanner for Excel files that supports both Pandas (fast bulk operations)
    and OpenPyXL (formula/formatting access)."""

    def __init__(self, filepath: Union[str, Path]) -> None:  # <-- Accepts both str and Path
        """Initialize the Excel scanner with a file path.

        Args:
            filepath: Path to the Excel file (.xlsx, .xls).

        Attributes:
            self.df (pd.DataFrame): Loaded DataFrame (Pandas mode).
            self.wb (Workbook): OpenPyXL workbook object.
            self.ws (Worksheet): Active worksheet (OpenPyXL mode).
        """
        self.filepath = str(filepath) # type str will backward compatibility with older python path library
        self.df = None  # Private with type hint
        self.wb = None
        self.ws = None

    def load_with_pandas(self) -> pd.DataFrame:
        """Load the Excel file into a Pandas DataFrame.

        Uses header=None to treat all rows as data (no header assumption).
        Caches the DataFrame for subsequent operations.

        Returns:
            pd.DataFrame: The loaded DataFrame.

        Raises:
            ExcelScannerError: If file loading fails.

        Example:
            scanner = ExcelScanner("data.xlsx")
            df = scanner.load_with_pandas()  # Returns DataFrame
        """
        try:
            if self.df is None:
                self.df = pd.read_excel(self.filepath, header=None)
            return self.df
        except Exception as e:
            raise ExcelScannerError(f"Failed to load with pandas: {e}")

    def load_with_openpyxl(self):
        """Load the Excel file using OpenPyXL.

        Enables access to formulas and formatting. Uses data_only=True
        to get calculated values instead of formulas.

        Returns:
            Worksheet: The active worksheet.

        Raises:
            ExcelScannerError: If file loading fails.

        Example:
            ws = scanner.load_with_openpyxl()  # Returns Worksheet
        """
        self.wb = None
        try:
            self.wb = load_workbook(self.filepath, data_only=True)
            self.ws = self.wb.active
            return self.ws
        except Exception as e:
            raise ExcelScannerError(f"Failed to load with openpyxl: {e}")

    def close(self) -> None:
        """Clean up resources, particularly OpenPyXL workbook handles.

        Important to prevent file lock issues on Windows.

        Example:
            scanner.close()  # Release file handles
        """
        if hasattr(self, 'wb') and self.wb:
            self.wb.close()

    def get_cell_info(self, row: int, col: int, use_pandas: bool = True) -> Union[str, float, int]:
        """Get cell content by row and column (1-based indexing).

        Args:
            row: Row number (1-based).
            col: Column number (1-based).
            use_pandas: If True, uses Pandas (faster). If False, uses OpenPyXL.

        Returns:
            The cell value (type depends on content - str, float, int, etc.)

        Example:
            scanner.get_cell_info(1, 1)  # Returns content of A1
            "Header"
        """
        if use_pandas:
            if not hasattr(self, 'df'):
                self.load_with_pandas()
            return self.df.iloc[row - 1, col - 1]
        else:
            if not hasattr(self, 'ws'):
                self.load_with_openpyxl()
            return self.ws.cell(row=row, column=col).value

    def get_cell_content(self, row: int, col: int, get_formula: bool = False) -> str:
        """Get cell content as string, with formula handling.

        Args:
            row: Row number (1-based).
            col: Column number (1-based).
            get_formula: If True, returns formula text. If False, returns value.

        Returns:
            str: String representation of cell content.

        Example:
            scanner.get_cell_content(1, 1)  # "Value"
            scanner.get_cell_content(1, 1, get_formula=True)  # "=A2+B2"
        """
        if get_formula:
            if not hasattr(self, 'ws'):
                self.load_with_openpyxl()
            return str(self.ws.cell(row, col).value)
        else:
            if self.df is None:
                self.load_with_pandas()
            return str(self.df.iat[row - 1, col - 1]) if pd.notna(self.df.iat[row - 1, col - 1]) else ""

    def get_keyword_cell(
            self,
            keyword: str,
            exact_match: bool = True,
            end_row: Optional[int] = None,
            end_col: Optional[int] = None
    ) -> List[Tuple[int, int]]:
        """Find all cells containing the keyword (exact or partial match).

        Performs case-insensitive search after normalizing both the
        keyword and cell contents. Returns 1-based coordinates.

        Args:
            keyword: The search term to find.
            exact_match: If True, looks for exact matches only. If False,
                looks for partial matches (cell contains keyword).
            end_row: Last row to search (1-based). If None, searches all rows.
            end_col: Last column to search (1-based). If None, searches all columns.

        Returns:
            List of (row, col) tuples where keyword was found.

        Example:
            scanner.get_keyword_cell("Total", end_row=10, end_col=5)
            [(1, 3), (5, 2)]  # Found at row 1 col 3 and row 5 col 2
        """
        if self.df is None:
            self.load_with_pandas()

        # Convert 1-based to 0-based and handle None
        row_slice = slice(None, end_row) if end_row is None else slice(None, end_row - 1)
        col_slice = slice(None, end_col) if end_col is None else slice(None, end_col - 1)

        # Get the subset of dataframe to search
        search_area = self.df.iloc[row_slice, col_slice]

        norm_keyword = normalize_text(str(keyword))

        if exact_match:
            matches = search_area.map(lambda x: normalize_text(str(x)) == norm_keyword)
        else:
            matches = search_area.map(lambda x: norm_keyword in normalize_text(str(x)))

        rows, cols = matches.to_numpy().nonzero()
        return [(int(row + 1), int(col + 1)) for row, col in zip(rows, cols)]

    def find_consensus_row(
            self,
            keywords: set[str],
            exact_match: bool = True,
            end_row: Optional[int] = None,
            end_col: Optional[int] = None
    ) -> Optional[int]:
        """Find the single row where ALL keywords appear.

        Args:
            keywords: Set of keywords. For accurate results, provide 2+ keywords.
            exact_match: If True, requires exact matches.
            end_row: Limit row search range.
            end_col: Limit col search range.

        Returns:
            int: Common row number if all keywords share exactly one row.
            None: If any keyword has no matches.

        Raises:
            ValueError: With specific guidance when:
                - Single keyword matches multiple rows (suggests adding more keywords)
                - Keywords don't share any row
                - Keywords share multiple rows
        """
        if not keywords:
            return None

        # Step 1: Get all rows for each keyword
        keyword_to_rows = {}
        for keyword in keywords:
            positions = self.get_keyword_cell(keyword, exact_match, end_row, end_col)
            if not positions:
                return None
            keyword_to_rows[keyword] = {pos[0] for pos in positions}

        # Step 2: Special case - single keyword with multiple matches
        if len(keywords) == 1 and len(next(iter(keyword_to_rows.values()))) > 1:
            keyword = next(iter(keywords))
            matched_rows = keyword_to_rows[keyword]
            raise ValueError(
                f"Keyword '{keyword}' appears in multiple rows: {matched_rows}. "
                f"Please provide 1-2 additional keywords to identify the correct row.\n"
                f"Example: scanner.find_consensus_row({{{keyword!r}, 'AdditionalKeyword1', 'AdditionalKeyword2'}})"
            )

        # Step 3: Multi-keyword validation
        common_rows = set.intersection(*keyword_to_rows.values())

        if not common_rows:
            all_matches = {k: v for k, v in keyword_to_rows.items()}
            raise ValueError(
                f"No common row found. Keywords appear in different rows: {all_matches}\n"
                f"Suggestions:\n"
                f"1. Verify keyword spelling\n"
                f"2. Add more specific keywords\n"
                f"3. Adjust search range (end_row/end_col)"
            )
        elif len(common_rows) > 1:
            raise ValueError(
                f"Keywords appear in multiple shared rows: {common_rows}\n"
                f"Try narrowing the search with:\n"
                f"1. More specific keywords\n"
                f"2. Smaller end_row/end_col range"
            )

        return common_rows.pop()

    def find_consensus_col(
            self,
            keywords: set[str],
            exact_match: bool = True,
            end_row: Optional[int] = None,
            end_col: Optional[int] = None
    ) -> Optional[int]:
        """Find the single column where ALL keywords appear.

        Args:
            keywords: Set of keywords. For accurate results, provide 2+ keywords.
            exact_match: If True, requires exact matches.
            end_row: Limit row search range.
            end_col: Limit col search range.

        Returns:
            int: Common column number if all keywords share exactly one column.
            None: If any keyword has no matches.

        Raises:
            ValueError: With specific guidance when:
                - Single keyword matches multiple columns (suggests adding more keywords)
                - Keywords don't share any column
                - Keywords share multiple columns
        """
        if not keywords:
            return None

        # Step 1: Get all columns for each keyword
        keyword_to_cols = {}
        for keyword in keywords:
            positions = self.get_keyword_cell(keyword, exact_match, end_row, end_col)
            if not positions:
                return None
            keyword_to_cols[keyword] = {pos[1] for pos in positions}

        # Step 2: Special case - single keyword with multiple matches
        if len(keywords) == 1 and len(next(iter(keyword_to_cols.values()))) > 1:
            keyword = next(iter(keywords))
            matched_cols = keyword_to_cols[keyword]
            raise ValueError(
                f"Keyword '{keyword}' appears in multiple columns: {matched_cols}. "
                f"Please provide 1-2 additional keywords to identify the correct column.\n"
                f"Example: scanner.find_consensus_col({{{keyword!r}, 'AdditionalKeyword1', 'AdditionalKeyword2'}})"
            )

        # Step 3: Multi-keyword validation
        common_cols = set.intersection(*keyword_to_cols.values())

        if not common_cols:
            all_matches = {k: v for k, v in keyword_to_cols.items()}
            raise ValueError(
                f"No common column found. Keywords appear in different columns: {all_matches}\n"
                f"Suggestions:\n"
                f"1. Verify keyword spelling\n"
                f"2. Add more specific keywords\n"
                f"3. Adjust search range (end_row/end_col)"
            )
        elif len(common_cols) > 1:
            raise ValueError(
                f"Keywords appear in multiple shared columns: {common_cols}\n"
                f"Try narrowing the search with:\n"
                f"1. More specific keywords\n"
                f"2. Smaller end_row/end_col range"
            )

        return common_cols.pop()

    def get_slice_content(
            self,
            start_slice_row: Optional[int] = None,
            end_slice_row: Optional[int] = None,
            start_slice_col: Optional[int] = None,
            end_slice_col: Optional[int] = None
    ) -> pd.DataFrame:
        """Extract a slice of the Excel content as a pandas DataFrame.

        Args:
            start_slice_row: First row to include (1-based). None = start from row 1.
            end_slice_row: Last row to include (1-based). None = end at last data row.
            start_slice_col: First column to include (1-based). None = start from column 1.
            end_slice_col: Last column to include (1-based). None = end at last data column.

        Returns:
            pd.DataFrame: Sliced data preserving original pandas format.

        Example:
            # Get rows 5-10, all columns
            df = scanner.get_slice_content(start_slice_row=5, end_slice_row=10)

            # Get all rows, columns 3-5
            df = scanner.get_slice_content(start_slice_col=3, end_slice_col=5)
        """
        if self.df is None:
            self.load_with_pandas()

        # Convert 1-based to 0-based and handle None values
        start_row = 0 if start_slice_row is None else start_slice_row - 1
        end_row = len(self.df) if end_slice_row is None else end_slice_row
        start_col = 0 if start_slice_col is None else start_slice_col - 1
        end_col = len(self.df.columns) if end_slice_col is None else end_slice_col

        # Perform slicing (iloc is exclusive on end index)
        return self.df.iloc[start_row:end_row, start_col:end_col].copy()
    

''' V2
    def find_consensus_row(
            self,
            keywords: set[str],
            exact_match: bool = True,
            end_row: Optional[int] = None,
            end_col: Optional[int] = None
    ) -> Optional[int]:
        """Find the single row where ALL keywords appear (may be in different columns).

        For multiple keywords (2+), ALL must share at least one common row.

        Args:
            keywords: Set of keywords (e.g., {"Product", "Brand"}).
            exact_match: If True, requires exact matches.
            end_row/end_col: Limit search range.

        Returns:
            int: Common row number if all keywords share at least one row.
            None: If any keyword has no matches.

        Raises:
            ValueError: If keywords don't share any row or disagree.
        """
        if not keywords:
            return None

        # Step 1: Get all rows for each keyword
        keyword_to_rows = {}
        for keyword in keywords:
            positions = self.get_keyword_cell(
                keyword=keyword,
                exact_match=exact_match,
                end_row=end_row,
                end_col=end_col
            )
            if not positions:
                return None  # Early exit if any keyword is missing
            keyword_to_rows[keyword] = {pos[0] for pos in positions}

        # Step 2: Find intersection of all rows
        common_rows = set.intersection(*keyword_to_rows.values())

        if not common_rows:
            raise ValueError(
                f"No common row found. Keywords appear in different rows: "
                f"{ {k: v for k, v in keyword_to_rows.items()} }"
            )
        elif len(common_rows) > 1:
            raise ValueError(
                f"Keywords appear in multiple shared rows: {common_rows}. "
                f"Expected exactly one common row."
            )

        return common_rows.pop()

    def find_consensus_col(
            self,
            keywords: set[str],
            exact_match: bool = True,
            end_row: Optional[int] = None,
            end_col: Optional[int] = None
    ) -> Optional[int]:
        """Find the single column where ALL keywords appear (may be in different rows).

        For multiple keywords (2+), ALL must share at least one common column.

        Args:
            keywords: Set of keywords (e.g., {"Total", "Subtotal"}).
            exact_match: If True, requires exact matches.
            end_row/end_col: Limit search range.

        Returns:
            int: Common column number if all keywords share at least one column.
            None: If any keyword has no matches.

        Raises:
            ValueError: If keywords don't share any column or disagree.
        """
        if not keywords:
            return None

        # Step 1: Get all columns for each keyword
        keyword_to_cols = {}
        for keyword in keywords:
            positions = self.get_keyword_cell(
                keyword=keyword,
                exact_match=exact_match,
                end_row=end_row,
                end_col=end_col
            )
            if not positions:
                return None  # Early exit if any keyword is missing
            keyword_to_cols[keyword] = {pos[1] for pos in positions}

        # Step 2: Find intersection of all columns
        common_cols = set.intersection(*keyword_to_cols.values())

        if not common_cols:
            raise ValueError(
                f"No common column found. Keywords appear in different columns: "
                f"{ {k: v for k, v in keyword_to_cols.items()} }"
            )
        elif len(common_cols) > 1:
            raise ValueError(
                f"Keywords appear in multiple shared columns: {common_cols}. "
                f"Expected exactly one common column."
            )

        return common_cols.pop()
'''



'''
    def find_consensus_row(
            self,
            keywords: set[str],
            exact_match: bool = True,
            end_row: Optional[int] = None,
            end_col: Optional[int] = None
    ) -> Optional[int]:
        """Find the single row where ALL keywords appear (may be in different columns).

        Args:
            keywords: Set of keywords (e.g., {"Product", "Brand"}).
            exact_match: If True, requires exact matches.
            end_row/end_col: Limit search range.

        Returns:
            int: Common row number (e.g., 25) if all keywords share it.
            None: If no consensus or no matches.

        Raises:
            ValueError: If keywords appear in different rows.
        """
        if not keywords:
            return None

        # Step 1: Get all (row, col) positions for each keyword
        keyword_rows = set()
        for keyword in keywords:
            positions = self.get_keyword_cell(
                keyword=keyword,
                exact_match=exact_match,
                end_row=end_row,
                end_col=end_col
            )
            if not positions:
                return None  # At least one keyword has no matches
            keyword_rows.update({pos[0] for pos in positions})

        # Step 2: Check if all keywords share a single row
        if len(keyword_rows) == 1:
            return keyword_rows.pop()
        else:
            raise ValueError(f"Keywords disagree on rows: {keyword_rows}")


    def find_consensus_col(
            self,
            keywords: set[str],
            exact_match: bool = True,
            end_row: Optional[int] = None,
            end_col: Optional[int] = None
    ) -> Optional[int]:
        """Find the single column where ALL keywords appear (may be in different rows).

        Args:
            keywords: Set of keywords (e.g., {"Total", "Subtotal"}).
            exact_match: If True, requires exact matches.
            end_row/end_col: Limit search range.

        Returns:
            int: Common column number (e.g., 17) if all keywords share it.
            None: If no consensus or no matches.

        Raises:
            ValueError: If keywords appear in different columns.
        """
        if not keywords:
            return None

        # Step 1: Get all (row, col) positions for each keyword
        keyword_cols = set()
        for keyword in keywords:
            positions = self.get_keyword_cell(
                keyword=keyword,
                exact_match=exact_match,
                end_row=end_row,
                end_col=end_col
            )
            if not positions:
                return None  # At least one keyword has no matches
            keyword_cols.update({pos[1] for pos in positions})

        # Step 2: Check if all keywords share a single column
        if len(keyword_cols) == 1:
            return keyword_cols.pop()
        else:
            raise ValueError(f"Keywords disagree on columns: {keyword_cols}")

'''