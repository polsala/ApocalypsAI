import unittest
import os
import json
import yaml
from unittest.mock import patch, mock_open
from src.mapper import (
    parse_yaml, parse_json, parse_ini,
    flatten_dict, scan_and_map_configs, analyze_configs
)

class TestConfigMapper(unittest.TestCase):

    def test_parse_yaml(self):
        yaml_content = """
        key1: value1
        key2:
            nested_key: nested_value
        list_key:
            - item1
            - item2
        """
        expected = {
            'key1': 'value1',
            'key2': {'nested_key': 'nested_value'},
            'list_key': ['item1', 'item2']
        }
        self.assertEqual(parse_yaml(yaml_content), expected)
        self.assertIsNone(parse_yaml("invalid: -")) # Invalid YAML

    def test_parse_json(self):
        json_content = """
        {
            "key1": "value1",
            "key2": {
                "nested_key": "nested_value"
            }
        }
        """
        expected = {
            'key1': 'value1',
            'key2': {'nested_key': 'nested_value'}
        }
        self.assertEqual(parse_json(json_content), expected)
        self.assertIsNone(parse_json("{invalid json")) # Invalid JSON

    def test_parse_ini(self):
        ini_content = """
        [section1]
        key1 = value1
        key2 = value2

        [section2]
        key3 = value3
        """
        expected = {
            'section1': {'key1': 'value1', 'key2': 'value2'},
            'section2': {'key3': 'value3'}
        }
        self.assertEqual(parse_ini(ini_content), expected)
        self.assertIsNone(parse_ini("invalid ini")) # Invalid INI

    def test_flatten_dict(self):
        nested_dict = {
            'a': 1,
            'b': {
                'c': 2,
                'd': {
                    'e': 3
                }
            },
            'f': [4, 5]
        }
        expected_flat = {
            'a': 1,
            'b.c': 2,
            'b.d.e': 3,
            'f': [4, 5]
        }
        self.assertEqual(flatten_dict(nested_dict), expected_flat)

    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_scan_and_map_configs(self, mock_file_open, mock_os_walk):
        # Mock rationale: Simulate file system traversal and content reading without actual files.
        # This ensures deterministic and offline testing.

        # Setup mock os.walk to return a specific directory structure
        mock_os_walk.return_value = [
            ('/test_dir', ('sub_dir',), ('config1.yaml', 'config2.json', 'config3.ini', 'ignore.txt')),
            ('/test_dir/sub_dir', (), ('sub_config.yaml',))
        ]

        # Setup mock_file_open to return specific content for each file
        def mock_open_side_effect(file_path, mode='r', encoding='utf-8'):
            if 'config1.yaml' in file_path:
                return mock_open(read_data="key_yaml: value_yaml\ncommon_key: common_value_1").return_value
            elif 'config2.json' in file_path:
                return mock_open(read_data='{"key_json": "value_json", "common_key": "common_value_2"}').return_value
            elif 'config3.ini' in file_path:
                return mock_open(read_data='[main]\nkey_ini = value_ini\ncommon_key = common_value_1').return_value
            elif 'sub_config.yaml' in file_path:
                return mock_open(read_data="sub_key: sub_value\ncommon_key: common_value_1").return_value
            elif 'ignore.txt' in file_path:
                return mock_open(read_data="plain text").return_value
            raise FileNotFoundError(f"File not found: {file_path}")

        mock_file_open.side_effect = mock_open_side_effect

        expected_configs = {
            'config1.yaml': {'key_yaml': 'value_yaml', 'common_key': 'common_value_1'},
            'config2.json': {'key_json': 'value_json', 'common_key': 'common_value_2'},
            'config3.ini': {'main.key_ini': 'value_ini', 'main.common_key': 'common_value_1'}, # INI keys are flattened with section
            'sub_config.yaml': {'sub_key': 'sub_value', 'common_key': 'common_value_1'}
        }

        result = scan_and_map_configs('/test_dir')
        self.assertDictEqual(result, expected_configs)
        self.assertEqual(mock_os_walk.call_count, 1)
        # Check that open was called for relevant files
        self.assertTrue(any('config1.yaml' in call.args[0] for call in mock_file_open.call_args_list))
        self.assertTrue(any('config2.json' in call.args[0] for call in mock_file_open.call_args_list))
        self.assertTrue(any('config3.ini' in call.args[0] for call in mock_file_open.call_args_list))
        self.assertTrue(any('sub_config.yaml' in call.args[0] for call in mock_file_open.call_args_list))
        self.assertFalse(any('ignore.txt' in call.args[0] for call in mock_file_open.call_args_list))


    def test_analyze_configs(self):
        # Mock rationale: Provide pre-parsed, flattened configurations to test the analysis logic directly.
        # This isolates the analysis function from file parsing and I/O.
        mock_flat_configs = {
            'agent_alpha.yaml': {
                'log_level': 'INFO',
                'api_key': 'abc',
                'feature_flags.new_ui': True
            },
            'agent_beta.json': {
                'log_level': 'DEBUG',
                'api_key': 'abc',
                'database.host': 'localhost'
            },
            'agent_gamma.ini': {
                'main.log_level': 'INFO', # Note: INI parsing flattens with section name
                'main.database.port': 5432
            }
        }

        expected_analysis = {
            "shared_keys": {
                "api_key": {
                    "abc": ["agent_alpha.yaml", "agent_beta.json"]
                }
            },
            "inconsistent_values": [
                {
                    "key": "log_level",
                    "values": {
                        "INFO": ["agent_alpha.yaml"],
                        "DEBUG": ["agent_beta.json"]
                    }
                }
            ],
            "missing_keys": [
                {
                    "key": "api_key",
                    "present_in": ["agent_alpha.yaml", "agent_beta.json"],
                    "absent_from": ["agent_gamma.ini"]
                },
                {
                    "key": "database.host",
                    "present_in": ["agent_beta.json"],
                    "absent_from": ["agent_alpha.yaml", "agent_gamma.ini"]
                },
                {
                    "key": "feature_flags.new_ui",
                    "present_in": ["agent_alpha.yaml"],
                    "absent_from": ["agent_beta.json", "agent_gamma.ini"]
                },
                {
                    "key": "log_level",
                    "present_in": ["agent_alpha.yaml", "agent_beta.json"],
                    "absent_from": ["agent_gamma.ini"]
                },
                {
                    "key": "main.database.port",
                    "present_in": ["agent_gamma.ini"],
                    "absent_from": ["agent_alpha.yaml", "agent_beta.json"]
                },
                {
                    "key": "main.log_level",
                    "present_in": ["agent_gamma.ini"],
                    "absent_from": ["agent_alpha.yaml", "agent_beta.json"]
                }
            ]
        }
        
        result = analyze_configs(mock_flat_configs)

        # Sort lists within the expected and actual results for consistent comparison
        def sort_analysis_data(data):
            if isinstance(data, dict):
                return {k: sort_analysis_data(v) for k, v in data.items()}
            if isinstance(data, list):
                return sorted([sort_analysis_data(item) for item in data], key=lambda x: json.dumps(x, sort_keys=True))
            return data

        # The order of inconsistent_values and missing_keys might vary, so sort them
        sorted_result = sort_analysis_data(result)
        sorted_expected = sort_analysis_data(expected_analysis)

        self.assertDictEqual(sorted_result, sorted_expected)


if __name__ == '__main__':
    unittest.main()
