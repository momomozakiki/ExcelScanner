from urllib.parse import uses_query

from excel_scanner import ExcelScanner

dummy_info = r"C:\Users\kbsim\Desktop\dummy info.xlsx"
dummy_invoice = r"C:\Users\ST-Service\Desktop\SIM\Excel Reader\sample file\Copy of IN32097_NMB SINGAPORE LIMITED_16DEC2024.xlsx"

read_excel = ExcelScanner(dummy_invoice)

print(read_excel.load_with_pandas())


keyword = 's/n'

get_info = read_excel.get_cell_info
keyword_cell = read_excel.get_keyword_cell_v2(keyword, exact_match=False)
print(keyword_cell)

for row, col in keyword_cell:
    content = read_excel.get_cell_content(row, col)
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
