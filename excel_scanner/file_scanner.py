from pathlib import Path
from typing import Union

from .scanner import ExcelScanner


class FileScanner:
    def __init__(self, filepath: Union[str, Path]) -> None:  # <-- Accepts both str and Path
        self.page_header = {
            'Quotation': 'J6',
            'Bill Company': 'B6',
            'Bill Address 1': 'B7',
            'Bill Address 2': 'B8',
            'Bill Address 3': 'B9',
            'Bill Attention': 'B10',
            'Bill Tel': 'G10',
            'Deliver Company': 'B12',
            'Deliver Address 1': 'B13',
            'Deliver Address 2': 'B14',
            'Deliver Address 3': 'B15',
            'Deliver Attention': 'B16',
            'Deliver Tel': 'G16',
            'Quotation No': 'K9',
            'Date': 'K11',
            'Currency': 'K12',
            'Payment Term': 'K13',
            'Sales Person': 'K14',
            'Email Address': 'K15'
        }

        self.cell_offset_info = {
            'SUB-TOTAL': '2',
            '9% GST': '2',
            'TOTAL AMOUNT': '2'
        }

        self.content = {
            'first_row_keywords': ['Product Description', 'Quantity', 'Price ($)'],
            'end_row_keywords': ['E. & O.E.', 'SUB-TOTAL'],
            'keyword' : ['product', 'model', 'brand', 'capacity', 's/n']
        }

