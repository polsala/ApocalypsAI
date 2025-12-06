import unittest
from unittest.mock import patch, mock_open
import sys
import os

# Mock PyYAML if it's not installed to ensure tests run offline and deterministically
try:
    import yaml
except ImportError:
    sys.modules['yaml'] = unittest.mock.MagicMock()
    sys.modules['yaml'].YAMLError = Exception # Define YAMLError for error handling
    sys.modules['yaml'].safe_load = unittest.mock.MagicMock(side_effect=ImportError("PyYAML not installed"))

# Import the validator module after potential yaml mock
# Adjust path for import if necessary, assuming src/validator.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from validator import load_config, validate_config, HAS_YAML
sys.path.pop(0)

class TestConfigValidator(unittest.TestCase):

    def setUp(self):
        # Store original HAS_YAML state and set to False for tests unless specifically enabled.
        # Mock rationale: Ensure HAS_YAML reflects the test environment, not actual system state.
        # This allows testing the 'PyYAML not installed' scenario deterministically.
        self._original_HAS_YAML = HAS_YAML
        global HAS_YAML
        HAS_YAML = False # Default to no PyYAML for test isolation

    def tearDown(self):
        # Restore original HAS_YAML state after each test.
        global HAS_YAML
        HAS_YAML = self._original_HAS_YAML

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_json_success(self, mock_file, mock_exists):
        # Mock rationale: Simulate file existence and content for a valid JSON file.
        config, error = load_config('test.json')
        self.assertIsNotNone(config)
        self.assertIsNone(error)
        self.assertEqual(config, {'key': 'value'})

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    def test_load_json_invalid_syntax(self, mock_file, mock_exists):
        # Mock rationale: Simulate file existence and content for an invalid JSON file.
        config, error = load_config('test.json')
        self.assertIsNone(config)
        self.assertIsNotNone(error)
        self.assertIn('Invalid JSON syntax', error)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='key: value')
    def test_load_yaml_success_with_mocked_yaml(self, mock_file, mock_exists):
        # Mock rationale: Simulate PyYAML being installed and successfully parsing YAML.
        # Temporarily enable HAS_YAML and mock yaml.safe_load for this test.
        global HAS_YAML
        HAS_YAML = True
        sys.modules['yaml'].safe_load.return_value = {'key': 'value'}

        config, error = load_config('test.yaml')
        self.assertIsNotNone(config)
        self.assertIsNone(error)
        self.assertEqual(config, {'key': 'value'})
        sys.modules['yaml'].safe_load.assert_called_once_with('key: value')

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='- invalid\n  yaml:')
    def test_load_yaml_invalid_syntax_with_mocked_yaml(self, mock_file, mock_exists):
        # Mock rationale: Simulate PyYAML being installed but failing to parse invalid YAML.
        # Temporarily enable HAS_YAML and mock yaml.safe_load to raise YAMLError.
        global HAS_YAML
        HAS_YAML = True
        sys.modules['yaml'].safe_load.side_effect = yaml.YAMLError("mocked YAML error")

        config, error = load_config('test.yaml')
        self.assertIsNone(config)
        self.assertIsNotNone(error)
        self.assertIn('Invalid YAML syntax', error)
        sys.modules['yaml'].safe_load.assert_called_once_with('- invalid\n  yaml:')

    @patch('os.path.exists', return_value=False)
    def test_load_file_not_found(self, mock_exists):
        # Mock rationale: Simulate a non-existent file.
        config, error = load_config('nonexistent.json')
        self.assertIsNone(config)
        self.assertIsNotNone(error)
        self.assertIn('File not found', error)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    def test_validate_json_success_no_required_keys(self, mock_file, mock_exists):
        # Mock rationale: Simulate a valid JSON file with no specific key requirements.
        is_valid, message = validate_config('test.json')
        self.assertTrue(is_valid)
        self.assertIn('valid', message)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value", "another": 123}')
    def test_validate_json_success_with_required_keys(self, mock_file, mock_exists):
        # Mock rationale: Simulate a valid JSON file with all required keys present.
        is_valid, message = validate_config('test.json', required_keys=['key', 'another'])
        self.assertTrue(is_valid)
        self.assertIn('valid', message)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    def test_validate_json_missing_required_key(self, mock_file, mock_exists):
        # Mock rationale: Simulate a JSON file missing a required key.
        is_valid, message = validate_config('test.json', required_keys=['missing_key'])
        self.assertFalse(is_valid)
        self.assertIn('Missing required keys: missing_key', message)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='"just_a_string"')
    def test_validate_json_not_dict_root(self, mock_file, mock_exists):
        # Mock rationale: Simulate a JSON file whose root is not a dictionary.
        is_valid, message = validate_config('test.json')
        self.assertFalse(is_valid)
        self.assertIn('must contain a dictionary at its root', message)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_validate_empty_file(self, mock_file, mock_exists):
        # Mock rationale: Simulate an empty file.
        is_valid, message = validate_config('empty.json')
        self.assertFalse(is_valid)
        self.assertIn('is empty or could not be parsed', message)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='key: value')
    def test_validate_yaml_with_json_type_hint(self, mock_file, mock_exists):
        # Mock rationale: Simulate a YAML file being incorrectly parsed as JSON.
        is_valid, message = validate_config('test.yaml', config_type='json')
        self.assertFalse(is_valid)
        self.assertIn('Invalid JSON syntax', message)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    def test_validate_json_with_yaml_type_hint_no_pyyaml(self, mock_file, mock_exists):
        # Mock rationale: Simulate a JSON file being incorrectly parsed as YAML, with PyYAML not installed.
        # HAS_YAML is False by default in setUp.
        is_valid, message = validate_config('test.json', config_type='yaml')
        self.assertFalse(is_valid)
        self.assertIn('PyYAML not installed', message)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='key: value')
    def test_validate_yaml_no_pyyaml_installed(self, mock_file, mock_exists):
        # Mock rationale: Simulate a scenario where PyYAML is not installed.
        # HAS_YAML is False by default in setUp.
        is_valid, message = validate_config('test.yaml', config_type='yaml')
        self.assertFalse(is_valid)
        self.assertIn('PyYAML not installed', message)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='some_plain_text')
    def test_load_config_unknown_type(self, mock_file, mock_exists):
        # Mock rationale: Simulate a file with an unknown extension and no type hint.
        config, error = load_config('test.txt')
        self.assertIsNone(config)
        self.assertIsNotNone(error)
        self.assertIn('Could not determine config type', error)
