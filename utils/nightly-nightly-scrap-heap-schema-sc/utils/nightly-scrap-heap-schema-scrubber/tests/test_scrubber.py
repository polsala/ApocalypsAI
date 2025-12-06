import pytest
import os
import json
import yaml
from unittest.mock import patch, mock_open
from src.scrubber import clean_data, main

# Mock rationale: We need to test the file I/O and argument parsing of the main function
# without actually touching the filesystem or relying on external files.
# `mock_open` allows simulating file read/write operations in memory.
# `patch('sys.argv')` allows simulating command-line arguments.

@pytest.fixture
def temp_files(tmp_path):
    """
    Provides temporary input and output file paths for tests.
    Mock rationale: Creates temporary files for I/O operations to ensure tests are self-contained
    and don't affect the actual filesystem.
    """
    input_file = tmp_path / "input.json"
    output_file = tmp_path / "output.json"
    yield input_file, output_file

@pytest.fixture
def temp_yaml_files(tmp_path):
    """
    Provides temporary input and output YAML file paths for tests.
    Mock rationale: Same as temp_files, but for YAML.
    """
    input_file = tmp_path / "input.yaml"
    output_file = tmp_path / "output.yaml"
    yield input_file, output_file

# --- Test clean_data function ---

def test_clean_data_removes_empty_dict_and_list():
    data = {
        "a": 1,
        "b": {},
        "c": [],
        "d": {"e": {}},
        "f": [1, [], {"g": {}}],
        "h": None
    }
    expected = {
        "a": 1,
        "f": [1]
    }
    assert clean_data(data) == expected

def test_clean_data_removes_null_values():
    data = {
        "a": 1,
        "b": None,
        "c": {"d": None, "e": 2},
        "f": [1, None, 3]
    }
    expected = {
        "a": 1,
        "c": {"e": 2},
        "f": [1, 3]
    }
    assert clean_data(data) == expected

def test_clean_data_removes_specified_keys():
    data = {
        "id": "123",
        "name": "test",
        "metadata": {"version": 1},
        "details": {"temp_id": "abc", "value": 10}
    }
    keys_to_remove = ["id", "temp_id"]
    expected = {
        "name": "test",
        "metadata": {"version": 1},
        "details": {"value": 10}
    }
    assert clean_data(data, keys_to_remove) == expected

def test_clean_data_handles_nested_cleaning_and_key_removal():
    data = {
        "root_id": "xyz",
        "user": {
            "id": "u1",
            "name": "Alice",
            "email": None,
            "preferences": {},
            "tags": []
        },
        "items": [
            {"item_id": "i1", "value": 10, "temp_data": None},
            {"item_id": "i2", "value": 20, "metadata": {"status": "active"}},
            {"item_id": "i3", "value": 30, "temp_data": {}, "tags": []}
        ],
        "empty_section": {},
        "null_field": None,
        "global_tags": ["tag1", "tag2", "temp_tag"]
    }
    keys_to_remove = ["root_id", "email", "temp_data", "temp_tag"]
    expected = {
        "user": {
            "id": "u1",
            "name": "Alice"
        },
        "items": [
            {"item_id": "i1", "value": 10},
            {"item_id": "i2", "value": 20, "metadata": {"status": "active"}},
            {"item_id": "i3", "value": 30}
        ],
        "global_tags": ["tag1", "tag2"]
    }
    assert clean_data(data, keys_to_remove) == expected

def test_clean_data_returns_none_for_completely_empty_input():
    assert clean_data({}) is None
    assert clean_data([]) is None
    assert clean_data(None) is None
    assert clean_data({"a": None, "b": {}}) is None
    assert clean_data([None, [], {}]) is None

def test_clean_data_handles_non_dict_or_list_input():
    assert clean_data(123) == 123
    assert clean_data("hello") == "hello"
    assert clean_data(True) == True

# --- Test main function with mocks ---

def test_main_json_cleaning(temp_files):
    input_file, output_file = temp_files
    input_content = {
        "a": 1,
        "b": {},
        "c": None,
        "d": [1, [], {"e": None}],
        "f": "value"
    }
    expected_output_content = {
        "a": 1,
        "d": [1],
        "f": "value"
    }

    # Mock rationale: Simulate file system operations without actual disk I/O.
    # `mock_open` intercepts `open()` calls.
    # `patch('os.path.exists')` ensures the input file is considered present.
    with patch('builtins.open', mock_open(read_data=json.dumps(input_content))) as m_open, \
         patch('os.path.exists', return_value=True), \
         patch('sys.argv', ['scrubber.py', '--input', str(input_file), '--output', str(output_file)]):
        main()

        # Verify input file was opened for reading
        m_open.assert_any_call(str(input_file), 'r', encoding='utf-8')
        # Verify output file was opened for writing
        m_open.assert_any_call(str(output_file), 'w', encoding='utf-8')

        # Get the written content from the mock
        written_content = m_open().write.call_args[0][0]
        assert json.loads(written_content) == expected_output_content

def test_main_yaml_cleaning_with_key_removal(temp_yaml_files):
    input_file, output_file = temp_yaml_files
    input_content = """
id: 123
name: Test Item
details:
  version: 1.0
  temp_id: abc
  tags: []
metadata: {}
status: null
    """
    expected_output_content = {
        "name": "Test Item",
        "details": {
            "version": 1.0
        }
    }

    # Mock rationale: Simulate file system operations for YAML.
    with patch('builtins.open', mock_open(read_data=input_content)) as m_open, \
         patch('os.path.exists', return_value=True), \
         patch('sys.argv', ['scrubber.py', '--input', str(input_file), '--output', str(output_file), '--remove-keys', 'id', 'temp_id', 'status']):
        main()

        m_open.assert_any_call(str(input_file), 'r', encoding='utf-8')
        m_open.assert_any_call(str(output_file), 'w', encoding='utf-8')

        written_content = m_open().write.call_args[0][0]
        assert yaml.safe_load(written_content) == expected_output_content

def test_main_input_file_not_found(temp_files, capsys):
    input_file, output_file = temp_files
    # Mock rationale: Simulate os.path.exists returning False for the input file.
    with patch('os.path.exists', return_value=False), \
         patch('sys.argv', ['scrubber.py', '--input', str(input_file), '--output', str(output_file)]), \
         pytest.raises(SystemExit) as excinfo: # main() calls exit(1) on error
        main()
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert f"Error: Input file not found at '{input_file}'" in captured.out

def test_main_unsupported_input_type(temp_files, capsys):
    input_file, output_file = temp_files
    input_file = input_file.with_suffix(".txt") # Change extension to unsupported
    # Mock rationale: Simulate an unsupported file extension.
    with patch('os.path.exists', return_value=True), \
         patch('sys.argv', ['scrubber.py', '--input', str(input_file), '--output', str(output_file)]), \
         pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Unsupported input file type '.txt'" in captured.out

def test_main_unsupported_output_type(temp_files, capsys):
    input_file, output_file = temp_files
    output_file = output_file.with_suffix(".txt") # Change extension to unsupported
    input_content = {"a": 1}
    # Mock rationale: Simulate an unsupported output file extension.
    with patch('builtins.open', mock_open(read_data=json.dumps(input_content))), \
         patch('os.path.exists', return_value=True), \
         patch('sys.argv', ['scrubber.py', '--input', str(input_file), '--output', str(output_file)]), \
         pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Unsupported output file type '.txt'" in captured.out

def test_main_json_decode_error(temp_files, capsys):
    input_file, output_file = temp_files
    bad_json_content = "{'a': 1" # Invalid JSON
    # Mock rationale: Simulate a JSON decoding error during file read.
    with patch('builtins.open', mock_open(read_data=bad_json_content)), \
         patch('os.path.exists', return_value=True), \
         patch('sys.argv', ['scrubber.py', '--input', str(input_file), '--output', str(output_file)]), \
         pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error parsing input file" in captured.out
    assert "JSONDecodeError" in captured.out

def test_main_yaml_parse_error(temp_yaml_files, capsys):
    input_file, output_file = temp_yaml_files
    bad_yaml_content = "key: - value" # Invalid YAML
    # Mock rationale: Simulate a YAML parsing error during file read.
    with patch('builtins.open', mock_open(read_data=bad_yaml_content)), \
         patch('os.path.exists', return_value=True), \
         patch('sys.argv', ['scrubber.py', '--input', str(input_file), '--output', str(output_file)]), \
         pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error parsing input file" in captured.out
    assert "YAMLError" in captured.out
