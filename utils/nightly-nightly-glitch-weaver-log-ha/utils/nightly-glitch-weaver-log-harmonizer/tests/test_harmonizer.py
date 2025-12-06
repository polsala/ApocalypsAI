import pytest
import json
from unittest.mock import patch, mock_open
from io import StringIO
from src.harmonizer import LogHarmonizer, main

@pytest.fixture
def harmonizer_instance():
    """Provides a fresh LogHarmonizer instance for each test."""
    return LogHarmonizer()

def test_harmonize_line_apache_access(harmonizer_instance):
    """Test harmonizing an Apache access log line."""
    line = '192.168.1.1 - - [27/Oct/2023:10:00:05 +0000] "GET /index.html HTTP/1.1" 200 1234'
    expected = {
        "ip": "192.168.1.1",
        "timestamp": "27/Oct/2023:10:00:05 +0000",
        "method": "GET",
        "path": "/index.html",
        "protocol": "HTTP/1.1",
        "status": "200",
        "size": "1234",
        "_pattern_name": "apache_access"
    }
    assert harmonizer_instance.harmonize_line(line) == expected

def test_harmonize_line_timestamped_message_with_user_ip(harmonizer_instance):
    """Test harmonizing a timestamped message with user and IP."""
    line = '[2023-10-27 10:00:01] INFO: User \'Alice\' logged in from 192.168.1.100'
    expected = {
        "timestamp": "2023-10-27 10:00:01",
        "level": "INFO",
        "user": "Alice",
        "ip": "192.168.1.100",
        "_pattern_name": "timestamped_message_with_user_ip"
    }
    assert harmonizer_instance.harmonize_line(line) == expected

def test_harmonize_line_timestamped_message(harmonizer_instance):
    """Test harmonizing a generic timestamped message."""
    line = '[2023-10-27 10:00:02] DEBUG: Application started successfully.'
    expected = {
        "timestamp": "2023-10-27 10:00:02",
        "level": "DEBUG",
        "message": "Application started successfully.",
        "_pattern_name": "timestamped_message"
    }
    assert harmonizer_instance.harmonize_line(line) == expected

def test_harmonize_line_simple_level_message(harmonizer_instance):
    """Test harmonizing a simple level message."""
    line = 'WARN: Low memory detected.'
    expected = {
        "level": "WARN",
        "message": "Low memory detected.",
        "_pattern_name": "simple_level_message"
    }
    assert harmonizer_instance.harmonize_line(line) == expected

def test_harmonize_line_key_value_pairs(harmonizer_instance):
    """Test harmonizing a line with key-value pairs."""
    line = 'event=login user_id=123'
    expected = {
        "key1": "event",
        "value1": "login",
        "key2": "user_id",
        "value2": "123",
        "_pattern_name": "key_value_pairs"
    }
    assert harmonizer_instance.harmonize_line(line) == expected

def test_harmonize_line_unmatched(harmonizer_instance):
    """Test harmonizing an unmatched log line."""
    line = 'This is a completely random log entry without a clear pattern.'
    expected = {
        "raw_message": "This is a completely random log entry without a clear pattern.",
        "_pattern_name": "unmatched"
    }
    assert harmonizer_instance.harmonize_line(line) == expected

def test_harmonize_logs_multiple_lines(harmonizer_instance):
    """Test harmonizing multiple lines with different patterns."""
    log_lines = [
        '[2023-10-27 10:00:01] INFO: User \'Alice\' logged in from 192.168.1.100',
        'WARN: Low memory detected.',
        '192.168.1.1 - - [27/Oct/2023:10:00:05 +0000] "GET /index.html HTTP/1.1" 200 1234',
        'Unrecognized line.'
    ]
    expected_outputs = [
        {"timestamp": "2023-10-27 10:00:01", "level": "INFO", "user": "Alice", "ip": "192.168.1.100", "_pattern_name": "timestamped_message_with_user_ip"},
        {"level": "WARN", "message": "Low memory detected.", "_pattern_name": "simple_level_message"},
        {"ip": "192.168.1.1", "timestamp": "27/Oct/2023:10:00:05 +0000", "method": "GET", "path": "/index.html", "protocol": "HTTP/1.1", "status": "200", "size": "1234", "_pattern_name": "apache_access"},
        {"raw_message": "Unrecognized line.", "_pattern_name": "unmatched"}
    ]
    
    results = list(harmonizer_instance.harmonize_logs(log_lines))
    assert results == expected_outputs

@patch('sys.stdout', new_callable=StringIO)
@patch('builtins.open', new_callable=mock_open)
@patch('argparse.ArgumentParser.parse_args')
def test_main_with_file_input(mock_parse_args, mock_file_open, mock_stdout):
    """Test main function with a log file as input."""
    # Mock rationale: We need to simulate reading from a file without actually touching the filesystem.
    # `mock_open` simulates `open()` and allows us to control the file content.
    # `sys.stdout` is mocked to capture printed output for assertion.
    # `argparse.ArgumentParser.parse_args` is mocked to control command-line arguments.

    mock_parse_args.return_value.log_file = 'test.log'
    mock_file_open.return_value.__enter__.return_value = StringIO(
        '[2023-10-27 10:00:01] INFO: Test message 1\n'
        'WARN: Test message 2\n'
    )

    main()

    output_lines = mock_stdout.getvalue().strip().split('\n')
    assert len(output_lines) == 2
    assert json.loads(output_lines[0]) == {
        "timestamp": "2023-10-27 10:00:01",
        "level": "INFO",
        "message": "Test message 1",
        "_pattern_name": "timestamped_message"
    }
    assert json.loads(output_lines[1]) == {
        "level": "WARN",
        "message": "Test message 2",
        "_pattern_name": "simple_level_message"
    }
    mock_file_open.assert_called_once_with('test.log', 'r', encoding='utf-8')

@patch('sys.stdout', new_callable=StringIO)
@patch('sys.stdin', new_callable=StringIO)
@patch('argparse.ArgumentParser.parse_args')
def test_main_with_stdin_input(mock_parse_args, mock_stdin, mock_stdout):
    """Test main function with stdin as input."""
    # Mock rationale: We need to simulate reading from stdin without user interaction.
    # `sys.stdin` is mocked to provide predefined input.
    # `sys.stdout` is mocked to capture printed output for assertion.
    # `argparse.ArgumentParser.parse_args` is mocked to control command-line arguments.

    mock_parse_args.return_value.log_file = None
    mock_stdin.write('[2023-10-27 10:00:01] INFO: Stdin message 1\n')
    mock_stdin.write('WARN: Stdin message 2\n')
    mock_stdin.seek(0) # Reset stdin buffer position

    main()

    output_lines = mock_stdout.getvalue().strip().split('\n')
    assert len(output_lines) == 2
    assert json.loads(output_lines[0]) == {
        "timestamp": "2023-10-27 10:00:01",
        "level": "INFO",
        "message": "Stdin message 1",
        "_pattern_name": "timestamped_message"
    }
    assert json.loads(output_lines[1]) == {
        "level": "WARN",
        "message": "Stdin message 2",
        "_pattern_name": "simple_level_message"
    }

@patch('sys.stderr', new_callable=StringIO)
@patch('builtins.open', new_callable=mock_open)
@patch('argparse.ArgumentParser.parse_args')
@patch('sys.exit')
def test_main_file_not_found(mock_exit, mock_file_open, mock_parse_args, mock_stderr):
    """Test main function handles FileNotFoundError."""
    # Mock rationale: We need to simulate a FileNotFoundError without creating a non-existent file.
    # `mock_file_open` is configured to raise FileNotFoundError.
    # `sys.stderr` is mocked to capture error messages.
    # `sys.exit` is mocked to prevent the test from actually exiting.

    mock_parse_args.return_value.log_file = 'non_existent.log'
    mock_file_open.side_effect = FileNotFoundError

    main()

    assert "Error: Log file 'non_existent.log' not found." in mock_stderr.getvalue()
    mock_exit.assert_called_once_with(1)

@patch('sys.stderr', new_callable=StringIO)
@patch('builtins.open', new_callable=mock_open)
@patch('argparse.ArgumentParser.parse_args')
@patch('sys.exit')
def test_main_general_exception(mock_exit, mock_file_open, mock_parse_args, mock_stderr):
    """Test main function handles general exceptions during file processing."""
    # Mock rationale: We need to simulate an unexpected error during file reading.
    # `mock_file_open` is configured to return a StringIO object, but then we simulate an error
    # during its `read` method (or iteration) to trigger the exception handling.
    # `sys.stderr` is mocked to capture error messages.
    # `sys.exit` is mocked to prevent the test from actually exiting.

    mock_parse_args.return_value.log_file = 'problematic.log'
    # Create a mock file that will raise an exception when read
    mock_file_content = StringIO("valid line\nline that causes error")
    mock_file_open.return_value.__enter__.return_value = mock_file_content
    # Simulate an error during iteration over the file lines
    def broken_lines():
        yield "line 1"
        raise Exception("Simulated read error")
    mock_file_open.return_value.__enter__.return_value.__iter__.return_value = broken_lines()

    main()

    assert "Error processing file: Simulated read error" in mock_stderr.getvalue()
    mock_exit.assert_called_once_with(1)
