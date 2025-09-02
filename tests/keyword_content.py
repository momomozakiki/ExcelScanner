from excel_scanner import ExcelScanner

from pathlib import Path

# Define paths relative to your project root
PROJECT_ROOT = Path(__file__).parent.parent  # Adjust based on your script's location
DUMMY_FILES_DIR = PROJECT_ROOT / "dummy_file"

dummy_invoice = DUMMY_FILES_DIR / "Copy of IN32097_NMB SINGAPORE LIMITED_16DEC2024.xlsx"
dummy_quotation = DUMMY_FILES_DIR / "ST-2025-03-002_SERVICE(FISCHER BELL PRIVATE LTD).xlsx"

# dummy_info = r"C:\Users\kbsim\Desktop\dummy info.xlsx"

# read_excel = ExcelScanner(dummy_quotation)
read_invoice = ExcelScanner(dummy_invoice)
read_quotation = ExcelScanner(dummy_quotation)

print(read_invoice.load_with_pandas())

keyword = 's/n'
keyword2 = 'SUB-TOTAL'
