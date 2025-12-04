import unittest
from markdown_table_formatter.src.formatter import csv_to_markdown

class TestMarkdownTableFormatter(unittest.TestCase):
    def test_basic_conversion(self):
        csv_data = """name,age,city
Alice,30,New York
Bob,25,Los Angeles"""
        expected = """| name | age | city |
| --- | --- | --- |
| Alice | 30 | New York |
| Bob | 25 | Los Angeles |"""
        self.assertEqual(csv_to_markdown(csv_data), expected)

    def test_empty_input(self):
        self.assertEqual(csv_to_markdown(""), "")

    def test_single_row(self):
        csv_data = """header1,header2
value1,value2"""
        expected = """| header1 | header2 |
| --- | --- |
| value1 | value2 |"""
        self.assertEqual(csv_to_markdown(csv_data), expected)

if __name__ == "__main__":
    unittest.main()
