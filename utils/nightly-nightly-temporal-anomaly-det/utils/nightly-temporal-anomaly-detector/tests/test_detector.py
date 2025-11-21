import pytest
from unittest.mock import patch, MagicMock
import os
import datetime
import time

# Import the function to test
from src.detector import detect_anomalies

# Define a fixed current time for deterministic testing
FIXED_CURRENT_DATETIME = datetime.datetime(2023, 10, 27, 10, 0, 0)
FIXED_CURRENT_TIMESTAMP = FIXED_CURRENT_DATETIME.timestamp()

# Define a stale threshold for testing (e.g., 30 days)
STALE_THRESHOLD_DAYS = 30
STALE_THRESHOLD_SECONDS = STALE_THRESHOLD_DAYS * 24 * 60 * 60

# Helper to create mock file system structure and mtimes
def setup_mock_filesystem(files_with_mtimes):
    """
    Prepares mock return values for os.walk and os.path.getmtime.
    files_with_mtimes: dict where key is full path, value is mtime (timestamp).
    Returns: (mock_walk_return_value, mock_getmtime_side_effect_func)
    """
    mock_walk_result = []
    dirs = {}
    for path, mtime in files_with_mtimes.items():
        dirname, basename = os.path.split(path)
        if dirname not in dirs:
            dirs[dirname] = {'files': [], 'dirs': []} # (dirpath, dirnames, filenames)
        dirs[dirname]['files'].append(basename)

    # Convert dirs dict to os.walk format
    for dirname, content in dirs.items():
        mock_walk_result.append((dirname, content['dirs'], content['files']))

    # Create a side effect function for os.path.getmtime
    def getmtime_side_effect(path):
        if path in files_with_mtimes:
            return files_with_mtimes[path]
        raise FileNotFoundError(f"No such file or directory: '{path}'")

    return mock_walk_result, getmtime_side_effect

@patch('os.path.getmtime')
@patch('os.walk')
def test_no_anomalies(mock_walk, mock_getmtime):
    # Mock rationale: Simulate a file system with no anomalies.
    # All files have mtimes before the current time and within the stale threshold.
    mock_files = {
        '/repo/file1.txt': (FIXED_CURRENT_DATETIME - datetime.timedelta(days=10)).timestamp(),
        '/repo/subdir/file2.py': (FIXED_CURRENT_DATETIME - datetime.timedelta(days=20)).timestamp(),
    }
    mock_walk_return, mock_getmtime_side_effect = setup_mock_filesystem(mock_files)
    mock_walk.return_value = mock_walk_return
    mock_getmtime.side_effect = mock_getmtime_side_effect

    results = detect_anomalies('/repo', FIXED_CURRENT_TIMESTAMP, STALE_THRESHOLD_SECONDS)
    assert not results["future_modified_files"]
    assert not results["stale_files"]

@patch('os.path.getmtime')
@patch('os.walk')
def test_future_modified_files(mock_walk, mock_getmtime):
    # Mock rationale: Simulate files with modification times in the future.
    # This tests the detection of future_modified_files.
    mock_files = {
        '/repo/future_file.log': (FIXED_CURRENT_DATETIME + datetime.timedelta(hours=1)).timestamp(),
        '/repo/normal_file.txt': (FIXED_CURRENT_DATETIME - datetime.timedelta(days=5)).timestamp(),
    }
    mock_walk_return, mock_getmtime_side_effect = setup_mock_filesystem(mock_files)
    mock_walk.return_value = mock_walk_return
    mock_getmtime.side_effect = mock_getmtime_side_effect

    results = detect_anomalies('/repo', FIXED_CURRENT_TIMESTAMP, STALE_THRESHOLD_SECONDS)
    assert results["future_modified_files"] == ['/repo/future_file.log']
    assert not results["stale_files"]

@patch('os.path.getmtime')
@patch('os.walk')
def test_stale_files(mock_walk, mock_getmtime):
    # Mock rationale: Simulate files with modification times older than the stale threshold.
    # This tests the detection of stale_files.
    mock_files = {
        '/repo/stale_doc.md': (FIXED_CURRENT_DATETIME - datetime.timedelta(days=STALE_THRESHOLD_DAYS + 10)).timestamp(),
        '/repo/recent_code.py': (FIXED_CURRENT_DATETIME - datetime.timedelta(days=15)).timestamp(),
    }
    mock_walk_return, mock_getmtime_side_effect = setup_mock_filesystem(mock_files)
    mock_walk.return_value = mock_walk_return
    mock_getmtime.side_effect = mock_getmtime_side_effect

    results = detect_anomalies('/repo', FIXED_CURRENT_TIMESTAMP, STALE_THRESHOLD_SECONDS)
    assert not results["future_modified_files"]
    assert results["stale_files"] == ['/repo/stale_doc.md']

@patch('os.path.getmtime')
@patch('os.walk')
def test_mixed_anomalies(mock_walk, mock_getmtime):
    # Mock rationale: Simulate a scenario with both future and stale files.
    # This ensures both anomaly types are detected correctly.
    mock_files = {
        '/repo/future_report.pdf': (FIXED_CURRENT_DATETIME + datetime.timedelta(minutes=30)).timestamp(),
        '/repo/old_config.ini': (FIXED_CURRENT_DATETIME - datetime.timedelta(days=STALE_THRESHOLD_DAYS + 60)).timestamp(),
        '/repo/current_script.sh': (FIXED_CURRENT_DATETIME - datetime.timedelta(days=1)).timestamp(),
    }
    mock_walk_return, mock_getmtime_side_effect = setup_mock_filesystem(mock_files)
    mock_walk.return_value = mock_walk_return
    mock_getmtime.side_effect = mock_getmtime_side_effect

    results = detect_anomalies('/repo', FIXED_CURRENT_TIMESTAMP, STALE_THRESHOLD_SECONDS)
    assert results["future_modified_files"] == ['/repo/future_report.pdf']
    assert results["stale_files"] == ['/repo/old_config.ini']

@patch('os.path.getmtime')
@patch('os.walk')
def test_empty_directory(mock_walk, mock_getmtime):
    # Mock rationale: Simulate an empty directory to ensure no errors and empty results.
    mock_walk.return_value = []
    # getmtime should not be called if walk is empty, but we set a side_effect for robustness
    mock_getmtime.side_effect = FileNotFoundError # Should not be called if walk is empty

    results = detect_anomalies('/empty_repo', FIXED_CURRENT_TIMESTAMP, STALE_THRESHOLD_SECONDS)
    assert not results["future_modified_files"]
    assert not results["stale_files"]

@patch('os.path.getmtime')
@patch('os.walk')
def test_file_disappears_during_scan(mock_walk, mock_getmtime):
    # Mock rationale: Simulate a race condition where a file is deleted between os.walk and os.path.getmtime.
    # The utility should handle this gracefully without crashing, skipping the disappeared file.
    mock_files_initial = {
        '/repo/existing_file.txt': (FIXED_CURRENT_DATETIME - datetime.timedelta(days=10)).timestamp(),
        '/repo/deleted_file.tmp': (FIXED_CURRENT_DATETIME - datetime.timedelta(days=10)).timestamp(),
    }

    # os.walk will report both files
    mock_walk_return, _ = setup_mock_filesystem(mock_files_initial)
    mock_walk.return_value = mock_walk_return

    # But os.path.getmtime will raise FileNotFoundError for 'deleted_file.tmp'
    def getmtime_side_effect(path):
        if path == '/repo/deleted_file.tmp':
            raise FileNotFoundError
        return mock_files_initial[path]

    mock_getmtime.side_effect = getmtime_side_effect

    results = detect_anomalies('/repo', FIXED_CURRENT_TIMESTAMP, STALE_THRESHOLD_SECONDS)
    assert not results["future_modified_files"]
    assert not results["stale_files"] # No anomalies from existing_file, deleted_file is ignored.
