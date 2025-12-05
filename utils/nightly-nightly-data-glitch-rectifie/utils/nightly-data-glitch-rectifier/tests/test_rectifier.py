import unittest
import json
import os
import sys
from unittest.mock import patch, mock_open

# Adjust path to import the rectifier module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from rectifier import rectify_string, main

class TestRectifier(unittest.TestCase):

    def test_trim_whitespace(self):
        rules = [{"type": "trim"}]
        self.assertEqual(rectify_string("  hello world  ", rules), "hello world")
        self.assertEqual(rectify_string("hello world", rules), "hello world")
        self.assertEqual(rectify_string(" \t\n ", rules), "")

    def test_normalize_case_lower(self):
        rules = [{"type": "lower"}]
        self.assertEqual(rectify_string("HELLO WORLD", rules), "hello world")
        self.assertEqual(rectify_string("Hello World", rules), "hello world")

    def test_normalize_case_upper(self):
        rules = [{"type": "upper"}]
        self.assertEqual(rectify_string("hello world", rules), "HELLO WORLD")
        self.assertEqual(rectify_string("Hello World", rules), "HELLO WORLD")

    def test_normalize_case_title(self):
        rules = [{"type": "title"}]
        self.assertEqual(rectify_string("hello world", rules), "Hello World")
        self.assertEqual(rectify_string("HELLO WORLD", rules), "Hello World")
        self.assertEqual(rectify_string("hello-world", rules), "Hello-World") # Title case splits on non-alphanumeric

    def test_simple_replace(self):
        rules = [{"type": "replace", "old": "glitch", "new": "fix"}]
        self.assertEqual(rectify_string("data glitch", rules), "data fix")
        self.assertEqual(rectify_string("no match", rules), "no match")
        self.assertEqual(rectify_string("glitch glitch", rules), "fix fix")

    def test_regex_replace(self):
        rules = [{"type": "regex_replace", "pattern": r"\d+", "replacement": "#"}]
        self.assertEqual(rectify_string("item 123 quantity 45", rules), "item # quantity #")
        self.assertEqual(rectify_string("no numbers", rules), "no numbers")

    def test_multiple_rules_sequential(self):
        rules = [
            {"type": "trim"},
            {"type": "lower"},
            {"type": "replace", "old": "error", "new": "ok"}
        ]
        self.assertEqual(rectify_string("  DATA ERROR  ", rules), "data ok")
        self.assertEqual(rectify_string("  ANOTHER OK  ", rules), "another ok")

    def test_invalid_rule_type(self):
        rules = [{"type": "unknown_type"}]
        with self.assertRaises(ValueError) as cm:
            rectify_string("test", rules)
        self.assertIn("Unknown rectification rule type: unknown_type", str(cm.exception))

    def test_missing_replace_params(self):
        rules = [{"type": "replace", "old": "a"}] # Missing 'new'
        with self.assertRaises(ValueError) as cm:
            rectify_string("test", rules)
        self.assertIn("Missing 'old' or 'new' for 'replace' rule", str(cm.exception))

    def test_missing_regex_replace_params(self):
        rules = [{"type": "regex_replace", "pattern": "a"}] # Missing 'replacement'
        with self.assertRaises(ValueError) as cm:
            rectify_string("test", rules)
        self.assertIn("Missing 'pattern' or 'replacement' for 'regex_replace' rule", str(cm.exception))

    def test_main_cli_input_output_files(self):
        mock_rules = [
            {"type": "trim"},
            {"type": "upper"}
        ]
        mock_input_content = "  hello world  \n  test line  \n"
        expected_output_content = "HELLO WORLD\nTEST LINE\n"

        # Mock rationale: We need to simulate file system interactions (reading input, rules, writing output)
        # without actually touching the disk. `mock_open` allows us to control the content returned
        # when files are opened and capture what's written.
        with patch("builtins.open", new_callable=mock_open) as m_open:
            # Configure mock_open for rules file
            m_open.side_effect = [
                unittest.mock.mock_open(read_data=json.dumps(mock_rules)).return_value, # For rules.json
                unittest.mock.mock_open(read_data=mock_input_content).return_value,    # For input.txt
                unittest.mock.mock_open().return_value                                 # For output.txt
            ]
            
            # Mock rationale: `sys.argv` is how command-line arguments are passed.
            # We need to replace it to simulate specific CLI calls.
            with patch("sys.argv", ["rectifier.py", "-i", "input.txt", "-r", "rules.json", "-o", "output.txt"]):
                main()
            
            # Assertions for file operations
            m_open.assert_any_call("rules.json", "r", encoding="utf-8")
            m_open.assert_any_call("input.txt", "r", encoding="utf-8")
            m_open.assert_any_call("output.txt", "w", encoding="utf-8")
            
            # Get the mock file handle for the output file
            output_handle = m_open().write
            output_handle.assert_called_once_with(expected_output_content)

    def test_main_cli_stdin_stdout(self):
        mock_rules = [
            {"type": "trim"},
            {"type": "lower"}
        ]
        mock_input_content = "  HELLO WORLD  \n  ANOTHER LINE  \n"
        expected_output_content = "hello world\nanother line\n"

        # Mock rationale: Similar to file I/O, we need to control `sys.stdin` and `sys.stdout`
        # to simulate input from the console and capture output.
        with patch("builtins.open", new_callable=mock_open) as m_open:
            m_open.return_value.read.return_value = json.dumps(mock_rules) # For rules.json
            
            with patch("sys.stdin", new_callable=unittest.mock.StringIO) as mock_stdin:
                mock_stdin.read.return_value = mock_input_content # Simulate stdin input
                
                with patch("sys.stdout", new_callable=unittest.mock.StringIO) as mock_stdout:
                    with patch("sys.argv", ["rectifier.py", "-r", "rules.json"]):
                        main()
                    self.assertEqual(mock_stdout.getvalue(), expected_output_content)
            
            m_open.assert_called_once_with("rules.json", "r", encoding="utf-8") # Only rules file opened

    def test_main_cli_rules_file_not_found(self):
        # Mock rationale: Simulate `FileNotFoundError` when trying to open the rules file.
        with patch("builtins.open", side_effect=FileNotFoundError) as m_open:
            with patch("sys.stderr", new_callable=unittest.mock.StringIO) as mock_stderr:
                with patch("sys.argv", ["rectifier.py", "-r", "non_existent_rules.json"]):
                    with self.assertRaises(SystemExit) as cm:
                        main()
                    self.assertEqual(cm.exception.code, 1)
                    self.assertIn("Error: Rules file not found", mock_stderr.getvalue())

    def test_main_cli_invalid_json_rules(self):
        # Mock rationale: Simulate `json.JSONDecodeError` when loading rules.
        with patch("builtins.open", mock_open(read_data="invalid json")) as m_open:
            with patch("sys.stderr", new_callable=unittest.mock.StringIO) as mock_stderr:
                with patch("sys.argv", ["rectifier.py", "-r", "invalid_rules.json"]):
                    with self.assertRaises(SystemExit) as cm:
                        main()
                    self.assertEqual(cm.exception.code, 1)
                    self.assertIn("Error: Invalid JSON in rules file", mock_stderr.getvalue())

    def test_main_cli_input_file_not_found(self):
        mock_rules = [{"type": "trim"}]
        # Mock rationale: Simulate `FileNotFoundError` for the input file, after successfully loading rules.
        with patch("builtins.open", new_callable=mock_open) as m_open:
            m_open.side_effect = [
                unittest.mock.mock_open(read_data=json.dumps(mock_rules)).return_value, # For rules.json
                FileNotFoundError # For input.txt
            ]
            with patch("sys.stderr", new_callable=unittest.mock.StringIO) as mock_stderr:
                with patch("sys.argv", ["rectifier.py", "-i", "non_existent_input.txt", "-r", "rules.json"]):
                    with self.assertRaises(SystemExit) as cm:
                        main()
                    self.assertEqual(cm.exception.code, 1)
                    self.assertIn("Error: Input file not found", mock_stderr.getvalue())

    def test_main_cli_output_file_io_error(self):
        mock_rules = [{"type": "trim"}]
        mock_input_content = "  hello world  \n"
        # Mock rationale: Simulate an `IOError` when trying to write to the output file.
        with patch("builtins.open", new_callable=mock_open) as m_open:
            m_open.side_effect = [
                unittest.mock.mock_open(read_data=json.dumps(mock_rules)).return_value, # For rules.json
                unittest.mock.mock_open(read_data=mock_input_content).return_value,    # For input.txt
                unittest.mock.mock_open(side_effect=IOError("Permission denied")).return_value # For output.txt
            ]
            with patch("sys.stderr", new_callable=unittest.mock.StringIO) as mock_stderr:
                with patch("sys.argv", ["rectifier.py", "-i", "input.txt", "-r", "rules.json", "-o", "output.txt"]):
                    with self.assertRaises(SystemExit) as cm:
                        main()
                    self.assertEqual(cm.exception.code, 1)
                    self.assertIn("Error writing to output file", mock_stderr.getvalue())

    def test_main_cli_error_in_rectify_string_continues(self):
        mock_rules = [
            {"type": "trim"},
            {"type": "unknown_type"}, # This will cause a ValueError
            {"type": "lower"}
        ]
        mock_input_content = "  GOOD LINE  \n  BAD LINE  \n"
        # Expected: GOOD LINE is trimmed, then error on unknown_type. BAD LINE is also processed.
        # The `rectify_string` will raise ValueError, but `main` should catch and print error, then continue.
        # The line with error should be outputted as original.
        expected_output_content = "  GOOD LINE  \n  BAD LINE  \n" # Original lines are kept if error occurs

        with patch("builtins.open", new_callable=mock_open) as m_open:
            m_open.side_effect = [
                unittest.mock.mock_open(read_data=json.dumps(mock_rules)).return_value, # For rules.json
                unittest.mock.mock_open(read_data=mock_input_content).return_value,    # For input.txt
                unittest.mock.mock_open().return_value                                 # For output.txt
            ]
            with patch("sys.stderr", new_callable=unittest.mock.StringIO) as mock_stderr:
                with patch("sys.argv", ["rectifier.py", "-i", "input.txt", "-r", "rules.json", "-o", "output.txt"]):
                    main() # Should not exit, but print error to stderr
            
            output_handle = m_open().write
            output_handle.assert_called_once_with(expected_output_content)
            self.assertIn("Error applying rule to line 'GOOD LINE': Unknown rectification rule type: unknown_type", mock_stderr.getvalue())
            self.assertIn("Error applying rule to line 'BAD LINE': Unknown rectification rule type: unknown_type", mock_stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
