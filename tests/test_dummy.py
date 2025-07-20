from urllib.parse import uses_query

from excel_scanner import ExcelScanner

dummy_info = r"C:\Users\kbsim\Desktop\dummy info.xlsx"

read_excel = ExcelScanner(dummy_info)

print(read_excel.load_with_pandas())


keyword = '-61'

get_info = read_excel.get_cell_info
keyword_cell = read_excel.get_keyword_cell(keyword)
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
