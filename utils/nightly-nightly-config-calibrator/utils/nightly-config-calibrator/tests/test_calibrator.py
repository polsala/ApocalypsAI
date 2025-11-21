import unittest
import os
from unittest.mock import patch, mock_open
from io import StringIO
import sys

# Adjust sys.path to allow importing from the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from calibrator import get_keys_from_file, calibrate_config, main

class TestCalibrator(unittest.TestCase):

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_keys_from_file_env_style(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate file existence and content without actual file I/O.
        mock_exists.return_value = True
        mock_file_open.return_value = StringIO(
            "API_KEY=123\n"
            "DATABASE_URL=postgres://...\n"
            "# This is a comment\n"
            "DEBUG=True\n"
            "\n" # Empty line
            "ANOTHER_KEY=" # Key with empty value
        )
        keys = get_keys_from_file("dummy_config.env")
        self.assertEqual(keys, {"API_KEY", "DATABASE_URL", "DEBUG", "ANOTHER_KEY"})

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_keys_from_file_template_style(self, mock_file_open, mock_exists):
        # Mock rationale: Simulate file existence and content without actual file I/O.
        mock_exists.return_value = True
        mock_file_open.return_value = StringIO(
            "API_KEY\n"
            "DATABASE_URL\n"
            "# Commented key\n"
            "LOG_LEVEL\n"
        )
        keys = get_keys_from_file("dummy_template.txt")
        self.assertEqual(keys, {"API_KEY", "DATABASE_URL", "LOG_LEVEL"})

    @patch('os.path.exists')
    def test_get_keys_from_file_not_found(self, mock_exists):
        # Mock rationale: Simulate a non-existent file.
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            get_keys_from_file("non_existent_file.txt")

    @patch('calibrator.get_keys_from_file')
    def test_calibrate_config_all_present(self, mock_get_keys):
        # Mock rationale: Control the output of get_keys_from_file to test calibration logic directly.
        mock_get_keys.side_effect = [
            {"API_KEY", "DATABASE_URL", "DEBUG"},  # config_keys
            {"API_KEY", "DATABASE_URL"}             # template_keys
        ]
        missing = calibrate_config("config.env", "template.txt")
        self.assertEqual(missing, [])

    @patch('calibrator.get_keys_from_file')
    def test_calibrate_config_missing_keys(self, mock_get_keys):
        # Mock rationale: Control the output of get_keys_from_file to test calibration logic directly.
        mock_get_keys.side_effect = [
            {"API_KEY", "DATABASE_URL"},            # config_keys
            {"API_KEY", "DATABASE_URL", "LOG_LEVEL", "PORT"} # template_keys
        ]
        missing = calibrate_config("config.env", "template.txt")
        self.assertEqual(missing, ["LOG_LEVEL", "PORT"]) # Sorted list

    @patch('calibrator.get_keys_from_file')
    def test_calibrate_config_empty_config(self, mock_get_keys):
        # Mock rationale: Control the output of get_keys_from_file to test calibration logic directly.
        mock_get_keys.side_effect = [
            set(),                                  # config_keys (empty)
            {"API_KEY", "DATABASE_URL"}             # template_keys
        ]
        missing = calibrate_config("empty_config.env", "template.txt")
        self.assertEqual(missing, ["API_KEY", "DATABASE_URL"])

    @patch('calibrator.get_keys_from_file')
    def test_calibrate_config_empty_template(self, mock_get_keys):
        # Mock rationale: Control the output of get_keys_from_file to test calibration logic directly.
        mock_get_keys.side_effect = [
            {"API_KEY", "DATABASE_URL"},            # config_keys
            set()                                   # template_keys (empty)
        ]
        missing = calibrate_config("config.env", "empty_template.txt")
        self.assertEqual(missing, [])

    @patch('calibrator.get_keys_from_file')
    def test_calibrate_config_file_not_found_error(self, mock_get_keys):
        # Mock rationale: Simulate FileNotFoundError from get_keys_from_file.
        mock_get_keys.side_effect = FileNotFoundError("File not found: non_existent.txt")
        
        with self.assertRaises(FileNotFoundError) as cm:
            calibrate_config("non_existent.txt", "template.txt")
        self.assertIn("File not found: non_existent.txt", str(cm.exception))
        mock_get_keys.assert_called_once() # It will be called for config_path, then raise.

    @patch('argparse.ArgumentParser.parse_args')
    @patch('calibrator.calibrate_config')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_success(self, mock_exit, mock_stderr, mock_stdout, mock_parse_args, mock_calibrate_config):
        # Mock rationale: Simulate CLI arguments, calibrate_config output, and capture stdout/exit.
        mock_parse_args.return_value.config = "config.env"
        mock_parse_args.return_value.template = "template.txt"
        mock_calibrate_config.return_value = []

        main()
        mock_calibrate_config.assert_called_once_with("config.env", "template.txt")
        self.assertIn("Configuration calibrated successfully. All required keys are present.", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(0)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('calibrator.calibrate_config')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_failure_missing_keys(self, mock_exit, mock_stderr, mock_stdout, mock_parse_args, mock_calibrate_config):
        # Mock rationale: Simulate CLI arguments, calibrate_config output with missing keys, and capture stdout/exit.
        mock_parse_args.return_value.config = "config.env"
        mock_parse_args.return_value.template = "template.txt"
        mock_calibrate_config.return_value = ["LOG_LEVEL", "PORT"]

        main()
        mock_calibrate_config.assert_called_once_with("config.env", "template.txt")
        self.assertIn("Missing required keys: ['LOG_LEVEL', 'PORT']", mock_stdout.getvalue())
        self.assertIn("Configuration requires calibration!", mock_stdout.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('calibrator.calibrate_config')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_file_not_found_error_handled(self, mock_exit, mock_stderr, mock_stdout, mock_parse_args, mock_calibrate_config):
        # Mock rationale: Simulate CLI arguments and a FileNotFoundError from calibrate_config.
        mock_parse_args.return_value.config = "non_existent.env"
        mock_parse_args.return_value.template = "template.txt"
        mock_calibrate_config.side_effect = FileNotFoundError("File not found: non_existent.env")
        
        main()
        mock_calibrate_config.assert_called_once_with("non_existent.env", "template.txt")
        self.assertIn("Error: File not found: non_existent.env", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
