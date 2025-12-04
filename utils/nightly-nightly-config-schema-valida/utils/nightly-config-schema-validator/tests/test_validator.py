import unittest
from unittest import mock
import sys
import io
import os

# Mock rationale: We need to test the script's behavior without actually touching the filesystem
# or executing sys.exit, which would terminate the test runner. Mocking `open` allows us to
# simulate file content, and mocking `sys.exit` and `sys.stdout`/`sys.stderr` allows us to
# capture output and exit codes for deterministic, offline testing.

# Add src directory to sys.path to allow importing validator.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import validator as config_validator

class TestConfigValidator(unittest.TestCase):

    def setUp(self):
        # Store original sys.argv to restore after tests
        self._original_argv = sys.argv
        # Reset sys.argv for each test to avoid interference from previous runs
        sys.argv = ['validator.py']

    def tearDown(self):
        # Restore original sys.argv
        sys.argv = self._original_argv

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_load_file_yaml(self, mock_open):
        mock_open.return_value.read.return_value = "key: value\nlist:\n  - item1"
        data = config_validator.load_file('config.yaml')
        self.assertEqual(data, {'key': 'value', 'list': ['item1']})
        mock_open.assert_called_once_with('config.yaml', 'r', encoding='utf-8')

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_load_file_json(self, mock_open):
        mock_open.return_value.read.return_value = '{"key": "value", "list": ["item1"]}'
        data = config_validator.load_file('config.json')
        self.assertEqual(data, {'key': 'value', 'list': ['item1']})
        mock_open.assert_called_once_with('config.json', 'r', encoding='utf-8')

    @mock.patch('builtins.open', side_effect=FileNotFoundError)
    @mock.patch('sys.stderr', new_callable=io.StringIO)
    @mock.patch('sys.exit')
    def test_load_file_not_found(self, mock_exit, mock_stderr, mock_open):
        config_validator.load_file('non_existent.yaml')
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: File not found at non_existent.yaml", mock_stderr.getvalue())

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('sys.stderr', new_callable=io.StringIO)
    @mock.patch('sys.exit')
    def test_load_file_malformed_yaml(self, mock_exit, mock_stderr, mock_open):
        mock_open.return_value.read.return_value = "key: - value\n  - item1" # Invalid YAML syntax
        config_validator.load_file('malformed.yaml')
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Malformed file malformed.yaml", mock_stderr.getvalue())

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('sys.stderr', new_callable=io.StringIO)
    @mock.patch('sys.exit')
    def test_load_file_malformed_json(self, mock_exit, mock_stderr, mock_open):
        mock_open.return_value.read.return_value = '{"key": "value", "list": ["item1"' # Invalid JSON syntax
        config_validator.load_file('malformed.json')
        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: Malformed file malformed.json", mock_stderr.getvalue())

    def test_validate_config_valid(self):
        config_data = {'name': 'test', 'version': 1}
        schema_data = {'type': 'object', 'properties': {'name': {'type': 'string'}, 'version': {'type': 'integer'}}, 'required': ['name', 'version']}
        is_valid, error = config_validator.validate_config(config_data, schema_data)
        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_config_invalid_missing_field(self):
        config_data = {'name': 'test'}
        schema_data = {'type': 'object', 'properties': {'name': {'type': 'string'}, 'version': {'type': 'integer'}}, 'required': ['name', 'version']}
        is_valid, error = config_validator.validate_config(config_data, schema_data)
        self.assertFalse(is_valid)
        self.assertIsInstance(error, config_validator.ValidationError)
        self.assertIn("'version' is a required property", str(error))

    def test_validate_config_invalid_type(self):
        config_data = {'name': 'test', 'version': 'one'}
        schema_data = {'type': 'object', 'properties': {'name': {'type': 'string'}, 'version': {'type': 'integer'}}, 'required': ['name', 'version']}
        is_valid, error = config_validator.validate_config(config_data, schema_data)
        self.assertFalse(is_valid)
        self.assertIsInstance(error, config_validator.ValidationError)
        self.assertIn("'one' is not of type 'integer'", str(error))

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('sys.stderr', new_callable=io.StringIO)
    @mock.patch('sys.exit')
    def test_cli_success(self, mock_exit, mock_stderr, mock_stdout, mock_open):
        # Mock config and schema files content
        mock_open.side_effect = [
            mock.mock_open(read_data='key: value').return_value, # config.yaml
            mock.mock_open(read_data='type: object\nproperties:\n  key:\n    type: string\nrequired: [key]').return_value # schema.yaml
        ]
        sys.argv = ['validator.py', '--config', 'config.yaml', '--schema', 'schema.yaml']

        config_validator.main()

        mock_exit.assert_called_once_with(0)
        self.assertIn("✅ Configuration 'config.yaml' is valid", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "") # No errors on stderr for success

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    @mock.patch('sys.stderr', new_callable=io.StringIO)
    @mock.patch('sys.exit')
    def test_cli_failure_validation_error(self, mock_exit, mock_stderr, mock_stdout, mock_open):
        # Mock config and schema files content, with config having an invalid type
        mock_open.side_effect = [
            mock.mock_open(read_data='key: 123').return_value, # config.yaml (invalid type)
            mock.mock_open(read_data='type: object\nproperties:\n  key:\n    type: string\nrequired: [key]').return_value # schema.yaml
        ]
        sys.argv = ['validator.py', '--config', 'config.yaml', '--schema', 'schema.yaml']

        config_validator.main()

        mock_exit.assert_called_once_with(1)
        self.assertIn("❌ Configuration 'config.yaml' failed validation", mock_stderr.getvalue())
        self.assertIn("123 is not of type 'string'", mock_stderr.getvalue())
        self.assertEqual(mock_stdout.getvalue(), "") # No success message on stdout for failure

    @mock.patch('builtins.open', side_effect=[FileNotFoundError('config.yaml'), mock.mock_open(read_data='{}').return_value])
    @mock.patch('sys.stderr', new_callable=io.StringIO)
    @mock.patch('sys.exit')
    def test_cli_failure_config_not_found(self, mock_exit, mock_stderr, mock_open):
        sys.argv = ['validator.py', '--config', 'config.yaml', '--schema', 'schema.yaml']

        config_validator.main()

        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: File not found at config.yaml", mock_stderr.getvalue())

    @mock.patch('builtins.open', side_effect=[mock.mock_open(read_data='key: value').return_value, FileNotFoundError('schema.yaml')])
    @mock.patch('sys.stderr', new_callable=io.StringIO)
    @mock.patch('sys.exit')
    def test_cli_failure_schema_not_found(self, mock_exit, mock_stderr, mock_open):
        sys.argv = ['validator.py', '--config', 'config.yaml', '--schema', 'schema.yaml']

        config_validator.main()

        mock_exit.assert_called_once_with(1)
        self.assertIn("Error: File not found at schema.yaml", mock_stderr.getvalue())

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('sys.stderr', new_callable=io.StringIO)
    @mock.patch('sys.exit')
    def test_cli_failure_unsupported_file_type(self, mock_exit, mock_stderr, mock_open):
        # Mock config file with unsupported extension
        mock_open.side_effect = [
            mock.mock_open(read_data='content').return_value, # config.txt
            mock.mock_open(read_data='{}').return_value # schema.json
        ]
        sys.argv = ['validator.py', '--config', 'config.txt', '--schema', 'schema.json']

        config_validator.main()

        mock_exit.assert_called_once_with(1)
        self.assertIn("Unsupported file type for config.txt", mock_stderr.getvalue())


if __name__ == '__main__':
    unittest.main()
