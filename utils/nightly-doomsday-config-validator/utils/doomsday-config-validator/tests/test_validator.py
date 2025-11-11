import unittest
from unittest.mock import patch, mock_open
import sys
import os

# Add the src directory to the Python path to allow importing validator.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from validator import validate_yaml_string, validate_json_string, validate_file, main

class TestConfigValidator(unittest.TestCase):

    # --- Core String Validation Tests ---

    def test_valid_yaml_string(self):
        valid_yaml = """
        server:
          port: 8080
          host: 127.0.0.1
        """
        is_valid, message = validate_yaml_string(valid_yaml)
        self.assertTrue(is_valid)
        self.assertIn("pristine", message)

    def test_invalid_yaml_string(self):
        invalid_yaml = """
        server:
          port: 8080
        host: 127.0.0.1:
        - item1
        - item2
        """ # Indentation error and colon after host
        is_valid, message = validate_yaml_string(invalid_yaml)
        self.assertFalse(is_valid)
        self.assertIn("YAML syntax error", message)

    def test_valid_json_string(self):
        valid_json = '{"name": "ApocalypsAI", "version": 1.0}'
        is_valid, message = validate_json_string(valid_json)
        self.assertTrue(is_valid)
        self.assertIn("pristine", message)

    def test_invalid_json_string(self):
        invalid_json = '{"name": "ApocalypsAI", "version": 1.0,}' # Trailing comma
        is_valid, message = validate_json_string(invalid_json)
        self.assertFalse(is_valid)
        self.assertIn("JSON syntax error", message)

    def test_empty_yaml_string(self):
        is_valid, message = validate_yaml_string("")
        self.assertTrue(is_valid) # Empty YAML is valid

    def test_empty_json_string(self):
        is_valid, message = validate_json_string("")
        self.assertFalse(is_valid) # Empty JSON is not valid
        self.assertIn("JSON syntax error", message)

    # --- File Validation Tests (with mocks) ---

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.splitext')
    def test_validate_yaml_file_success(self, mock_splitext, mock_file, mock_exists):
        # Mock rationale: Simulate file existence and content for YAML validation.
        mock_exists.return_value = True
        mock_splitext.return_value = ('config', '.yaml')
        mock_file.return_value.read.return_value = "key: value\nlist:\n  - item1"

        is_valid, message = validate_file('config.yaml')
        self.assertTrue(is_valid)
        self.assertIn("pristine", message)
        mock_exists.assert_called_once_with('config.yaml')
        mock_file.assert_called_once_with('config.yaml', 'r', encoding='utf-8')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.splitext')
    def test_validate_json_file_success(self, mock_splitext, mock_file, mock_exists):
        # Mock rationale: Simulate file existence and content for JSON validation.
        mock_exists.return_value = True
        mock_splitext.return_value = ('data', '.json')
        mock_file.return_value.read.return_value = '{"data": [1, 2, 3]}'

        is_valid, message = validate_file('data.json')
        self.assertTrue(is_valid)
        self.assertIn("pristine", message)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.splitext')
    def test_validate_yaml_file_failure(self, mock_splitext, mock_file, mock_exists):
        # Mock rationale: Simulate file existence and invalid YAML content.
        mock_exists.return_value = True
        mock_splitext.return_value = ('bad_config', '.yml')
        mock_file.return_value.read.return_value = "key: value\n  - bad_indent"

        is_valid, message = validate_file('bad_config.yml')
        self.assertFalse(is_valid)
        self.assertIn("YAML syntax error", message)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.splitext')
    def test_validate_json_file_failure(self, mock_splitext, mock_file, mock_exists):
        # Mock rationale: Simulate file existence and invalid JSON content.
        mock_exists.return_value = True
        mock_splitext.return_value = ('bad_data', '.json')
        mock_file.return_value.read.return_value = '{"data": [1, 2, 3,]}'

        is_valid, message = validate_file('bad_data.json')
        self.assertFalse(is_valid)
        self.assertIn("JSON syntax error", message)

    @patch('os.path.exists')
    def test_validate_file_not_found(self, mock_exists):
        # Mock rationale: Simulate a non-existent file.
        mock_exists.return_value = False

        is_valid, message = validate_file('non_existent.yaml')
        self.assertFalse(is_valid)
        self.assertIn("File not found", message)
        mock_exists.assert_called_once_with('non_existent.yaml')

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.splitext')
    def test_validate_unsupported_file_type(self, mock_splitext, mock_file, mock_exists):
        # Mock rationale: Simulate an unsupported file type (.txt).
        mock_exists.return_value = True
        mock_splitext.return_value = ('document', '.txt')
        mock_file.return_value.read.return_value = "some text"

        is_valid, message = validate_file('document.txt')
        self.assertFalse(is_valid)
        self.assertIn("Unsupported file type", message)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.splitext')
    def test_validate_file_read_error(self, mock_splitext, mock_file, mock_exists):
        # Mock rationale: Simulate an error during file reading.
        mock_exists.return_value = True
        mock_splitext.return_value = ('locked_file', '.yaml')
        mock_file.side_effect = IOError("Permission denied")

        is_valid, message = validate_file('locked_file.yaml')
        self.assertFalse(is_valid)
        self.assertIn("Error reading file: Permission denied", message)

    # --- Main CLI Function Tests (with mocks) ---

    @patch('sys.argv', ['validator.py', 'test.yaml'])
    @patch('sys.exit')
    @patch('builtins.print')
    @patch('validator.validate_file')
    def test_main_success(self, mock_validate_file, mock_print, mock_exit):
        # Mock rationale: Simulate successful file validation via CLI.
        mock_validate_file.return_value = (True, "Syntax is pristine.")
        main()
        mock_print.assert_called_with('test.yaml: OK - Syntax is pristine.')
        mock_exit.assert_called_once_with(0)

    @patch('sys.argv', ['validator.py', 'bad.json'])
    @patch('sys.exit')
    @patch('builtins.print')
    @patch('validator.validate_file')
    def test_main_failure(self, mock_validate_file, mock_print, mock_exit):
        # Mock rationale: Simulate failed file validation via CLI.
        mock_validate_file.return_value = (False, "JSON syntax error.")
        main()
        mock_print.assert_called_with('bad.json: ERROR - JSON syntax error.')
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['validator.py'])
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_no_args(self, mock_print, mock_exit):
        # Mock rationale: Simulate running CLI without arguments.
        main()
        mock_print.assert_called_with('Usage: python src/validator.py <path_to_config_file>', file=sys.stderr)
        mock_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
