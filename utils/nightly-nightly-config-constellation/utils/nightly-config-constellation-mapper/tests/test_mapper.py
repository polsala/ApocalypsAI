import unittest
from unittest.mock import patch, mock_open
import os
import sys

# Add the src directory to the path to allow importing mapper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import mapper

class TestConfigConstellationMapper(unittest.TestCase):

    # Mock rationale: Avoid actual file system interaction for deterministic, offline tests.
    # We simulate file system structure and content to test parsing logic.
    mock_files_content = {
        '/test_dir/config1.yaml': 'key_a: value1\nkey_b: value2',
        '/test_dir/subdir/config2.yml': 'key_b: value3\nkey_c: value4', # Test .yml extension
        '/test_dir/other.txt': 'just some text, not a config',
        '/test_dir/invalid.yaml': 'key_a: -\n  - item1', # Invalid YAML structure
        '/test_dir/empty.yaml': '',
        '/test_dir/config_nested.yaml': 'top_key:\n  nested_key: value',
        '/test_dir/config_json.json': '{"json_key": "value"}', # Should be ignored by .yaml extension
        '/test_dir/config3.json': '{"json_key_1": "val1", "json_key_2": "val2"}',
        '/test_dir/subdir/config4.json': '{"json_key_2": "val3", "json_key_3": "val4"}',
        '/test_dir/config_list.yaml': '- item1\n- item2', # YAML list, not dict
    }

    def mock_open_side_effect(self, filepath, mode='r', encoding=None):
        if filepath in self.mock_files_content:
            # Create a mock file handle with the specified content
            mock_file_handle = mock_open(read_data=self.mock_files_content[filepath]).return_value
            return mock_file_handle
        raise FileNotFoundError(f"No such file or directory: '{filepath}'")

    @patch('builtins.open')
    @patch('os.walk')
    def test_empty_directory(self, mock_os_walk, mock_open_builtin):
        mock_os_walk.return_value = []
        result = mapper.map_config_constellation('/empty_dir', '.yaml')
        self.assertEqual(result, {})
        mock_os_walk.assert_called_once_with('/empty_dir')
        mock_open_builtin.assert_not_called()

    @patch('builtins.open')
    @patch('os.walk')
    def test_single_yaml_file_single_key(self, mock_os_walk, mock_open_builtin):
        mock_os_walk.return_value = [
            ('/test_dir', [], ['config1.yaml'])
        ]
        mock_open_builtin.side_effect = self.mock_open_side_effect

        expected_result = {
            'key_a': ['/test_dir/config1.yaml'],
            'key_b': ['/test_dir/config1.yaml']
        }
        result = mapper.map_config_constellation('/test_dir', '.yaml')
        self.assertEqual(result, expected_result)
        mock_open_builtin.assert_any_call('/test_dir/config1.yaml', 'r', encoding='utf-8')

    @patch('builtins.open')
    @patch('os.walk')
    def test_multiple_yaml_files_overlapping_keys(self, mock_os_walk, mock_open_builtin):
        mock_os_walk.return_value = [
            ('/test_dir', ['subdir'], ['config1.yaml', 'other.txt', 'invalid.yaml', 'empty.yaml', 'config_nested.yaml']),
            ('/test_dir/subdir', [], ['config2.yml'])
        ]
        mock_open_builtin.side_effect = self.mock_open_side_effect

        expected_result = {
            'key_a': ['/test_dir/config1.yaml'],
            'key_b': ['/test_dir/config1.yaml', '/test_dir/subdir/config2.yml'],
            'key_c': ['/test_dir/subdir/config2.yml'],
            'top_key': ['/test_dir/config_nested.yaml']
        }
        result = mapper.map_config_constellation('/test_dir', '.yaml')
        self.assertEqual(result, expected_result)
        mock_open_builtin.assert_any_call('/test_dir/config1.yaml', 'r', encoding='utf-8')
        mock_open_builtin.assert_any_call('/test_dir/subdir/config2.yml', 'r', encoding='utf-8')
        mock_open_builtin.assert_any_call('/test_dir/config_nested.yaml', 'r', encoding='utf-8')
        # Ensure other.txt and invalid.yaml were opened but not parsed for keys (or skipped)
        mock_open_builtin.assert_any_call('/test_dir/other.txt', 'r', encoding='utf-8')
        mock_open_builtin.assert_any_call('/test_dir/invalid.yaml', 'r', encoding='utf-8')
        mock_open_builtin.assert_any_call('/test_dir/empty.yaml', 'r', encoding='utf-8')

    @patch('builtins.open')
    @patch('os.walk')
    def test_non_matching_extension_files_ignored(self, mock_os_walk, mock_open_builtin):
        mock_os_walk.return_value = [
            ('/test_dir', [], ['config1.yaml', 'config_json.json'])
        ]
        mock_open_builtin.side_effect = self.mock_open_side_effect

        expected_result = {
            'key_a': ['/test_dir/config1.yaml'],
            'key_b': ['/test_dir/config1.yaml']
        }
        result = mapper.map_config_constellation('/test_dir', '.yaml')
        self.assertEqual(result, expected_result)
        mock_open_builtin.assert_any_call('/test_dir/config1.yaml', 'r', encoding='utf-8')
        # config_json.json should not be opened with .yaml extension
        with self.assertRaises(AssertionError): # This asserts it was NOT called with config_json.json
            mock_open_builtin.assert_any_call('/test_dir/config_json.json', 'r', encoding='utf-8')

    @patch('builtins.open')
    @patch('os.walk')
    def test_invalid_yaml_files_skipped(self, mock_os_walk, mock_open_builtin):
        mock_os_walk.return_value = [
            ('/test_dir', [], ['invalid.yaml', 'config1.yaml'])
        ]
        mock_open_builtin.side_effect = self.mock_open_side_effect

        expected_result = {
            'key_a': ['/test_dir/config1.yaml'],
            'key_b': ['/test_dir/config1.yaml']
        }
        result = mapper.map_config_constellation('/test_dir', '.yaml')
        self.assertEqual(result, expected_result)
        mock_open_builtin.assert_any_call('/test_dir/invalid.yaml', 'r', encoding='utf-8')
        mock_open_builtin.assert_any_call('/test_dir/config1.yaml', 'r', encoding='utf-8')

    @patch('builtins.open')
    @patch('os.walk')
    def test_empty_yaml_file(self, mock_os_walk, mock_open_builtin):
        mock_os_walk.return_value = [
            ('/test_dir', [], ['empty.yaml'])
        ]
        mock_open_builtin.side_effect = self.mock_open_side_effect

        result = mapper.map_config_constellation('/test_dir', '.yaml')
        self.assertEqual(result, {})
        mock_open_builtin.assert_any_call('/test_dir/empty.yaml', 'r', encoding='utf-8')

    @patch('builtins.open')
    @patch('os.walk')
    def test_yaml_file_with_list_root(self, mock_os_walk, mock_open_builtin):
        mock_os_walk.return_value = [
            ('/test_dir', [], ['config_list.yaml'])
        ]
        mock_open_builtin.side_effect = self.mock_open_side_effect

        result = mapper.map_config_constellation('/test_dir', '.yaml')
        self.assertEqual(result, {})
        mock_open_builtin.assert_any_call('/test_dir/config_list.yaml', 'r', encoding='utf-8')

    @patch('builtins.open')
    @patch('os.walk')
    def test_json_files(self, mock_os_walk, mock_open_builtin):
        mock_os_walk.return_value = [
            ('/test_dir', ['subdir'], ['config3.json']),
            ('/test_dir/subdir', [], ['config4.json'])
        ]
        mock_open_builtin.side_effect = self.mock_open_side_effect

        expected_result = {
            'json_key_1': ['/test_dir/config3.json'],
            'json_key_2': ['/test_dir/config3.json', '/test_dir/subdir/config4.json'],
            'json_key_3': ['/test_dir/subdir/config4.json']
        }
        result = mapper.map_config_constellation('/test_dir', '.json')
        self.assertEqual(result, expected_result)
        mock_open_builtin.assert_any_call('/test_dir/config3.json', 'r', encoding='utf-8')
        mock_open_builtin.assert_any_call('/test_dir/subdir/config4.json', 'r', encoding='utf-8')

    @patch('builtins.open')
    @patch('os.walk')
    def test_mixed_extensions_yaml(self, mock_os_walk, mock_open_builtin):
        mock_os_walk.return_value = [
            ('/test_dir', [], ['config1.yaml', 'config3.json'])
        ]
        mock_open_builtin.side_effect = self.mock_open_side_effect

        expected_result = {
            'key_a': ['/test_dir/config1.yaml'],
            'key_b': ['/test_dir/config1.yaml']
        }
        result = mapper.map_config_constellation('/test_dir', '.yaml')
        self.assertEqual(result, expected_result)
        mock_open_builtin.assert_any_call('/test_dir/config1.yaml', 'r', encoding='utf-8')
        # config3.json should not be opened when looking for .yaml
        with self.assertRaises(AssertionError):
            mock_open_builtin.assert_any_call('/test_dir/config3.json', 'r', encoding='utf-8')

    @patch('builtins.open')
    @patch('os.walk')
    def test_mixed_extensions_json(self, mock_os_walk, mock_open_builtin):
        mock_os_walk.return_value = [
            ('/test_dir', [], ['config1.yaml', 'config3.json'])
        ]
        mock_open_builtin.side_effect = self.mock_open_side_effect

        expected_result = {
            'json_key_1': ['/test_dir/config3.json'],
            'json_key_2': ['/test_dir/config3.json']
        }
        result = mapper.map_config_constellation('/test_dir', '.json')
        self.assertEqual(result, expected_result)
        mock_open_builtin.assert_any_call('/test_dir/config3.json', 'r', encoding='utf-8')
        # config1.yaml should not be opened when looking for .json
        with self.assertRaises(AssertionError):
            mock_open_builtin.assert_any_call('/test_dir/config1.yaml', 'r', encoding='utf-8')


if __name__ == '__main__':
    unittest.main()
