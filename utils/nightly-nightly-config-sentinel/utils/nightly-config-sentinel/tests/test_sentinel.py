import unittest
import os
import tempfile
from unittest.mock import patch
from src.sentinel import check_config, parse_env_file, main

class TestConfigSentinel(unittest.TestCase):

    def setUp(self):
        # Mock rationale: We need to create temporary .env files for testing
        # without affecting the actual file system or requiring manual cleanup.
        # tempfile.mkstemp handles creation and os.remove is called in tearDown.
        self.temp_files = []

    def tearDown(self):
        for f in self.temp_files:
            if os.path.exists(f):
                os.remove(f)

    def _create_temp_env_file(self, content: str) -> str:
        """Helper to create a temporary .env file."""
        fd, path = tempfile.mkstemp(suffix=".env")
        with os.fdopen(fd, 'w') as tmp:
            tmp.write(content)
        self.temp_files.append(path)
        return path

    def test_parse_env_file_basic(self):
        content = "KEY1=value1\nKEY2=value2\n#COMMENT=ignored"
        filepath = self._create_temp_env_file(content)
        config = parse_env_file(filepath)
        self.assertEqual(config, {"KEY1": "value1", "KEY2": "value2"})

    def test_parse_env_file_empty_lines_and_whitespace(self):
        content = "\nKEY1 = value1 \n\n  KEY2=value2\n"
        filepath = self._create_temp_env_file(content)
        config = parse_env_file(filepath)
        self.assertEqual(config, {"KEY1": "value1", "KEY2": "value2"})

    def test_parse_env_file_non_existent(self):
        # Mock rationale: Testing the behavior when the file doesn't exist.
        # No actual file creation is needed, just a non-existent path.
        config = parse_env_file("/non/existent/path/.env")
        self.assertEqual(config, {})

    def test_check_config_no_issues(self):
        content = "DEBUG=False\nAPI_KEY=some_value\nNORMAL_VAR=hello"
        filepath = self._create_temp_env_file(content)
        warnings = check_config(filepath)
        self.assertEqual(warnings, [])

    def test_check_config_debug_true(self):
        content = "DEBUG=True\nAPI_KEY=some_value"
        filepath = self._create_temp_env_file(content)
        warnings = check_config(filepath)
        self.assertIn("[WARNING] Found 'DEBUG=True'. This is often unsafe for production environments.", warnings)
        self.assertEqual(len(warnings), 1)

    def test_check_config_empty_api_key(self):
        content = "DEBUG=False\nAPI_KEY=\nSECRET_KEY=  "
        filepath = self._create_temp_env_file(content)
        warnings = check_config(filepath)
        self.assertIn("[WARNING] Sensitive variable 'API_KEY' has an empty or whitespace-only value.", warnings)
        self.assertIn("[WARNING] Sensitive variable 'SECRET_KEY' has an empty or whitespace-only value.", warnings)
        self.assertEqual(len(warnings), 2)

    def test_check_config_mixed_issues(self):
        content = "DEBUG=True\nAPI_KEY=\nDB_PASSWORD=  \nNORMAL_VAR=ok"
        filepath = self._create_temp_env_file(content)
        warnings = check_config(filepath)
        self.assertIn("[WARNING] Found 'DEBUG=True'. This is often unsafe for production environments.", warnings)
        self.assertIn("[WARNING] Sensitive variable 'API_KEY' has an empty or whitespace-only value.", warnings)
        self.assertIn("[WARNING] Sensitive variable 'DB_PASSWORD' has an empty or whitespace-only value.", warnings)
        self.assertEqual(len(warnings), 3)

    def test_check_config_file_not_found(self):
        # Mock rationale: Testing the behavior when the file doesn't exist.
        # No actual file creation is needed, just a non-existent path.
        filepath = "/non/existent/path/.env"
        warnings = check_config(filepath)
        self.assertIn(f"[ERROR] Configuration file '{filepath}' not found.", warnings)
        self.assertEqual(len(warnings), 1)

    def test_check_config_empty_file(self):
        content = ""
        filepath = self._create_temp_env_file(content)
        warnings = check_config(filepath)
        self.assertIn(f"[INFO] No key-value pairs found in '{filepath}'.", warnings)
        self.assertEqual(len(warnings), 1)

    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_issues(self, mock_parse_args, mock_print):
        # Mock rationale: We need to simulate command-line arguments and capture print output.
        # mock_parse_args simulates the CLI input.
        # mock_print captures what would be printed to stdout.
        mock_parse_args.return_value.file = self._create_temp_env_file("DEBUG=False\nAPI_KEY=valid")
        main()
        mock_print.assert_any_call("[INFO] No issues found. Configuration looks good!")

    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_issues(self, mock_parse_args, mock_print):
        # Mock rationale: Simulate CLI arguments and capture print output for a file with issues.
        mock_parse_args.return_value.file = self._create_temp_env_file("DEBUG=True\nAPI_KEY=")
        main()
        mock_print.assert_any_call("[WARNING] Found 'DEBUG=True'. This is often unsafe for production environments.")
        mock_print.assert_any_call("[WARNING] Sensitive variable 'API_KEY' has an empty or whitespace-only value.")

    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_file_not_found(self, mock_parse_args, mock_print):
        # Mock rationale: Simulate CLI arguments and capture print output for a non-existent file.
        non_existent_path = "/non/existent/path/for_main/.env"
        mock_parse_args.return_value.file = non_existent_path
        main()
        mock_print.assert_any_call(f"[ERROR] Configuration file '{non_existent_path}' not found.")


if __name__ == '__main__':
    unittest.main()
