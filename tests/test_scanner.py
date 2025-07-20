import unittest
from excel_scanner.scanner import ExcelScanner
import os

file_path = r"C:\Users\kbsim\Desktop\scales.xlsx"

class TestExcelReader(unittest.TestCase):
    def setUp(self):
        self.filepath = file_path
        self.reader = ExcelScanner(self.filepath)

    def test_search_keyword(self):
        self.reader.load_with_pandas()
        result = self.reader.search_keyword("max_capacity")
        print(result)
        self.assertIsInstance(result, list)

    def test_get_cell(self):
        self.reader.load_with_openpyxl()
        value = self.reader.get_cell(1, 1)
        self.assertIsNotNone(value)

if __name__ == '__main__':
    unittest.main()