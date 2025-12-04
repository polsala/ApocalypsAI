import unittest
from unittest.mock import patch, mock_open
import os
import sys

# Add the src directory to the Python path for importing the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from fossil_cleaner import clean_config_content, main

class TestFossilCleaner(unittest.TestCase):

    def test_clean_config_content_basic(self):
        # Test basic cleaning: full-line comments and empty lines
        input_lines = [
            "# This is a comment\n",
            "setting1=value1 # inline comment\n",
            "\n",
            "; Another type of comment\n",
            "setting2 = value2\n",
            "  \n", # whitespace-only line
            "# Deprecated setting\n",
            "#old_setting=old_value\n"
        ]
        expected_lines = [
            "setting1=value1 # inline comment\n",
            "setting2 = value2\n"
        ]
        self.assertEqual(clean_config_content(input_lines, ['#', ';']), expected_lines)

    def test_clean_config_content_no_changes(self):
        # Test content that requires no cleaning
        input_lines = [
            "setting1=value1\n",
            "setting2=value2\n"
        ]
        expected_lines = [
            "setting1=value1\n",
            "setting2=value2\n"
        ]
        self.assertEqual(clean_config_content(input_lines, ['#', ';']), expected_lines)

    def test_clean_config_content_only_comments_and_empty_lines(self):
        # Test content consisting only of comments and empty lines
        input_lines = [
            "# Comment 1\n",
            "\n",
            "; Comment 2\n",
            "  \n"
        ]
        expected_lines = []
        self.assertEqual(clean_config_content(input_lines, ['#', ';']), expected_lines)

    def test_clean_config_content_different_comment_chars(self):
        # Test with different comment characters, e.g., for JSONC
        input_lines = [
            "// This is a JSONC comment\n",
            "{\n",
            "  \"key\": \"value\", // inline comment\n",
            "  // Another comment\n",
            "  \"another_key\": \"another_value\"\n",
            "}\n"
        ]
        expected_lines = [
            "{\n",
            "  \"key\": \"value\", // inline comment\n",
            "  \"another_key\": \"another_value\"\n",
            "}\n"
        ]
        self.assertEqual(clean_config_content(input_lines, ['//']), expected_lines)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('shutil.copyfile')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print') # Mock rationale: Capture print statements for verification
    def test_main_overwrite_with_backup(self, mock_print, mock_parse_args, mock_copyfile, mock_open_file, mock_exists):
        # Mock rationale: Simulate file existence, file read/write, and backup operation
        # without touching the actual filesystem. Also mock argparse to control CLI args.
        mock_exists.return_value = True
        mock_parse_args.return_value = argparse.Namespace(
            input_file_path="test_config.ini",
            output=None,
            backup=True,
            comment_chars=['#', ';']
        )
        
        mock_open_file.side_effect = [
            mock_open(read_data="# Comment\nsetting=value\n\n").return_value, # For reading input
            mock_open().return_value # For writing output
        ]

        main()

        mock_exists.assert_called_once_with("test_config.ini")
        mock_copyfile.assert_called_once_with("test_config.ini", "test_config.ini.bak")
        # Check that open was called for reading and writing
        self.assertEqual(mock_open_file.call_count, 2)
        mock_open_file.assert_any_call("test_config.ini", 'r', encoding='utf-8')
        mock_open_file.assert_any_call("test_config.ini", 'w', encoding='utf-8')
        mock_open_file().writelines.assert_called_once_with(["setting=value\n"])
        mock_print.assert_any_call("Backup created at 'test_config.ini.bak'")
        mock_print.assert_any_call("Configuration file cleaned and saved to 'test_config.ini'.")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('shutil.copyfile')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print') # Mock rationale: Capture print statements for verification
    def test_main_output_to_new_file(self, mock_print, mock_parse_args, mock_copyfile, mock_open_file, mock_exists):
        # Mock rationale: Simulate file existence, file read/write to a new file, and no backup operation
        # without touching the actual filesystem. Also mock argparse to control CLI args.
        mock_exists.return_value = True
        mock_parse_args.return_value = argparse.Namespace(
            input_file_path="input.conf",
            output="output.conf",
            backup=False,
            comment_chars=['#', ';']
        )
        
        mock_open_file.side_effect = [
            mock_open(read_data="# Comment\nkey=val\n").return_value, # For reading input
            mock_open().return_value # For writing output
        ]

        main()

        mock_exists.assert_called_once_with("input.conf")
        mock_copyfile.assert_not_called()
        self.assertEqual(mock_open_file.call_count, 2)
        mock_open_file.assert_any_call("input.conf", 'r', encoding='utf-8')
        mock_open_file.assert_any_call("output.conf", 'w', encoding='utf-8')
        mock_open_file().writelines.assert_called_once_with(["key=val\n"])
        mock_print.assert_any_call("Configuration file cleaned and saved to 'output.conf'.")

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_file_not_found(self, mock_print, mock_exit, mock_parse_args, mock_open_file, mock_exists):
        # Mock rationale: Simulate a non-existent input file and verify error handling.
        # Mock sys.exit to prevent actual program termination during test.
        mock_exists.return_value = False
        mock_parse_args.return_value = argparse.Namespace(
            input_file_path="non_existent.conf",
            output=None,
            backup=False,
            comment_chars=['#', ';']
        )

        main()

        mock_exists.assert_called_once_with("non_existent.conf")
        mock_print.assert_called_with("Error: Input file not found at 'non_existent.conf'")
        mock_exit.assert_called_once_with(1)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_exception_handling(self, mock_print, mock_exit, mock_parse_args, mock_open_file, mock_exists):
        # Mock rationale: Simulate an arbitrary exception during file processing and verify error handling.
        # Mock sys.exit to prevent actual program termination during test.
        mock_exists.return_value = True
        mock_parse_args.return_value = argparse.Namespace(
            input_file_path="error_file.conf",
            output=None,
            backup=False,
            comment_chars=['#', ';']
        )
        
        # Simulate an IOError during file read
        mock_open_file.side_effect = IOError("Permission denied")

        main()

        mock_print.assert_called_with("An error occurred: Permission denied")
        mock_exit.assert_called_once_with(1)
