import pytest
import os
import sys
from unittest.mock import patch, mock_open
from datetime import datetime

# Add the src directory to the path to allow importing luminator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from luminator import scan_log_file, generate_summary_report, main, DEFAULT_PATTERNS

# Mock rationale: We need to simulate file system interactions without actually creating files
# or relying on the host's file system state. `mock_open` and `os.path` mocks achieve this.

@pytest.fixture
def mock_log_content():
    """Fixture for common log content."""
    return """
INFO: Application started
ERROR: Failed to connect to database
DEBUG: Processing request 123
WARNING: Disk space low
ERROR: NullPointerException at com.example.App.doSomething(App.java:42)
INFO: User 'admin' logged in
CRITICAL: System meltdown imminent
Another line with an error keyword but not a full pattern.
Exception: An unexpected error occurred.
Traceback (most recent call last):
  File "app.py", line 10, in <module>
    raise ValueError("Test error")
ValueError: Test error
"""

@pytest.fixture
def mock_empty_log_content():
    """Fixture for empty log content."""
    return ""

@pytest.fixture
def mock_no_match_log_content():
    """Fixture for log content with no matching patterns."""
    return """
INFO: Everything is fine.
DEBUG: All systems go.
VERBOSE: Just a regular day.
"""

def test_scan_log_file_basic_patterns(mock_log_content):
    """Test scanning a log file with default patterns."""
    # Mock rationale: Simulate reading a file from disk.
    with patch("builtins.open", mock_open(read_data=mock_log_content)):
        results = scan_log_file("dummy.log", DEFAULT_PATTERNS)

        assert "ERROR" in results
        assert results["ERROR"]["count"] == 2
        assert "ERROR: Failed to connect to database" in results["ERROR"]["unique_messages"]
        assert "ERROR: NullPointerException at com.example.App.doSomething(App.java:42)" in results["ERROR"]["unique_messages"]

        assert "WARNING" in results
        assert results["WARNING"]["count"] == 1
        assert "WARNING: Disk space low" in results["WARNING"]["unique_messages"]

        assert "CRITICAL" in results
        assert results["CRITICAL"]["count"] == 1
        assert "CRITICAL: System meltdown imminent" in results["CRITICAL"]["unique_messages"]

        assert "Exception:" in results
        assert results["Exception:"]["count"] == 1

        assert "Traceback (most recent call last):" in results
        assert results["Traceback (most recent call last):"]["count"] == 1


def test_scan_log_file_custom_patterns():
    """Test scanning with custom patterns."""
    log_content = "ALERT: Intruder detected!\nINFO: Normal operation.\nALERT: System compromised."
    custom_patterns = [r"ALERT"]
    # Mock rationale: Simulate reading a file from disk.
    with patch("builtins.open", mock_open(read_data=log_content)):
        results = scan_log_file("custom.log", custom_patterns)

        assert "ALERT" in results
        assert results["ALERT"]["count"] == 2
        assert "ALERT: Intruder detected!" in results["ALERT"]["unique_messages"]
        assert "ALERT: System compromised." in results["ALERT"]["unique_messages"]
        assert len(results) == 1

def test_scan_log_file_empty_log(mock_empty_log_content):
    """Test scanning an empty log file."""
    # Mock rationale: Simulate reading an empty file.
    with patch("builtins.open", mock_open(read_data=mock_empty_log_content)):
        results = scan_log_file("empty.log", DEFAULT_PATTERNS)
        assert not results

def test_scan_log_file_no_matches(mock_no_match_log_content):
    """Test scanning a log file with no matching patterns."""
    # Mock rationale: Simulate reading a file with no relevant content.
    with patch("builtins.open", mock_open(read_data=mock_no_match_log_content)):
        results = scan_log_file("no_match.log", DEFAULT_PATTERNS)
        assert not results

def test_generate_summary_report_basic(mock_log_content):
    """Test generating a summary report."""
    # Mock rationale: Simulate the output of scan_log_file for report generation.
    mock_scan_results = {
        "dummy.log": scan_log_file("dummy.log", DEFAULT_PATTERNS)
    }
    
    # Mock rationale: Fix the datetime for deterministic report generation.
    with patch('luminator.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2023, 1, 1, 10, 0, 0)
        mock_dt.strftime.side_effect = lambda fmt: datetime(2023, 1, 1, 10, 0, 0).strftime(fmt)
        report = generate_summary_report(mock_scan_results, output_file=None)

    assert "Nightly Log Luminator Report" in report
    assert "Generated on: 2023-01-01 10:00:00" in report
    assert "Total patterns detected: 6" in report 
    assert "File: `dummy.log`" in report
    assert "Pattern: `ERROR` (Count: 2)" in report
    assert "- `ERROR: Failed to connect to database` (x1)" in report
    assert "- `ERROR: NullPointerException at com.example.App.doSomething(App.java:42)` (x1)" in report
    assert "Pattern: `WARNING` (Count: 1)" in report
    assert "Pattern: `CRITICAL` (Count: 1)" in report
    assert "Pattern: `Exception:` (Count: 1)" in report
    assert "Pattern: `Traceback (most recent call last):` (Count: 1)" in report


def test_generate_summary_report_no_results():
    """Test generating a report with no scan results."""
    # Mock rationale: Fix the datetime for deterministic report generation.
    with patch('luminator.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2023, 1, 1, 10, 0, 0)
        mock_dt.strftime.side_effect = lambda fmt: datetime(2023, 1, 1, 10, 0, 0).strftime(fmt)
        report = generate_summary_report({}, output_file=None)

    assert "No relevant patterns found across scanned logs. All clear!" in report
    assert "Total patterns detected:" not in report # Ensure this line is not present

def test_generate_summary_report_output_file():
    """Test saving the report to a file."""
    mock_scan_results = {
        "dummy.log": {
            "ERROR": {"count": 1, "unique_messages": {"ERROR: Test error": 1}}
        }
    }
    mock_output_file = "test_report.md"

    # Mock rationale: Simulate writing to a file.
    with patch("builtins.open", mock_open()) as mocked_file_open, \
         patch('luminator.datetime') as mock_dt, \
         patch('builtins.print') as mock_print: # Mock print to avoid actual console output during test
        mock_dt.now.return_value = datetime(2023, 1, 1, 10, 0, 0)
        mock_dt.strftime.side_effect = lambda fmt: datetime(2023, 1, 1, 10, 0, 0).strftime(fmt)
        generate_summary_report(mock_scan_results, output_file=mock_output_file)

        mocked_file_open.assert_called_once_with(mock_output_file, 'w', encoding='utf-8')
        mocked_file_open().write.assert_called_once()
        mock_print.assert_called_with(f"Report saved to {mock_output_file}")

# Mock rationale: We need to simulate command-line arguments and file system structure
# without actually interacting with the real OS.
@patch('argparse.ArgumentParser.parse_args')
@patch('luminator.scan_log_file')
@patch('luminator.generate_summary_report')
@patch('os.path.isfile')
@patch('os.path.isdir')
@patch('os.walk')
@patch('builtins.print') # Mock print to avoid actual console output during test
def test_main_single_file(mock_print, mock_os_walk, mock_os_isdir, mock_os_isfile, 
                          mock_generate_summary_report, mock_scan_log_file, mock_parse_args):
    """Test main function with a single log file."""
    mock_parse_args.return_value = argparse.Namespace(
        path="test.log",
        output_file=None,
        patterns=DEFAULT_PATTERNS
    )
    mock_os_isfile.return_value = True
    mock_os_isdir.return_value = False
    mock_scan_log_file.return_value = {"ERROR": {"count": 1, "unique_messages": {"Test error": 1}}}

    main()

    mock_scan_log_file.assert_called_once_with("test.log", DEFAULT_PATTERNS)
    mock_generate_summary_report.assert_called_once()
    assert "test.log" in mock_generate_summary_report.call_args[0][0]

@patch('argparse.ArgumentParser.parse_args')
@patch('luminator.scan_log_file')
@patch('luminator.generate_summary_report')
@patch('os.path.isfile')
@patch('os.path.isdir')
@patch('os.walk')
@patch('builtins.print') # Mock print to avoid actual console output during test
def test_main_directory(mock_print, mock_os_walk, mock_os_isdir, mock_os_isfile, 
                        mock_generate_summary_report, mock_scan_log_file, mock_parse_args):
    """Test main function with a directory of log files."""
    mock_parse_args.return_value = argparse.Namespace(
        path="logs/",
        output_file="report.md",
        patterns=DEFAULT_PATTERNS
    )
    mock_os_isfile.return_value = False
    mock_os_isdir.return_value = True
    # Mock rationale: Simulate directory structure and files within it.
    mock_os_walk.return_value = [
        ("logs/", [], ["app.log", "auth.txt", "config.json"])
    ]
    mock_scan_log_file.side_effect = [
        {"ERROR": {"count": 1, "unique_messages": {"App error": 1}}},
        {"WARNING": {"count": 1, "unique_messages": {"Auth warning": 1}}},
        {} # config.json should not be processed
    ]

    main()

    assert mock_scan_log_file.call_count == 2 # app.log and auth.txt
    mock_scan_log_file.assert_any_call(os.path.join("logs/", "app.log"), DEFAULT_PATTERNS)
    mock_scan_log_file.assert_any_call(os.path.join("logs/", "auth.txt"), DEFAULT_PATTERNS)
    mock_generate_summary_report.assert_called_once()
    assert "logs/app.log" in mock_generate_summary_report.call_args[0][0]
    assert "logs/auth.txt" in mock_generate_summary_report.call_args[0][0]
    assert mock_generate_summary_report.call_args[0][1] == "report.md"

@patch('argparse.ArgumentParser.parse_args')
@patch('os.path.isfile')
@patch('os.path.isdir')
@patch('builtins.print')
@patch('sys.exit') # Mock sys.exit to prevent actual exit during test
def test_main_invalid_path(mock_sys_exit, mock_print, mock_os_isdir, mock_os_isfile, mock_parse_args):
    """Test main function with an invalid path."""
    mock_parse_args.return_value = argparse.Namespace(
        path="nonexistent/",
        output_file=None,
        patterns=DEFAULT_PATTERNS
    )
    mock_os_isfile.return_value = False
    mock_os_isdir.return_value = False

    main()

    mock_print.assert_called_with("Error: Path 'nonexistent/' is neither a file nor a directory.")
    mock_sys_exit.assert_called_once_with(1)
