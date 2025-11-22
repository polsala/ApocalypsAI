import unittest
from unittest.mock import patch, mock_open
import datetime
import os

# Import the functions to be tested
from src.manifest_generator import parse_item_line, generate_markdown_manifest, main

class TestManifestGenerator(unittest.TestCase):

    def test_parse_item_line_valid(self):
        # Test a line with all components
        line = "Rusty wrench | Tools | repair, melee"
        expected = {'name': 'Rusty wrench', 'category': 'Tools', 'tags': ['repair', 'melee']}
        self.assertEqual(parse_item_line(line), expected)

        # Test a line with no tags
        line = "Can of beans | Food"
        expected = {'name': 'Can of beans', 'category': 'Food', 'tags': []}
        self.assertEqual(parse_item_line(line), expected)

        # Test a line with extra spaces
        line = "  Tattered map  |  Info  |  navigation , paper  "
        expected = {'name': 'Tattered map', 'category': 'Info', 'tags': ['navigation', 'paper']}
        self.assertEqual(parse_item_line(line), expected)

    def test_parse_item_line_invalid(self):
        # Test a line with too few parts
        self.assertIsNone(parse_item_line("Just an item"))
        self.assertIsNone(parse_item_line("Item |"))
        self.assertIsNone(parse_item_line("|"))
        self.assertIsNone(parse_item_line(""))

    @patch('datetime.date')
    def test_generate_markdown_manifest_basic(self, mock_date):
        # Mock rationale: Ensure the date in the manifest is consistent for deterministic testing.
        mock_date.today.return_value = datetime.date(2023, 10, 27)

        items = [
            {'name': 'Can of beans', 'category': 'Food', 'tags': ['edible']},
            {'name': 'Rusty wrench', 'category': 'Tools', 'tags': ['repair']}
        ]
        expected_markdown = (
            "# Scavenger's Manifest - 2023-10-27\n\n"
            "## Food\n"
            "- Can of beans (edible)\n\n"
            "## Tools\n"
            "- Rusty wrench (repair)"
        )
        self.assertEqual(generate_markdown_manifest(items), expected_markdown)

    @patch('datetime.date')
    def test_generate_markdown_manifest_multiple_categories_and_tags(self, mock_date):
        # Mock rationale: Ensure the date in the manifest is consistent for deterministic testing.
        mock_date.today.return_value = datetime.date(2023, 10, 27)

        items = [
            {'name': 'Can of beans', 'category': 'Food', 'tags': ['edible', 'long-shelf-life']},
            {'name': 'Tattered map', 'category': 'Info', 'tags': ['navigation']},
            {'name': 'Broken radio', 'category': 'Electronics', 'tags': ['salvage', 'broken']},
            {'name': 'Medical kit (partial)', 'category': 'Medical', 'tags': ['first-aid']},
            {'name': 'Rusty wrench', 'category': 'Tools', 'tags': ['repair', 'melee']},
            {'name': 'Fresh apple', 'category': 'Food', 'tags': ['perishable']}
        ]
        expected_markdown = (
            "# Scavenger's Manifest - 2023-10-27\n\n"
            "## Electronics\n"
            "- Broken radio (salvage, broken)\n\n"
            "## Food\n"
            "- Can of beans (edible, long-shelf-life)\n"
            "- Fresh apple (perishable)\n\n"
            "## Info\n"
            "- Tattered map (navigation)\n\n"
            "## Medical\n"
            "- Medical kit (partial) (first-aid)\n\n"
            "## Tools\n"
            "- Rusty wrench (repair, melee)"
        )
        self.assertEqual(generate_markdown_manifest(items), expected_markdown)

    @patch('datetime.date')
    def test_generate_markdown_manifest_empty_items(self, mock_date):
        # Mock rationale: Ensure the date in the manifest is consistent for deterministic testing.
        mock_date.today.return_value = datetime.date(2023, 10, 27)

        items = []
        expected_markdown = "# Scavenger's Manifest - 2023-10-27"
        self.assertEqual(generate_markdown_manifest(items), expected_markdown)

    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('datetime.date')
    def test_main_success(self, mock_date, mock_parse_args, mock_file_open):
        # Mock rationale: 
        # 1. `mock_date`: Fixes the date for deterministic output.
        # 2. `mock_parse_args`: Simulates command-line arguments without actually parsing `sys.argv`.
        # 3. `mock_file_open`: Intercepts file I/O to provide test input and capture output without touching the filesystem.

        mock_date.today.return_value = datetime.date(2023, 10, 27)
        mock_parse_args.return_value = argparse.Namespace(
            input='test_input.txt',
            output='test_output.md'
        )

        # Configure the mock_open to return specific content for the input file
        mock_file_open.side_effect = [
            mock_open(read_data="Rusty wrench | Tools | repair\nCan of beans | Food").return_value, # For reading input
            mock_open().return_value # For writing output
        ]

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()
            self.assertIn("Manifest successfully generated", mock_stdout.getvalue())

        # Verify that the output file was written correctly
        handle = mock_file_open().write
        expected_output = (
            "# Scavenger's Manifest - 2023-10-27\n\n"
            "## Food\n"
            "- Can of beans\n\n"
            "## Tools\n"
            "- Rusty wrench (repair)"
        )
        handle.assert_called_once_with(expected_output)

    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_input_file_not_found(self, mock_parse_args, mock_file_open):
        # Mock rationale: 
        # 1. `mock_parse_args`: Simulates command-line arguments.
        # 2. `mock_file_open`: Simulates `FileNotFoundError` when trying to open the input file.

        mock_parse_args.return_value = argparse.Namespace(
            input='non_existent.txt',
            output='output.md'
        )
        mock_file_open.side_effect = FileNotFoundError # Simulate input file not found

        import io
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()
            self.assertIn("Error: Input file 'non_existent.txt' not found.", mock_stdout.getvalue())
        mock_file_open.assert_called_once_with('non_existent.txt', 'r', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('datetime.date')
    def test_main_empty_input_file(self, mock_date, mock_parse_args, mock_file_open):
        # Mock rationale: 
        # 1. `mock_date`: Fixes the date for deterministic output.
        # 2. `mock_parse_args`: Simulates command-line arguments.
        # 3. `mock_file_open`: Provides an empty string for the input file content.

        mock_date.today.return_value = datetime.date(2023, 10, 27)
        mock_parse_args.return_value = argparse.Namespace(
            input='empty_input.txt',
            output='empty_output.md'
        )

        mock_file_open.side_effect = [
            mock_open(read_data="").return_value, # Empty input file
            mock_open().return_value # For writing output
        ]

        import io
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            main()
            self.assertIn("No valid items found in the input file. Generating empty manifest.", mock_stdout.getvalue())

        handle = mock_file_open().write
        expected_output = "# Scavenger's Manifest - 2023-10-27"
        handle.assert_called_once_with(expected_output)

if __name__ == '__main__':
    unittest.main()
