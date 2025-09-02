
from excel_scanner import ExcelScanner

from pathlib import Path

# Define paths relative to your project root
PROJECT_ROOT = Path(__file__).parent.parent  # Adjust based on your script's location
DUMMY_FILES_DIR = PROJECT_ROOT / "dummy_file"

dummy_invoice = DUMMY_FILES_DIR / "Copy of IN32097_NMB SINGAPORE LIMITED_16DEC2024.xlsx"
dummy_quotation = DUMMY_FILES_DIR / "ST-2025-03-002_SERVICE(FISCHER BELL PRIVATE LTD).xlsx"

# dummy_info = r"C:\Users\kbsim\Desktop\dummy info.xlsx"

# read_excel = ExcelScanner(dummy_quotation)
read_excel = ExcelScanner(dummy_invoice)
read_quotation = ExcelScanner(dummy_quotation)

print(read_quotation.load_with_pandas())


keyword = 's/n'
keyword2 = 'SUB-TOTAL'
multi_keyword = 'model'

get_info = read_quotation.get_cell_info
keyword_cell = read_quotation.get_keyword_cell(multi_keyword, exact_match=False, end_col=14, end_row=None)
print(keyword_cell)

for row, col in keyword_cell:
    ## content = read_excel.get_cell_content(row=row, col=col, get_formula=False, row_offset=None, col_offset=2, debug=True)
    content = read_quotation.get_cell_content(row=row, col=col, get_formula=False, row_offset=None, col_offset=None, return_native_type=False, use_pandas=True, debug=False )
    print(content)


# content = read_excel.get_cell_content(1,5)


'''
keyword = 'B4'

get_info = read_excel.get_cell_info
get_keyword = read_excel.search_keyword(keyword)
get_keyword_fast = read_excel.search_keyword_fast(keyword)
read_excel.close()


print(get_info(1, 3, use_pandas=True))
print(get_info(1, 3))
print(get_info(1, 4))
print(get_keyword[0])
print(type(get_keyword[0]))
# print(get_keyword_fast)

'''
