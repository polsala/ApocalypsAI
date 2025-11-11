import pytest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Mock rationale: We need to simulate file system interactions (os.walk, os.stat)
# and time-related functions (time.time) without actually touching the disk
# or relying on the system's current time, to ensure deterministic and offline tests.

# Import the function to be tested
from src.anomaly_detector import find_temporal_anomalies

# Define a consistent current time for testing
TEST_CURRENT_TIME_EPOCH = datetime(2023, 10, 27, 10, 0, 0).timestamp()

@pytest.fixture
def mock_os_walk():
    """Mocks os.walk to simulate a directory structure."""
    with patch('os.walk') as mock_walk:
        yield mock_walk

@pytest.fixture
def mock_os_stat():
    """Mocks os.stat to return custom stat_result objects."""
    with patch('os.stat') as mock_stat:
        yield mock_stat

@pytest.fixture
def mock_time_time():
    """Mocks time.time to return a fixed current time."""
    with patch('time.time', return_value=TEST_CURRENT_TIME_EPOCH) as mock_time:
        yield mock_time

@pytest.fixture
def mock_os_path_isdir():
    """Mocks os.path.isdir to simulate directory existence."""
    with patch('os.path.isdir', return_value=True) as mock_isdir:
        yield mock_isdir

class MockStatResult:
    """A mock object to simulate os.stat_result."""
    def __init__(self, mtime, ctime):
        self.st_mtime = mtime
        self.st_ctime = ctime

def test_no_anomalies(mock_os_walk, mock_os_stat, mock_time_time, mock_os_path_isdir):
    # Mock rationale: Simulate a clean directory with no anomalies.
    mock_os_walk.return_value = [
        ('/mock/path', [], ['file1.txt', 'file2.log'])
    ]
    mock_os_stat.side_effect = [
        MockStatResult(TEST_CURRENT_TIME_EPOCH - 3600, TEST_CURRENT_TIME_EPOCH - 7200), # file1.txt: mtime > ctime, both in past
        MockStatResult(TEST_CURRENT_TIME_EPOCH - 100, TEST_CURRENT_TIME_EPOCH - 200)  # file2.log: mtime > ctime, both in past
    ]

    results = find_temporal_anomalies('/mock/path')

    assert not results['future_timestamps']
    assert not results['retrograde_modifications']

def test_future_mtime_anomaly(mock_os_walk, mock_os_stat, mock_time_time, mock_os_path_isdir):
    # Mock rationale: Simulate a file with a modification time in the future.
    future_mtime = TEST_CURRENT_TIME_EPOCH + 120 # 2 minutes in the future
    mock_os_walk.return_value = [
        ('/mock/path', [], ['future_file.txt'])
    ]
    mock_os_stat.return_value = MockStatResult(future_mtime, TEST_CURRENT_TIME_EPOCH - 100)

    results = find_temporal_anomalies('/mock/path', future_threshold_seconds=60)

    assert len(results['future_timestamps']) == 1
    assert results['future_timestamps'][0]['file'] == '/mock/path/future_file.txt'
    assert results['future_timestamps'][0]['type'] == 'future_mtime'

def test_future_ctime_anomaly(mock_os_walk, mock_os_stat, mock_time_time, mock_os_path_isdir):
    # Mock rationale: Simulate a file with a creation time in the future.
    future_ctime = TEST_CURRENT_TIME_EPOCH + 120 # 2 minutes in the future
    mock_os_walk.return_value = [
        ('/mock/path', [], ['future_created_file.txt'])
    ]
    mock_os_stat.return_value = MockStatResult(TEST_CURRENT_TIME_EPOCH - 100, future_ctime)

    results = find_temporal_anomalies('/mock/path', future_threshold_seconds=60)

    assert len(results['future_timestamps']) == 1
    assert results['future_timestamps'][0]['file'] == '/mock/path/future_created_file.txt'
    assert results['future_timestamps'][0]['type'] == 'future_ctime'

def test_retrograde_modification_anomaly(mock_os_walk, mock_os_stat, mock_time_time, mock_os_path_isdir):
    # Mock rationale: Simulate a file where mtime is older than ctime.
    retro_mtime = TEST_CURRENT_TIME_EPOCH - 500 # mtime is older
    normal_ctime = TEST_CURRENT_TIME_EPOCH - 200
    mock_os_walk.return_value = [
        ('/mock/path', [], ['retro_file.txt'])
    ]
    mock_os_stat.return_value = MockStatResult(retro_mtime, normal_ctime)

    results = find_temporal_anomalies('/mock/path')

    assert len(results['retrograde_modifications']) == 1
    assert results['retrograde_modifications'][0]['file'] == '/mock/path/retro_file.txt'
    assert datetime.fromisoformat(results['retrograde_modifications'][0]['mtime']).timestamp() == retro_mtime
    assert datetime.fromisoformat(results['retrograde_modifications'][0]['ctime']).timestamp() == normal_ctime

def test_multiple_anomalies(mock_os_walk, mock_os_stat, mock_time_time, mock_os_path_isdir):
    # Mock rationale: Simulate a scenario with multiple types of anomalies across different files.
    future_mtime = TEST_CURRENT_TIME_EPOCH + 120
    future_ctime = TEST_CURRENT_TIME_EPOCH + 150
    retro_mtime = TEST_CURRENT_TIME_EPOCH - 500
    normal_ctime = TEST_CURRENT_TIME_EPOCH - 200

    mock_os_walk.return_value = [
        ('/mock/path', [], ['file_future_mtime.txt', 'file_retro.log', 'file_future_ctime.py'])
    ]
    mock_os_stat.side_effect = [
        MockStatResult(future_mtime, TEST_CURRENT_TIME_EPOCH - 100), # future_mtime
        MockStatResult(retro_mtime, normal_ctime), # retrograde
        MockStatResult(TEST_CURRENT_TIME_EPOCH - 50, future_ctime) # future_ctime
    ]

    results = find_temporal_anomalies('/mock/path', future_threshold_seconds=60)

    assert len(results['future_timestamps']) == 2
    assert any(a['file'] == '/mock/path/file_future_mtime.txt' for a in results['future_timestamps'])
    assert any(a['file'] == '/mock/path/file_future_ctime.py' for a in results['future_timestamps'])
    assert len(results['retrograde_modifications']) == 1
    assert results['retrograde_modifications'][0]['file'] == '/mock/path/file_retro.log'

def test_os_error_handling(mock_os_walk, mock_os_stat, mock_time_time, mock_os_path_isdir, capsys):
    # Mock rationale: Simulate an OSError during os.stat to ensure robust error handling.
    mock_os_walk.return_value = [
        ('/mock/path', [], ['unreadable_file.txt'])
    ]
    mock_os_stat.side_effect = OSError("Permission denied")

    results = find_temporal_anomalies('/mock/path')

    assert not results['future_timestamps']
    assert not results['retrograde_modifications']
    captured = capsys.readouterr()
    assert "Warning: Could not access '/mock/path/unreadable_file.txt': Permission denied" in captured.out

def test_invalid_path(mock_os_path_isdir, capsys):
    # Mock rationale: Simulate an invalid directory path.
    mock_os_path_isdir.return_value = False

    results = find_temporal_anomalies('/nonexistent/path')

    assert not results['future_timestamps']
    assert not results['retrograde_modifications']
    captured = capsys.readouterr()
    assert "Error: Path '/nonexistent/path' is not a valid directory." in captured.out

def test_future_threshold_respected(mock_os_walk, mock_os_stat, mock_time_time, mock_os_path_isdir):
    # Mock rationale: Test that files just outside the threshold are flagged, but those inside are not.
    just_future_mtime = TEST_CURRENT_TIME_EPOCH + 50 # Within default 60s threshold
    very_future_mtime = TEST_CURRENT_TIME_EPOCH + 70 # Outside default 60s threshold

    mock_os_walk.return_value = [
        ('/mock/path', [], ['file_just_future.txt', 'file_very_future.txt'])
    ]
    mock_os_stat.side_effect = [
        MockStatResult(just_future_mtime, TEST_CURRENT_TIME_EPOCH - 100),
        MockStatResult(very_future_mtime, TEST_CURRENT_TIME_EPOCH - 100)
    ]

    results = find_temporal_anomalies('/mock/path', future_threshold_seconds=60)

    assert len(results['future_timestamps']) == 1
    assert results['future_timestamps'][0]['file'] == '/mock/path/file_very_future.txt'

    # Test with a custom threshold that includes 'file_just_future.txt'
    mock_os_stat.side_effect = [
        MockStatResult(just_future_mtime, TEST_CURRENT_TIME_EPOCH - 100),
        MockStatResult(very_future_mtime, TEST_CURRENT_TIME_EPOCH - 100)
    ]
    results_custom_threshold = find_temporal_anomalies('/mock/path', future_threshold_seconds=100)
    assert len(results_custom_threshold['future_timestamps']) == 2
    assert any(a['file'] == '/mock/path/file_just_future.txt' for a in results_custom_threshold['future_timestamps'])
    assert any(a['file'] == '/mock/path/file_very_future.txt' for a in results_custom_threshold['future_timestamps'])
