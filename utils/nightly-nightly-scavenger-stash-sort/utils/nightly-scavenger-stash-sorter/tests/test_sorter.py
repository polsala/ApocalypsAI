import unittest
import sys
import io
from unittest.mock import patch, mock_open
from src.sorter import StashSorter, main

class TestStashSorter(unittest.TestCase):

    def setUp(self):
        self.sorter = StashSorter()

    def test_categorize_item_food(self):
        self.assertEqual(self.sorter.categorize_item("can of beans"), {
            "category": "Food", "priority": "High", "location": "Pantry"
        })
        self.assertEqual(self.sorter.categorize_item("fresh apple"), {
            "category": "Food", "priority": "High", "location": "Pantry"
        })
        self.assertEqual(self.sorter.categorize_item("purified water"), {
            "category": "Food", "priority": "High", "location": "Pantry"
        })

    def test_categorize_item_tools(self):
        self.assertEqual(self.sorter.categorize_item("rusty wrench"), {
            "category": "Tools", "priority": "Medium", "location": "Workshop"
        })
        self.assertEqual(self.sorter.categorize_item("survival knife"), {
            "category": "Tools", "priority": "Medium", "location": "Workshop"
        })

    def test_categorize_item_materials(self):
        self.assertEqual(self.sorter.categorize_item("pile of scrap metal"), {
            "category": "Materials", "priority": "Medium", "location": "Storage Shed"
        })
        self.assertEqual(self.sorter.categorize_item("copper wire"), {
            "category": "Materials", "priority": "Medium", "location": "Storage Shed"
        })

    def test_categorize_item_medical(self):
        self.assertEqual(self.sorter.categorize_item("first aid bandages"), {
            "category": "Medical", "priority": "High", "location": "Infirmary"
        })
        self.assertEqual(self.sorter.categorize_item("painkillers (expired)"), {
            "category": "Medical", "priority": "High", "location": "Infirmary"
        })

    def test_categorize_item_junk(self):
        self.assertEqual(self.sorter.categorize_item("broken toy car"), {
            "category": "Junk", "priority": "Low", "location": "Disposal Pile"
        })
        self.assertEqual(self.sorter.categorize_item("old boot"), {
            "category": "Junk", "priority": "Low", "location": "Disposal Pile"
        })

    def test_categorize_item_uncategorized(self):
        self.assertEqual(self.sorter.categorize_item("mysterious glowing rock"), {
            "category": "Uncategorized", "priority": "Unknown", "location": "Undetermined"
        })
        self.assertEqual(self.sorter.categorize_item("alien artifact"), {
            "category": "Uncategorized", "priority": "Unknown", "location": "Undetermined"
        })
        self.assertEqual(self.sorter.categorize_item(""), {
            "category": "Uncategorized", "priority": "Unknown", "location": "Undetermined"
        })

    def test_sort_stash(self):
        items = ["apple", "rusty wrench", "scrap metal", "mysterious glowing rock"]
        expected = [
            {"item": "apple", "category": "Food", "priority": "High", "location": "Pantry"},
            {"item": "rusty wrench", "category": "Tools", "priority": "Medium", "location": "Workshop"},
            {"item": "scrap metal", "category": "Materials", "priority": "Medium", "location": "Storage Shed"},
            {"item": "mysterious glowing rock", "category": "Uncategorized", "priority": "Unknown", "location": "Undetermined"}
        ]
        self.assertEqual(self.sorter.sort_stash(items), expected)

    def test_sort_stash_empty(self):
        self.assertEqual(self.sorter.sort_stash([]), [])

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_display_report(self, mock_stdout):
        sorted_items = [
            {"item": "apple", "category": "Food", "priority": "High", "location": "Pantry"},
            {"item": "rusty wrench", "category": "Tools", "priority": "Medium", "location": "Workshop"}
        ]
        self.sorter.display_report(sorted_items)
        output = mock_stdout.getvalue()
        self.assertIn("--- Scavenger's Stash Report ---", output)
        self.assertIn("Item: apple", output)
        self.assertIn("Category: Food", output)
        self.assertIn("Location: Pantry", output)
        self.assertIn("Item: rusty wrench", output)
        self.assertIn("Category: Tools", output)
        self.assertIn("Location: Workshop", output)
        self.assertIn("--- End of Report ---", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_display_report_empty(self, mock_stdout):
        self.sorter.display_report([])
        output = mock_stdout.getvalue()
        self.assertIn("No items to report. Time to go scavenging!", output)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.sorter.StashSorter.display_report')
    @patch('src.sorter.StashSorter.sort_stash')
    def test_main_with_items_arg(self, mock_sort_stash, mock_display_report, mock_parse_args):
        # Mock rationale: Simulate command-line arguments without actually parsing sys.argv.
        mock_parse_args.return_value = argparse.Namespace(
            items="apple,wrench,scrap metal", file=None
        )
        mock_sort_stash.return_value = [
            {"item": "apple", "category": "Food", "priority": "High", "location": "Pantry"},
            {"item": "wrench", "category": "Tools", "priority": "Medium", "location": "Workshop"},
            {"item": "scrap metal", "category": "Materials", "priority": "Medium", "location": "Storage Shed"}
        ]

        main()

        mock_sort_stash.assert_called_once_with(["apple", "wrench", "scrap metal"])
        mock_display_report.assert_called_once()
        self.assertEqual(mock_display_report.call_args[0][0], mock_sort_stash.return_value)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.open', new_callable=mock_open, read_data="can of beans\nold boot\n# This is a comment\ncopper wire")
    @patch('src.sorter.StashSorter.display_report')
    @patch('src.sorter.StashSorter.sort_stash')
    def test_main_with_file_arg(self, mock_sort_stash, mock_display_report, mock_open_file, mock_parse_args):
        # Mock rationale: Simulate command-line arguments and file reading without actual file I/O.
        mock_parse_args.return_value = argparse.Namespace(
            items=None, file="test_haul.txt"
        )
        mock_sort_stash.return_value = [
            {"item": "can of beans", "category": "Food", "priority": "High", "location": "Pantry"},
            {"item": "old boot", "category": "Junk", "priority": "Low", "location": "Disposal Pile"},
            {"item": "copper wire", "category": "Materials", "priority": "Medium", "location": "Storage Shed"}
        ]

        main()

        mock_open_file.assert_called_once_with("test_haul.txt", 'r')
        mock_sort_stash.assert_called_once_with(["can of beans", "old boot", "copper wire"])
        mock_display_report.assert_called_once()
        self.assertEqual(mock_display_report.call_args[0][0], mock_sort_stash.return_value)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_file_not_found(self, mock_exit, mock_stderr, mock_parse_args):
        # Mock rationale: Simulate command-line arguments and a FileNotFoundError without actual file I/O.
        mock_parse_args.return_value = argparse.Namespace(
            items=None, file="non_existent_file.txt"
        )
        # Simulate FileNotFoundError when open() is called
        with patch('builtins.open', side_effect=FileNotFoundError):
            main()

        mock_stderr_output = mock_stderr.getvalue()
        self.assertIn("Error: File 'non_existent_file.txt' not found.", mock_stderr_output)
        mock_exit.assert_called_once_with(1)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_no_args(self, mock_exit, mock_stdout, mock_parse_args):
        # Mock rationale: Simulate command-line arguments where none are provided.
        mock_parse_args.return_value = argparse.Namespace(
            items=None, file=None
        )

        main()

        output = mock_stdout.getvalue()
        self.assertIn("usage: sorter.py", output) # Checks if help message is printed
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
