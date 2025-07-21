import pandas as pd
from openpyxl import load_workbook
from .core import normalize_text
from .exceptions import ExcelScannerError
from typing import Optional, Union, List, Tuple


class ExcelScanner:
    """A scanner for Excel files that supports both Pandas (fast bulk operations)
    and OpenPyXL (formula/formatting access)."""

    def __init__(self, filepath: str) -> None:
        """Initialize the Excel scanner with a file path.

        Args:
            filepath: Path to the Excel file (.xlsx, .xls).

        Attributes:
            df (pd.DataFrame): Loaded DataFrame (Pandas mode).
            wb (Workbook): OpenPyXL workbook object.
            ws (Worksheet): Active worksheet (OpenPyXL mode).
        """
        self.filepath = filepath
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

    def get_keyword_cell(self, keyword: str) -> List[Tuple[int, int]]:
        """Find all cells containing the exact normalized keyword match.

        Performs case-insensitive search after normalizing both the
        keyword and cell contents. Returns 1-based coordinates.

        Args:
            keyword: The search term to find.

        Returns:
            List of (row, col) tuples where keyword was found.

        Example:
            scanner.get_keyword_cell("Total")
            [(1, 3), (5, 2)]  # Found at row 1 col 3 and row 5 col 2
        """
        if self.df is None:
            self.load_with_pandas()

        norm_keyword = normalize_text(str(keyword))
        matches = self.df.map(lambda x: normalize_text(str(x)) == norm_keyword)
        rows, cols = matches.to_numpy().nonzero()
        return [(int(row + 1), int(col + 1)) for row, col in zip(rows, cols)]

    def get_keyword_cell_v2(self, keyword: str, exact_match: bool = True) -> List[Tuple[int, int]]:
        """Find all cells containing the keyword (exact or partial match).

        Performs case-insensitive search after normalizing both the
        keyword and cell contents. Returns 1-based coordinates.

        Args:
            keyword: The search term to find.
            exact_match: If True, looks for exact matches only. If False,
                looks for partial matches (cell contains keyword).

        Returns:
            List of (row, col) tuples where keyword was found.

        Example:
            scanner.get_keyword_cell("Total")
            [(1, 3), (5, 2)]  # Found at row 1 col 3 and row 5 col 2
        """
        if self.df is None:
            self.load_with_pandas()

        norm_keyword = normalize_text(str(keyword))

        if exact_match:
            matches = self.df.map(lambda x: normalize_text(str(x)) == norm_keyword)
        else:
            matches = self.df.map(lambda x: norm_keyword in normalize_text(str(x)))

        rows, cols = matches.to_numpy().nonzero()
        return [(int(row + 1), int(col + 1)) for row, col in zip(rows, cols)]