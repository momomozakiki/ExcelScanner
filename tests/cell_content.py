from excel_scanner import ExcelScanner

from pathlib import Path

# Define paths relative to your project root
PROJECT_ROOT = Path(__file__).parent.parent  # Adjust based on your script's location
DUMMY_FILES_DIR = PROJECT_ROOT / "dummy_file"

dummy_invoice = DUMMY_FILES_DIR / "Copy of IN32097_NMB SINGAPORE LIMITED_16DEC2024.xlsx"
dummy_quotation = DUMMY_FILES_DIR / "ST-2025-03-002_SERVICE(FISCHER BELL PRIVATE LTD).xlsx"


read_excel = ExcelScanner(dummy_invoice)

cell_content = read_excel.get_cell_content(row=58, col=13, get_formula=False, row_offset=None, col_offset=None, debug=False)

print(cell_content)