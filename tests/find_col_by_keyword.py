from excel_scanner import ExcelScanner

from pathlib import Path

# Define paths relative to your project root
PROJECT_ROOT = Path(__file__).parent.parent  # Adjust based on your script's location
DUMMY_FILES_DIR = PROJECT_ROOT / "dummy_file"

dummy_invoice = DUMMY_FILES_DIR / "Copy of IN32097_NMB SINGAPORE LIMITED_16DEC2024.xlsx"
dummy_quotation = DUMMY_FILES_DIR / "ST-2025-03-002_SERVICE(FISCHER BELL PRIVATE LTD).xlsx"


read_excel = ExcelScanner(dummy_invoice)
read_quotation = ExcelScanner(dummy_quotation)

print(read_excel.load_with_pandas())


first_row_keywords = {'Product Description', 'Quantity', 'Price ($)'}
# end_row_keywords = {'E. & O.E.', 'SUB-TOTAL'}
# end_row_keywords = {'E. & O.E.'}
end_row_keywords = {'SUB-TOTAL'}


inv_col_keywords = {'Price ($)'}
quo_col_keywords = {'Price ($)'}


first_row_found = read_excel.find_consensus_row(keywords=first_row_keywords, exact_match=True, end_row=None, end_col=None)
end_row_found = read_excel.find_consensus_row(keywords=end_row_keywords, exact_match=True, end_row=None, end_col=14)


print(first_row_found)
print(end_row_found)