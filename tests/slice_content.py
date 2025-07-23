from excel_scanner import ExcelScanner

from pathlib import Path

# Define paths relative to your project root
PROJECT_ROOT = Path(__file__).parent.parent  # Adjust based on your script's location
DUMMY_FILES_DIR = PROJECT_ROOT / "dummy_file"

dummy_invoice = DUMMY_FILES_DIR / "Copy of IN32097_NMB SINGAPORE LIMITED_16DEC2024.xlsx"
dummy_quotation = DUMMY_FILES_DIR / "ST-2025-03-002_SERVICE(FISCHER BELL PRIVATE LTD).xlsx"


read_excel = ExcelScanner(dummy_invoice)

print(read_excel.load_with_pandas())

header = read_excel.get_slice_content(start_slice_row=None, end_slice_row=17, start_slice_col=None, end_slice_col=14)
print(header)

content = read_excel.get_slice_content(start_slice_row=18, end_slice_row=57, start_slice_col=None, end_slice_col=14)
print(content)