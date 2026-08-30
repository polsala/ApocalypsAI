import unittest
from unittest.mock import patch, mock_open
import sys
import os

# Mock the yaml library to control its behavior during tests
class MockYaml:
    def safe_load(self, stream):
        if 'syntax error' in stream.read():
            raise self.YAMLError("Mocked syntax error")
        return {}

    class YAMLError(Exception):
        pass

# Mock the os.walk function to control directory traversal
class MockOsWalk:
    def __init__(self, files_to_return):
        self.files_to_return = files_to_return

    def __iter__(self):
        return iter(self.files_to_return)

# Mock sys.exit to prevent actual program termination during tests
@patch('sys.exit')
# Mock os.environ to control environment variables
@patch('os.environ', {
    'INPUT_SEARCH_PATH': '.',
    'INPUT_FAIL_ON_ERROR': 'false'
})
# Mock open to control file reading
@patch('builtins.open', new_callable=mock_open)
# Mock yaml.safe_load and yaml.YAMLError
@patch('yaml', new_callable=MockYaml)
# Mock os.walk
@patch('os.walk', new_callable=MockOsWalk)
def test_yaml_lint_reporter(mock_os_walk, mock_yaml, mock_file_open, mock_sys_exit):
    # Import the main function after patching
    from src.main import main

    # --- Test Case 1: No errors --- 
    mock_file_open.side_effect = [
        mock_open(read_data='key: value\n').return_value, # For file1.yaml
        mock_open(read_data='another: \n  nested: true').return_value # For file2.yml
    ]
    mock_os_walk.side_effect = [[
        ('.', ['file1.yaml', 'file2.yml'], [])
    ]]
    
    main()
    
    # Assertions for no errors case
    mock_sys_exit.assert_not_called()
    # Check if outputs were set correctly
    # Note: Accessing set-output is tricky in direct tests, we rely on sys.exit behavior for fail_on_error
    # and the absence of error messages for success.
    
    # --- Test Case 2: With errors --- 
    mock_file_open.side_effect = [
        mock_open(read_data='key: value\n').return_value, # For file1.yaml
        mock_open(read_data='invalid yaml syntax: \n  - item1\n  item2: \n    - subitem').return_value # For file_with_error.yaml
    ]
    mock_os_walk.side_effect = [[
        ('.', ['file1.yaml', 'file_with_error.yaml'], [])
    ]]
    
    # Resetting mocks for the second test case
    mock_yaml.reset_mock()
    mock_file_open.reset_mock()
    mock_sys_exit.reset_mock()
    
    # Re-apply mocks for the second test case
    @patch('sys.exit')
    @patch('os.environ', {
        'INPUT_SEARCH_PATH': '.',
        'INPUT_FAIL_ON_ERROR': 'true'
    })
    @patch('builtins.open', new_callable=mock_open)
    @patch('yaml', new_callable=MockYaml)
    @patch('os.walk', new_callable=MockOsWalk)
    def run_second_test(mock_os_walk_2, mock_yaml_2, mock_file_open_2, mock_sys_exit_2):
        from src.main import main
        mock_file_open_2.side_effect = [
            mock_open(read_data='key: value\n').return_value, # For file1.yaml
            mock_open(read_data='invalid yaml syntax: \n  - item1\n  item2: \n    - subitem').return_value # For file_with_error.yaml
        ]
        mock_os_walk_2.side_effect = [[
            ('.', ['file1.yaml', 'file_with_error.yaml'], [])
        ]]
        main()
        mock_sys_exit_2.assert_called_once_with(1)

    run_second_test()

    # --- Test Case 3: No YAML files found --- 
    mock_file_open.reset_mock()
    mock_os_walk.side_effect = [[
        ('.', ['some_other_file.txt'], [])
    ]]
    
    main()
    mock_sys_exit.assert_not_called() # Should not exit with error if no files found


if __name__ == '__main__':
    unittest.main()
