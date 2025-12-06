import unittest
from nightly_markdown_table_to_csv import converter


class TestMarkdownTableToCsv(unittest.TestCase):
    def test_basic_table(self):
        md = """
| Name | Age | City |
|------|-----|------|
| Alice | 30 | New York |
| Bob | 25 | London |
"""
        expected_csv = "Name,Age,City\nAlice,30,New York\nBob,25,London\n"
        self.assertEqual(converter.markdown_table_to_csv(md), expected_csv)

    def test_table_with_commas_and_quotes(self):
        md = """
| Description | Value |
|-------------|-------|
| "Hello, world" | 42 |
| "She said \"Hi\"" | 7 |
"""
        # Mock rationale: ensure proper CSV escaping of commas and quotes
        expected_csv = 'Description,Value\n"Hello, world",42\n"She said ""Hi""",7\n'
        self.assertEqual(converter.markdown_table_to_csv(md), expected_csv)

    def test_no_table(self):
        md = """# No tables here\nJust some text.
"""
        self.assertEqual(converter.markdown_table_to_csv(md), "")

    def test_multiple_tables_only_first_converted(self):
        md = """
| A | B |
|---|---|
| 1 | 2 |

Some intervening text.

| X | Y |
|---|---|
| 9 | 8 |
"""
        expected_csv = "A,B\n1,2\n"
        self.assertEqual(converter.markdown_table_to_csv(md), expected_csv)


if __name__ == "__main__":
    unittest.main()
