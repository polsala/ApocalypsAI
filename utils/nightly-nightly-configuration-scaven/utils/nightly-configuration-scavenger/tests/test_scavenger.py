import pytest
import os
import json
import yaml
import configparser
from unittest.mock import patch, mock_open
from src.scavenger import parse_ini, parse_json, parse_yaml, scavenge_configs, main

# --- Test individual parsers ---

def test_parse_ini_valid():
    ini_content = """
[section1]
key1 = value1
key2 = 123

[section2]
host = localhost
port = 8080
"""
    expected = {
        "section1": {"key1": "value1", "key2": "123"},
        "section2": {"host": "localhost", "port": "8080"}
    }
    assert parse_ini(ini_content) == expected

def test_parse_ini_empty():
    assert parse_ini("") == {}

def test_parse_ini_invalid():
    ini_content = "not a valid ini format"
    # Mock rationale: configparser.read_string expects a valid INI format.
    # configparser is quite forgiving for simple malformed strings and often
    # parses an empty config if no sections are found or ignores malformed lines.
    # Here, we expect it to return an empty dict as no valid sections are present.
    assert parse_ini(ini_content) == {} 

def test_parse_json_valid():
    json_content = '{"name": "test", "value": 123}'
    expected = {"name": "test", "value": 123}
    assert parse_json(json_content) == expected

def test_parse_json_empty():
    with pytest.raises(json.JSONDecodeError):
        parse_json("")

def test_parse_json_invalid():
    json_content = '{"name": "test", "value": 123' # Missing closing brace
    with pytest.raises(json.JSONDecodeError):
        parse_json(json_content)

def test_parse_yaml_valid():
    yaml_content = """
name: test
data:
  key: value
list:
  - item1
  - item2
"""
    expected = {
        "name": "test",
        "data": {"key": "value"},
        "list": ["item1", "item2"]
    }
    assert parse_yaml(yaml_content) == expected

def test_parse_yaml_empty():
    assert parse_yaml("") is None # yaml.safe_load returns None for empty string

def test_parse_yaml_invalid():
    yaml_content = """
- item1
  item2: value # Invalid indentation
"""
    with pytest.raises(yaml.YAMLError):
        parse_yaml(yaml_content)

# --- Test scavenge_configs ---

@patch('os.walk')
@patch('builtins.open', new_callable=mock_open)
def test_scavenge_configs_multiple_formats(mock_file_open, mock_os_walk):
    # Mock rationale: Simulate a file system structure and file contents
    # without actually touching the disk, ensuring deterministic and offline tests.
    
    mock_os_walk.return_value = [
        ('/mock_dir', ('sub_dir',), ('app.ini', 'config.json', 'settings.yaml', 'invalid.txt')),
        ('/mock_dir/sub_dir', (), ('db.json', 'malformed.ini', 'empty.yaml'))
    ]

    # Configure mock_file_open to return different content based on file path
    def mock_open_side_effect(file_path, mode='r', encoding='utf-8'):
        if file_path == '/mock_dir/app.ini':
            return mock_open(read_data="[main]\nuser=admin").return_value
        elif file_path == '/mock_dir/config.json':
            return mock_open(read_data='{"debug": true, "port": 80}').return_value
        elif file_path == '/mock_dir/settings.yaml':
            return mock_open(read_data='database:\n  host: db.example.com').return_value
        elif file_path == '/mock_dir/sub_dir/db.json':
            return mock_open(read_data='{"connection": "postgres"}').return_value
        elif file_path == '/mock_dir/sub_dir/malformed.ini':
            # configparser is forgiving, will parse this as an empty config if no valid sections
            return mock_open(read_data='[section\nkey=value').return_value 
        elif file_path == '/mock_dir/sub_dir/empty.yaml':
            return mock_open(read_data='').return_value
        raise FileNotFoundError(f"File not found: {file_path}")

    mock_file_open.side_effect = mock_open_side_effect

    expected_results = {
        '/mock_dir/app.ini': {'main': {'user': 'admin'}},
        '/mock_dir/config.json': {'debug': True, 'port': 80},
        '/mock_dir/settings.yaml': {'database': {'host': 'db.example.com'}},
        '/mock_dir/sub_dir/db.json': {'connection': 'postgres'},
        '/mock_dir/sub_dir/malformed.ini': {}, 
        '/mock_dir/sub_dir/empty.yaml': None 
    }

    results = scavenge_configs('/mock_dir', ['ini', 'json', 'yaml'])
    assert results == expected_results

@patch('os.walk')
@patch('builtins.open', new_callable=mock_open)
def test_scavenge_configs_unsupported_extension(mock_file_open, mock_os_walk):
    # Mock rationale: Ensure only specified extensions are processed.
    mock_os_walk.return_value = [
        ('/mock_dir', (), ('config.toml', 'settings.json'))
    ]
    mock_file_open.return_value.read.return_value = '{"key": "value"}'

    results = scavenge_configs('/mock_dir', ['json'])
    assert '/mock_dir/settings.json' in results
    assert '/mock_dir/config.toml' not in results

@patch('os.walk')
@patch('builtins.open', new_callable=mock_open)
def test_scavenge_configs_parsing_error(mock_file_open, mock_os_walk):
    # Mock rationale: Verify that parsing errors are caught and reported.
    mock_os_walk.return_value = [
        ('/mock_dir', (), ('bad.json', 'good.json'))
    ]

    def mock_open_side_effect(file_path, mode='r', encoding='utf-8'):
        if file_path == '/mock_dir/bad.json':
            return mock_open(read_data='{"key": "value"').return_value # Malformed JSON
        elif file_path == '/mock_dir/good.json':
            return mock_open(read_data='{"status": "ok"}').return_value
        raise FileNotFoundError(f"File not found: {file_path}")

    mock_file_open.side_effect = mock_open_side_effect

    results = scavenge_configs('/mock_dir', ['json'])
    assert '/mock_dir/good.json' in results
    assert results['/mock_dir/good.json'] == {'status': 'ok'}
    assert '/mock_dir/bad.json' in results
    assert 'error' in results['/mock_dir/bad.json']
    assert 'JSONDecodeError' in results['/mock_dir/bad.json']['error']

@patch('os.path.isdir', return_value=True)
@patch('src.scavenger.scavenge_configs', return_value={'file.json': {'key': 'value'}})
@patch('builtins.print')
@patch('sys.exit')
def test_main_prints_to_stdout(mock_exit, mock_print, mock_scavenge, mock_isdir):
    # Mock rationale: Test the main function's CLI interaction and output behavior.
    # We mock os.path.isdir to simulate a valid directory, scavenge_configs to provide data,
    # print to capture stdout, and sys.exit to prevent actual program termination during test.
    
    test_args = ['--path', '/test_dir', '--extensions', 'json']
    with patch('sys.argv', ['scavenger.py'] + test_args):
        main()
        mock_print.assert_called_once_with(json.dumps({'file.json': {'key': 'value'}}, indent=2))
        mock_exit.assert_not_called() # Should not exit on success

@patch('os.path.isdir', return_value=True)
@patch('src.scavenger.scavenge_configs', return_value={'file.json': {'key': 'value'}})
@patch('builtins.open', new_callable=mock_open)
@patch('builtins.print')
@patch('sys.exit')
def test_main_writes_to_file(mock_exit, mock_print, mock_file_open, mock_scavenge, mock_isdir):
    # Mock rationale: Test the main function's ability to write output to a specified file.
    test_args = ['--path', '/test_dir', '--extensions', 'json', '--output', '/output.json']
    with patch('sys.argv', ['scavenger.py'] + test_args):
        main()
        mock_file_open.assert_called_once_with('/output.json', 'w', encoding='utf-8')
        mock_file_open().write.assert_called_once_with(json.dumps({'file.json': {'key': 'value'}}, indent=2))
        mock_print.assert_called_once_with("Scavenged data saved to '/output.json'")
        mock_exit.assert_not_called()

@patch('os.path.isdir', return_value=False)
@patch('builtins.print')
@patch('sys.exit')
def test_main_invalid_path_exits(mock_exit, mock_print, mock_isdir):
    # Mock rationale: Test error handling for an invalid input directory.
    test_args = ['--path', '/non_existent_dir']
    with patch('sys.argv', ['scavenger.py'] + test_args):
        main()
        mock_print.assert_called_once() # Should print an error message
        mock_exit.assert_called_once_with(1) # Should exit with error code 1

@patch('os.path.isdir', return_value=True)
@patch('src.scavenger.scavenge_configs', return_value={'file.json': {'key': 'value'}})
@patch('builtins.open', side_effect=IOError("Permission denied"))
@patch('builtins.print')
@patch('sys.exit')
def test_main_output_file_error_exits(mock_exit, mock_print, mock_file_open, mock_scavenge, mock_isdir):
    # Mock rationale: Test error handling when writing to the output file fails.
    test_args = ['--path', '/test_dir', '--output', '/unwritable.json']
    with patch('sys.argv', ['scavenger.py'] + test_args):
        main()
        mock_print.assert_called_once() # Should print an error message
        mock_exit.assert_called_once_with(1) # Should exit with error code 1
