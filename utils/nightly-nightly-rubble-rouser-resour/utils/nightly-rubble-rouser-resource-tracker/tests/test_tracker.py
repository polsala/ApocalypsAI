import unittest
from unittest.mock import patch, mock_open
import os
from src.tracker import load_resources, summarize_resources, identify_low_resources, main

class TestResourceTracker(unittest.TestCase):

    def test_load_resources_success(self):
        # Mock rationale: Simulate reading a valid resource file without actual file I/O.
        mock_file_content = "Water: 10\nFood: 5\nBatteries: 20"
        with patch("builtins.open", mock_open(read_data=mock_file_content)) as mock_file:
            with patch("os.path.exists", return_value=True): # Mock rationale: Simulate file existence check.
                resources = load_resources("dummy_path.txt")
                self.assertEqual(resources, {"Water": 10, "Food": 5, "Batteries": 20})
                mock_file.assert_called_once_with("dummy_path.txt", 'r', encoding='utf-8')

    def test_load_resources_file_not_found(self):
        # Mock rationale: Simulate a non-existent file to test error handling.
        with patch("os.path.exists", return_value=False):
            with self.assertRaises(FileNotFoundError):
                load_resources("non_existent.txt")

    def test_load_resources_empty_file(self):
        # Mock rationale: Simulate an empty file.
        with patch("builtins.open", mock_open(read_data="")) as mock_file:
            with patch("os.path.exists", return_value=True):
                resources = load_resources("empty.txt")
                self.assertEqual(resources, {})

    def test_load_resources_malformed_lines(self):
        # Mock rationale: Simulate a file with malformed lines to test robustness.
        mock_file_content = "Water: 10\nInvalid Line\nFood: five\nBatteries: 20"
        with patch("builtins.open", mock_open(read_data=mock_file_content)) as mock_file:
            with patch("os.path.exists", return_value=True):
                # We expect warnings to be printed, but the valid lines should still be parsed.
                with patch('builtins.print') as mock_print: # Mock rationale: Capture print statements for warnings.
                    resources = load_resources("malformed.txt")
                    self.assertEqual(resources, {"Water": 10, "Batteries": 20})
                    mock_print.assert_any_call("Warning: Could not parse line 'Invalid Line'. Skipping.")
                    mock_print.assert_any_call("Warning: Could not parse line 'Food: five'. Skipping.")

    def test_load_resources_negative_quantity(self):
        # Mock rationale: Simulate a file with a negative quantity.
        mock_file_content = "Water: 10\nBroken Item: -5\nFood: 5"
        with patch("builtins.open", mock_open(read_data=mock_file_content)) as mock_file:
            with patch("os.path.exists", return_value=True):
                with patch('builtins.print') as mock_print:
                    resources = load_resources("negative.txt")
                    self.assertEqual(resources, {"Water": 10, "Food": 5})
                    mock_print.assert_any_call("Warning: Negative quantity for 'Broken Item'. Skipping.")

    def test_summarize_resources_empty(self):
        summary = summarize_resources({})
        self.assertEqual(summary, ["--- Resource Inventory Summary ---", "No resources tracked."])

    def test_summarize_resources_with_data(self):
        resources = {"Food": 5, "Water": 10, "Batteries": 20}
        summary = summarize_resources(resources)
        expected_summary = [
            "--- Resource Inventory Summary ---",
            "Batteries: 20 units",
            "Food: 5 units",
            "Water: 10 units"
        ]
        self.assertEqual(summary, expected_summary)

    def test_identify_low_resources_none_low(self):
        resources = {"Water": 10, "Food": 15, "Batteries": 20}
        low_resources = identify_low_resources(resources, 5);
        expected_low = [
            "--- Low Resources (below 5 units) ---",
            "All resources are above the threshold. Good job!"
        ]
        self.assertEqual(low_resources, expected_low)

    def test_identify_low_resources_some_low(self):
        resources = {"Water": 3, "Food": 15, "Batteries": 2, "Medical Supplies": 8}
        low_resources = identify_low_resources(resources, 5)
        expected_low = [
            "--- Low Resources (below 5 units) ---",
            "Batteries: 2 units (CRITICAL!)",
            "Water: 3 units (CRITICAL!)"
        ]
        self.assertEqual(low_resources, expected_low)

    def test_identify_low_resources_all_low(self):
        resources = {"Water": 3, "Food": 1, "Batteries": 2}
        low_resources = identify_low_resources(resources, 5)
        expected_low = [
            "--- Low Resources (below 5 units) ---",
            "Batteries: 2 units (CRITICAL!)",
            "Food: 1 units (CRITICAL!)",
            "Water: 3 units (CRITICAL!)"
        ]
        self.assertEqual(low_resources, expected_low)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.tracker.load_resources')
    @patch('src.tracker.summarize_resources')
    @patch('src.tracker.identify_low_resources')
    @patch('builtins.print')
    def test_main_success(self, mock_print, mock_identify, mock_summarize, mock_load, mock_parse_args):
        # Mock rationale: Simulate command-line arguments, resource loading, and output generation.
        mock_parse_args.return_value = argparse.Namespace(file="test.txt", threshold=5)
        mock_load.return_value = {"Water": 10, "Food": 3}
        mock_summarize.return_value = ["Summary Line 1"]
        mock_identify.return_value = ["Low Line 1"]

        main()

        mock_load.assert_called_once_with("test.txt")
        mock_summarize.assert_called_once_with({"Water": 10, "Food": 3})
        mock_identify.assert_called_once_with({"Water": 10, "Food": 3}, 5)
        mock_print.assert_any_call("Summary Line 1")
        mock_print.assert_any_call("Low Line 1")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.tracker.load_resources', side_effect=FileNotFoundError("Mocked file not found"))
    @patch('builtins.print')
    @patch('sys.exit') # Mock rationale: Prevent actual exit during testing.
    def test_main_file_not_found_error(self, mock_exit, mock_print, mock_load, mock_parse_args):
        # Mock rationale: Simulate a FileNotFoundError during resource loading.
        mock_parse_args.return_value = argparse.Namespace(file="non_existent.txt", threshold=5)

        main()

        mock_print.assert_called_once_with("Error: Mocked file not found")
        mock_exit.assert_called_once_with(1)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.tracker.load_resources', side_effect=Exception("Generic error"))
    @patch('builtins.print')
    @patch('sys.exit') # Mock rationale: Prevent actual exit during testing.
    def test_main_generic_error(self, mock_exit, mock_print, mock_load, mock_parse_args):
        # Mock rationale: Simulate a generic unexpected error.
        mock_parse_args.return_value = argparse.Namespace(file="error.txt", threshold=5)

        main()

        mock_print.assert_called_once_with("An unexpected error occurred: Generic error")
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
