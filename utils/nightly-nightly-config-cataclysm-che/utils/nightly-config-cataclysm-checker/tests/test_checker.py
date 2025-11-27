import unittest
import os
import json
import yaml
from unittest.mock import patch, mock_open
from src.checker import ConfigCataclysmChecker

class TestConfigCataclysmChecker(unittest.TestCase):

    def setUp(self):
        # Define a base config spec for testing
        self.base_spec_content = json.dumps({
            "files": [
                {"path": "/app/config.json", "required": True, "type": "json"},
                {"path": "/app/data/", "required": True, "type": "directory"},
                {"path": "/app/optional.txt", "required": False, "type": "file"},
                {"path": "/app/settings.yaml", "required": True, "type": "yaml"}
            ],
            "env_vars": [
                {"name": "API_KEY", "required": True, "type": "string"},
                {"name": "DEBUG_MODE", "required": False, "type": "boolean"},
                {"name": "MAX_RETRIES", "required": True, "type": "int"}
            ]
        })
        self.spec_path = "/tmp/config_spec.json"

    def _create_checker_and_run(self, spec_content, fs_mock_data, env_mock_data):
        with mock_open(read_data=spec_content) as m_open_spec,
             patch('os.path.exists', side_effect=lambda p: p == self.spec_path or p in fs_mock_data),
             patch('os.path.isdir', side_effect=lambda p: fs_mock_data.get(p) == 'directory'),
             patch('os.path.isfile', side_effect=lambda p: p in fs_mock_data and fs_mock_data.get(p) != 'directory'),
             patch('builtins.open', side_effect=lambda p, mode='r', encoding=None: m_open_spec if p == self.spec_path else mock_open(read_data=fs_mock_data.get(p, '')).return_value),
             patch.dict(os.environ, env_mock_data, clear=True): # Mock rationale: Isolate environment variables for deterministic tests.
            
            checker = ConfigCataclysmChecker(self.spec_path)
            result = checker.run_checks()
            return result, checker.get_errors()

    def test_all_present_and_valid(self):
        # Mock rationale: Simulate a file system and environment where all required items are present and valid.
        fs_mock_data = {
            "/app/config.json": '{"key": "value"}',
            "/app/data/": "directory",
            "/app/optional.txt": "some content",
            "/app/settings.yaml": "setting: value"
        }
        env_mock_data = {
            "API_KEY": "abc123",
            "DEBUG_MODE": "true",
            "MAX_RETRIES": "5"
        }
        result, errors = self._create_checker_and_run(self.base_spec_content, fs_mock_data, env_mock_data)
        self.assertTrue(result)
        self.assertEqual(len(errors), 0)

    def test_missing_required_file(self):
        # Mock rationale: Simulate a file system where a required file is missing.
        fs_mock_data = {
            # "/app/config.json" is missing
            "/app/data/": "directory",
            "/app/settings.yaml": "setting: value"
        }
        env_mock_data = {
            "API_KEY": "abc123",
            "MAX_RETRIES": "5"
        }
        result, errors = self._create_checker_and_run(self.base_spec_content, fs_mock_data, env_mock_data)
        self.assertFalse(result)
        self.assertIn("MISSING: Required json '/app/config.json' does not exist.", errors)
        self.assertEqual(len(errors), 1)

    def test_missing_required_env_var(self):
        # Mock rationale: Simulate an environment where a required environment variable is missing.
        fs_mock_data = {
            "/app/config.json": '{"key": "value"}',
            "/app/data/": "directory",
            "/app/settings.yaml": "setting: value"
        }
        env_mock_data = {
            "API_KEY": "abc123",
            # "MAX_RETRIES" is missing
        }
        result, errors = self._create_checker_and_run(self.base_spec_content, fs_mock_data, env_mock_data)
        self.assertFalse(result)
        self.assertIn("MISSING: Required environment variable 'MAX_RETRIES' is not set.", errors)
        self.assertEqual(len(errors), 1)

    def test_invalid_json_file(self):
        # Mock rationale: Simulate a file system where a file expected to be JSON is malformed.
        fs_mock_data = {
            "/app/config.json": '{"key": "value', # Malformed JSON
            "/app/data/": "directory",
            "/app/settings.yaml": "setting: value"
        }
        env_mock_data = {
            "API_KEY": "abc123",
            "MAX_RETRIES": "5"
        }
        result, errors = self._create_checker_and_run(self.base_spec_content, fs_mock_data, env_mock_data)
        self.assertFalse(result)
        self.assertIn("INVALID FORMAT: File '/app/config.json' is not valid JSON.", errors)
        self.assertEqual(len(errors), 1)

    def test_invalid_yaml_file(self):
        # Mock rationale: Simulate a file system where a file expected to be YAML is malformed.
        fs_mock_data = {
            "/app/config.json": '{"key": "value"}',
            "/app/data/": "directory",
            "/app/settings.yaml": "setting: - item1\n  - item2: value" # Malformed YAML (indentation error)
        }
        env_mock_data = {
            "API_KEY": "abc123",
            "MAX_RETRIES": "5"
        }
        result, errors = self._create_checker_and_run(self.base_spec_content, fs_mock_data, env_mock_data)
        self.assertFalse(result)
        self.assertIn("INVALID FORMAT: File '/app/settings.yaml' is not valid YAML.", errors)
        self.assertEqual(len(errors), 1)

    def test_file_is_directory_type_mismatch(self):
        # Mock rationale: Simulate a file system where a path expected to be a directory is a file.
        fs_mock_data = {
            "/app/config.json": '{"key": "value"}',
            "/app/data/": "this is a file, not a directory", # Should be a directory
            "/app/settings.yaml": "setting: value"
        }
        env_mock_data = {
            "API_KEY": "abc123",
            "MAX_RETRIES": "5"
        }
        result, errors = self._create_checker_and_run(self.base_spec_content, fs_mock_data, env_mock_data)
        self.assertFalse(result)
        self.assertIn("TYPE MISMATCH: Expected '/app/data/' to be a directory, but it's not.", errors)
        self.assertEqual(len(errors), 1)

    def test_env_var_int_type_mismatch(self):
        # Mock rationale: Simulate an environment where an environment variable expected to be an integer is not.
        fs_mock_data = {
            "/app/config.json": '{"key": "value"}',
            "/app/data/": "directory",
            "/app/settings.yaml": "setting: value"
        }
        env_mock_data = {
            "API_KEY": "abc123",
            "MAX_RETRIES": "five" # Should be an int
        }
        result, errors = self._create_checker_and_run(self.base_spec_content, fs_mock_data, env_mock_data)
        self.assertFalse(result)
        self.assertIn("TYPE MISMATCH: Environment variable 'MAX_RETRIES' ('five') is not a valid integer.", errors)
        self.assertEqual(len(errors), 1)

    def test_env_var_boolean_type_mismatch(self):
        # Mock rationale: Simulate an environment where an environment variable expected to be a boolean is not.
        fs_mock_data = {
            "/app/config.json": '{"key": "value"}',
            "/app/data/": "directory",
            "/app/settings.yaml": "setting: value"
        }
        env_mock_data = {
            "API_KEY": "abc123",
            "DEBUG_MODE": "maybe", # Should be a boolean
            "MAX_RETRIES": "5"
        }
        result, errors = self._create_checker_and_run(self.base_spec_content, fs_mock_data, env_mock_data)
        self.assertFalse(result)
        self.assertIn("TYPE MISMATCH: Environment variable 'DEBUG_MODE' ('maybe') is not a valid boolean (true/false/1/0).", errors)
        self.assertEqual(len(errors), 1)

    def test_optional_file_missing_no_error(self):
        # Mock rationale: Simulate a file system where an optional file is missing, which should not produce an error.
        fs_mock_data = {
            "/app/config.json": '{"key": "value"}',
            "/app/data/": "directory",
            # "/app/optional.txt" is missing, but it's optional
            "/app/settings.yaml": "setting: value"
        }
        env_mock_data = {
            "API_KEY": "abc123",
            "MAX_RETRIES": "5"
        }
        result, errors = self._create_checker_and_run(self.base_spec_content, fs_mock_data, env_mock_data)
        self.assertTrue(result)
        self.assertEqual(len(errors), 0)

    def test_spec_file_not_found(self):
        # Mock rationale: Simulate the scenario where the configuration specification file itself is missing.
        with patch('os.path.exists', side_effect=lambda p: p != self.spec_path),
             patch.dict(os.environ, {}, clear=True):
            checker = ConfigCataclysmChecker(self.spec_path)
            result = checker.run_checks()
            errors = checker.get_errors()
            self.assertFalse(result)
            self.assertIn(f"Config specification file not found: {self.spec_path}", errors)
            self.assertEqual(len(errors), 1)

    def test_spec_file_invalid_json(self):
        # Mock rationale: Simulate the scenario where the configuration specification file is malformed JSON.
        invalid_spec_content = '{"files": [{"path": "/app/config.json", "required": true, "type": "json"}' # Malformed
        with mock_open(read_data=invalid_spec_content) as m_open_spec,
             patch('os.path.exists', return_value=True),
             patch('builtins.open', return_value=m_open_spec),
             patch.dict(os.environ, {}, clear=True):
            checker = ConfigCataclysmChecker(self.spec_path)
            result = checker.run_checks()
            errors = checker.get_errors()
            self.assertFalse(result)
            self.assertIn(f"INVALID FORMAT: Config specification file '{self.spec_path}' is not valid JSON.", errors)
            self.assertEqual(len(errors), 1)


if __name__ == '__main__':
    unittest.main()
