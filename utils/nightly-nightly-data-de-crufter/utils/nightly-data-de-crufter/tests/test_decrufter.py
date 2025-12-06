import unittest
from unittest.mock import patch, mock_open
import sys
import os
from io import StringIO

# Import the functions from the utility
# Assuming the utility is in src/decrufter.py relative to the test file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from decrufter import (
    remove_empty_lines,
    trim_whitespace,
    remove_duplicate_lines,
    remove_lines_by_pattern,
    convert_to_case,
    decruft_data,
    main
)
sys.path.pop(0)


class TestDecrufterFunctions(unittest.TestCase):

    def test_remove_empty_lines(self):
        lines = ["line1", "", "  ", "line2", "\t"]
        expected = ["line1", "line2"]
        self.assertEqual(remove_empty_lines(lines), expected)

        lines_empty = ["", "  ", "\t"]
        expected_empty = []
        self.assertEqual(remove_empty_lines(lines_empty), expected_empty)

        lines_full = ["line1", "line2"]
        expected_full = ["line1", "line2"]
        self.assertEqual(remove_empty_lines(lines_full), expected_full)

    def test_trim_whitespace(self):
        lines = ["  line1  ", "line2\t", "\tline3", "line4"]
        expected = ["line1", "line2", "line3", "line4"]
        self.assertEqual(trim_whitespace(lines), expected)

        lines_no_trim = ["line1", "line2"]
        expected_no_trim = ["line1", "line2"]
        self.assertEqual(trim_whitespace(lines_no_trim), expected_no_trim)

    def test_remove_duplicate_lines(self):
        lines = ["apple", "banana", "apple", "cherry", "banana", "apple"]
        expected = ["apple", "banana", "cherry"]
        self.assertEqual(remove_duplicate_lines(lines), expected)

        lines_no_duplicates = ["apple", "banana", "cherry"]
        expected_no_duplicates = ["apple", "banana", "cherry"]
        self.assertEqual(remove_duplicate_lines(lines_no_duplicates), expected_no_duplicates)

        lines_all_duplicates = ["test", "test", "test"]
        expected_all_duplicates = ["test"]
        self.assertEqual(remove_duplicate_lines(lines_all_duplicates), expected_all_duplicates)

    def test_remove_lines_by_pattern(self):
        lines = ["log: info", "data line", "log: error", "another line", "# comment"]
        
        # Test with a simple pattern
        pattern_log = r"^log:"
        expected_log = ["data line", "another line", "# comment"]
        self.assertEqual(remove_lines_by_pattern(lines, pattern_log), expected_log)

        # Test with another pattern
        pattern_comment = r"^#"
        expected_comment = ["log: info", "data line", "log: error", "another line"]
        self.assertEqual(remove_lines_by_pattern(lines, pattern_comment), expected_comment)

        # Test with no matching pattern
        pattern_nomatch = r"xyz"
        expected_nomatch = lines
        self.assertEqual(remove_lines_by_pattern(lines, pattern_nomatch), expected_nomatch)

        # Test with None pattern
        self.assertEqual(remove_lines_by_pattern(lines, None), lines)
        self.assertEqual(remove_lines_by_pattern(lines, ""), lines)


    def test_convert_to_case(self):
        lines = ["Apple", "bAnAnA", "CHERRY"]

        # Test lowercase
        expected_lower = ["apple", "banana", "cherry"]
        self.assertEqual(convert_to_case(lines, 'lower'), expected_lower)

        # Test uppercase
        expected_upper = ["APPLE", "BANANA", "CHERRY"]
        self.assertEqual(convert_to_case(lines, 'upper'), expected_upper)

        # Test titlecase
        expected_title = ["Apple", "Banana", "Cherry"]
        self.assertEqual(convert_to_case(lines, 'title'), expected_title)

        # Test invalid case type
        self.assertEqual(convert_to_case(lines, 'invalid'), lines)
        self.assertEqual(convert_to_case(lines, None), lines)

    def test_decruft_data_all_options(self):
        input_data = (
            "  Header Line  \n"
            "Data 1\n"
            "\n"
            "  Data 2  \n"
            "Data 1\n"
            "  # Comment Line\n"
            "data 3\n"
            "DATA 3\n"
            "  \t\n"
            "Footer Line\n"
        )
        expected_output = (
            "header line\n"
            "data 1\n"
            "data 2\n"
            "data 3\n"
            "footer line"
        )
        result = decruft_data(
            input_data,
            trim=True,
            empty_lines=True,
            duplicates=True,
            pattern=r"^#", # Remove comment lines
            case='lower'
        )
        self.assertEqual(result, expected_output)

    def test_decruft_data_no_options(self):
        input_data = (
            "  Header Line  \n"
            "Data 1\n"
            "\n"
            "  Data 2  \n"
            "Data 1\n"
            "  # Comment Line\n"
            "data 3\n"
            "DATA 3\n"
            "  \t\n"
            "Footer Line\n"
        )
        # If no options are enabled, it should just split and join
        expected_output = (
            "  Header Line  \n"
            "Data 1\n"
            "\n"
            "  Data 2  \n"
            "Data 1\n"
            "  # Comment Line\n"
            "data 3\n"
            "DATA 3\n"
            "  \t\n"
            "Footer Line"
        )
        result = decruft_data(
            input_data,
            trim=False,
            empty_lines=False,
            duplicates=False,
            pattern=None,
            case=None
        )
        self.assertEqual(result, expected_output)


class TestDecrufterMain(unittest.TestCase):

    def setUp(self):
        self.mock_input_data = (
            "  Line 1  \n"
            "Line 2\n"
            "\n"
            "Line 1\n"
            "  # Comment\n"
            "line 3\n"
            "LINE 3\n"
            "  \t\n"
            "Final Line\n"
        )
        self.expected_output_default = (
            "Line 1\n"
            "Line 2\n"
            "Line 3\n"
            "Final Line"
        )
        self.expected_output_pattern_case = (
            "line 1\n"
            "line 2\n"
            "line 3\n"
            "final line"
        )

    @patch('sys.stdin', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_stdin_stdout_default(self, mock_parse_args, mock_stdout, mock_stdin):
        # Mock rationale: Simulate reading from stdin and writing to stdout for CLI execution.
        mock_parse_args.return_value = argparse.Namespace(
            input_file=None, output_file=None, trim=True, empty_lines=True,
            duplicates=True, pattern=None, case=None
        )
        mock_stdin.read.return_value = self.mock_input_data
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), self.expected_output_default)

    @patch('sys.stdin', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_stdin_stdout_with_options(self, mock_parse_args, mock_stdout, mock_stdin):
        # Mock rationale: Simulate reading from stdin and writing to stdout with specific CLI options.
        mock_parse_args.return_value = argparse.Namespace(
            input_file=None, output_file=None, trim=True, empty_lines=True,
            duplicates=True, pattern=r"^#", case='lower'
        )
        mock_stdin.read.return_value = self.mock_input_data
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), self.expected_output_pattern_case)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_input_file_stdout(self, mock_parse_args, mock_stdout, mock_open_func):
        # Mock rationale: Simulate reading from a file and writing to stdout.
        # mock_open_func is used to control file content without actual file I/O.
        mock_parse_args.return_value = argparse.Namespace(
            input_file="input.txt", output_file=None, trim=True, empty_lines=True,
            duplicates=True, pattern=None, case=None
        )
        mock_open_func.return_value.read.return_value = self.mock_input_data
        main()
        mock_open_func.assert_called_once_with("input.txt", 'r', encoding='utf-8')
        self.assertEqual(mock_stdout.getvalue().strip(), self.expected_output_default)

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO) # Still patch stdout to ensure nothing unexpected is printed
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_input_file_output_file(self, mock_parse_args, mock_stdout, mock_open_func):
        # Mock rationale: Simulate reading from an input file and writing to an output file.
        # mock_open_func is used to control file content and capture written data.
        mock_parse_args.return_value = argparse.Namespace(
            input_file="input.txt", output_file="output.txt", trim=True, empty_lines=True,
            duplicates=True, pattern=r"^#", case='lower'
        )
        # Configure mock_open for reading and writing
        mock_open_func.side_effect = [
            mock_open(read_data=self.mock_input_data).return_value, # For input.txt
            mock_open().return_value # For output.txt
        ]
        main()
        # Assert calls to open
        mock_open_func.assert_any_call("input.txt", 'r', encoding='utf-8')
        mock_open_func.assert_any_call("output.txt", 'w', encoding='utf-8')
        # Assert content written to output file
        handle = mock_open_func()
        handle.write.assert_called_once_with(self.expected_output_pattern_case)
        self.assertEqual(mock_stdout.getvalue(), "") # Ensure nothing was printed to stdout

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_input_file_not_found(self, mock_parse_args, mock_exit, mock_stderr, mock_open_func):
        # Mock rationale: Simulate a FileNotFoundError when trying to open the input file.
        # mock_exit is used to prevent the test from actually exiting.
        mock_parse_args.return_value = argparse.Namespace(
            input_file="nonexistent.txt", output_file=None, trim=True, empty_lines=True,
            duplicates=True, pattern=None, case=None
        )
        mock_open_func.side_effect = FileNotFoundError
        main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Input file 'nonexistent.txt' not found.", mock_stderr.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_output_file_write_error(self, mock_parse_args, mock_exit, mock_stderr, mock_open_func):
        # Mock rationale: Simulate an IOError when trying to write to the output file.
        # mock_exit is used to prevent the test from actually exiting.
        mock_parse_args.return_value = argparse.Namespace(
            input_file="input.txt", output_file="/dev/null/output.txt", trim=True, empty_lines=True,
            duplicates=True, pattern=None, case=None
        )
        # Configure mock_open for reading and then raising an error on write
        mock_open_func.side_effect = [
            mock_open(read_data=self.mock_input_data).return_value, # For input.txt
            mock_open(side_effect=IOError("Permission denied")).return_value # For output.txt
        ]
        main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error writing to output file: Permission denied", mock_stderr.getvalue())

    @patch('sys.stdin', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_trim(self, mock_parse_args, mock_stdout, mock_stdin):
        # Mock rationale: Test the --no-trim flag.
        mock_parse_args.return_value = argparse.Namespace(
            input_file=None, output_file=None, trim=False, empty_lines=True,
            duplicates=True, pattern=None, case=None
        )
        input_data_with_whitespace = "  line1  \nline2\n  line1  "
        expected_output = "  line1  \nline2" # Duplicates removed, empty lines removed, but whitespace preserved
        mock_stdin.read.return_value = input_data_with_whitespace
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch('sys.stdin', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_empty_lines(self, mock_parse_args, mock_stdout, mock_stdin):
        # Mock rationale: Test the --no-empty-lines flag.
        mock_parse_args.return_value = argparse.Namespace(
            input_file=None, output_file=None, trim=True, empty_lines=False,
            duplicates=True, pattern=None, case=None
        )
        input_data_with_empty = "line1\n\n  \nline2\nline1"
        expected_output = "line1\n\n\nline2" # Duplicates removed, whitespace trimmed, but empty lines preserved
        mock_stdin.read.return_value = input_data_with_empty
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)

    @patch('sys.stdin', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_duplicates(self, mock_parse_args, mock_stdout, mock_stdin):
        # Mock rationale: Test the --no-duplicates flag.
        mock_parse_args.return_value = argparse.Namespace(
            input_file=None, output_file=None, trim=True, empty_lines=True,
            duplicates=False, pattern=None, case=None
        )
        input_data_with_duplicates = "line1\nline2\nline1\nline3"
        expected_output = "line1\nline2\nline1\nline3" # Empty lines removed, whitespace trimmed, but duplicates preserved
        mock_stdin.read.return_value = input_data_with_duplicates
        main()
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)


if __name__ == '__main__':
    unittest.main()
