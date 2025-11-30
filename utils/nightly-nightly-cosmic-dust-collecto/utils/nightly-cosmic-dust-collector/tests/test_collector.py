import pytest
import os
import datetime
from unittest.mock import patch, MagicMock
from src.collector import find_cosmic_dust

# Define a fixed current time for deterministic age calculations
FIXED_NOW = datetime.datetime(2023, 10, 26, 12, 0, 0)

# Mock rationale: os.walk, os.stat, os.path.isdir, and os.path.isfile are file system operations
# that would make tests non-deterministic and dependent on the actual file system state.
# Mocking them allows us to simulate various directory structures and file properties
# without creating real files, ensuring tests are fast, isolated, and repeatable.
# datetime.datetime.now() is mocked to ensure age calculations are deterministic.

@pytest.fixture
def mock_os_walk():
    """Fixture to mock os.walk for various test scenarios."""
    with patch('os.walk') as mock_walk:
        yield mock_walk

@pytest.fixture
def mock_os_stat():
    """Fixture to mock os.stat for various test scenarios."""
    with patch('os.stat') as mock_stat:
        yield mock_stat

@pytest.fixture
def mock_os_path_isdir():
    """Fixture to mock os.path.isdir for various test scenarios."""
    with patch('os.path.isdir') as mock_isdir:
        yield mock_isdir

@pytest.fixture
def mock_os_path_isfile():
    """Fixture to mock os.path.isfile for various test scenarios."""
    with patch('os.path.isfile') as mock_isfile:
        yield mock_isfile

@pytest.fixture(autouse=True)
def mock_datetime_now():
    """Fixture to mock datetime.datetime.now() for deterministic age calculations."""
    with patch('datetime.datetime') as mock_dt:
        mock_dt.now.return_value = FIXED_NOW
        # Ensure other datetime methods are not mocked away
        mock_dt.fromtimestamp = datetime.datetime.fromtimestamp
        mock_dt.timedelta = datetime.timedelta
        # Also ensure the class itself can be called to create new datetime objects
        mock_dt.side_effect = lambda *args, **kwargs: datetime.datetime(*args, **kwargs)
        yield mock_dt

# --- Test Cases ---

def test_no_dust_found(mock_os_walk, mock_os_stat, mock_os_path_isdir, mock_os_path_isfile):
    mock_os_path_isdir.return_value = True
    mock_os_walk.return_value = [
        ('/test_dir', [], ['large_recent.txt', 'small_recent.log'])
    ]
    mock_os_path_isfile.return_value = True

    # Mock stat for files:
    # large_recent.txt: 100KB, 1 day old (not dust due to size)
    # small_recent.log: 5KB, 1 day old (not dust due to age)
    file_stats = {
        '/test_dir/large_recent.txt': MagicMock(st_size=100 * 1024, st_mtime=(FIXED_NOW - datetime.timedelta(days=1)).timestamp()),
        '/test_dir/small_recent.log': MagicMock(st_size=5 * 1024, st_mtime=(FIXED_NOW - datetime.timedelta(days=1)).timestamp()),
    }
    mock_os_stat.side_effect = lambda p: file_stats[p]

    dust = find_cosmic_dust('/test_dir', max_size_kb=10, min_age_days=30)
    assert len(dust) == 0

def test_dust_found_single_file(mock_os_walk, mock_os_stat, mock_os_path_isdir, mock_os_path_isfile):
    mock_os_path_isdir.return_value = True
    mock_os_walk.return_value = [
        ('/test_dir', [], ['dusty_old.txt'])
    ]
    mock_os_path_isfile.return_value = True

    # dusty_old.txt: 5KB, 60 days old (is dust)
    file_stats = {
        '/test_dir/dusty_old.txt': MagicMock(st_size=5 * 1024, st_mtime=(FIXED_NOW - datetime.timedelta(days=60)).timestamp()),
    }
    mock_os_stat.side_effect = lambda p: file_stats[p]

    dust = find_cosmic_dust('/test_dir', max_size_kb=10, min_age_days=30)
    assert len(dust) == 1
    assert dust[0]['path'] == '/test_dir/dusty_old.txt'
    assert dust[0]['size_bytes'] == 5 * 1024
    assert dust[0]['last_modified'] == (FIXED_NOW - datetime.timedelta(days=60)).isoformat(timespec='seconds')

def test_dust_found_multiple_files_and_dirs(mock_os_walk, mock_os_stat, mock_os_path_isdir, mock_os_path_isfile):
    mock_os_path_isdir.return_value = True
    mock_os_walk.return_value = [
        ('/test_dir', ['subdir1', 'subdir2'], ['recent.txt', 'dusty1.log']),
        ('/test_dir/subdir1', [], ['large.bin', 'dusty2.tmp']),
        ('/test_dir/subdir2', [], ['empty.txt'])
    ]
    mock_os_path_isfile.return_value = True

    # Define file stats:
    # /test_dir/recent.txt: 20KB, 10 days old (not dust - too recent)
    # /test_dir/dusty1.log: 2KB, 40 days old (dust)
    # /test_dir/subdir1/large.bin: 50KB, 50 days old (not dust - too large)
    # /test_dir/subdir1/dusty2.tmp: 8KB, 90 days old (dust)
    # /test_dir/subdir2/empty.txt: 0KB, 100 days old (dust)
    file_stats = {
        '/test_dir/recent.txt': MagicMock(st_size=20 * 1024, st_mtime=(FIXED_NOW - datetime.timedelta(days=10)).timestamp()),
        '/test_dir/dusty1.log': MagicMock(st_size=2 * 1024, st_mtime=(FIXED_NOW - datetime.timedelta(days=40)).timestamp()),
        '/test_dir/subdir1/large.bin': MagicMock(st_size=50 * 1024, st_mtime=(FIXED_NOW - datetime.timedelta(days=50)).timestamp()),
        '/test_dir/subdir1/dusty2.tmp': MagicMock(st_size=8 * 1024, st_mtime=(FIXED_NOW - datetime.timedelta(days=90)).timestamp()),
        '/test_dir/subdir2/empty.txt': MagicMock(st_size=0, st_mtime=(FIXED_NOW - datetime.timedelta(days=100)).timestamp()),
    }
    mock_os_stat.side_effect = lambda p: file_stats[p]

    dust = find_cosmic_dust('/test_dir', max_size_kb=10, min_age_days=30)
    assert len(dust) == 3
    dust_paths = {item['path'] for item in dust}
    assert '/test_dir/dusty1.log' in dust_paths
    assert '/test_dir/subdir1/dusty2.tmp' in dust_paths
    assert '/test_dir/subdir2/empty.txt' in dust_paths

def test_invalid_path(mock_os_path_isdir, capsys):
    mock_os_path_isdir.return_value = False
    dust = find_cosmic_dust('/non_existent_dir')
    assert len(dust) == 0
    captured = capsys.readouterr()
    assert "Error: Path '/non_existent_dir' is not a valid directory." in captured.out

def test_os_error_during_scan(mock_os_walk, mock_os_stat, mock_os_path_isdir, mock_os_path_isfile, capsys):
    mock_os_path_isdir.return_value = True
    mock_os_walk.return_value = [
        ('/test_dir', [], ['good_file.txt', 'bad_file.txt'])
    ]
    mock_os_path_isfile.return_value = True

    # good_file.txt: 1KB, 40 days old (dust)
    # bad_file.txt: raises OSError
    file_stats = {
        '/test_dir/good_file.txt': MagicMock(st_size=1 * 1024, st_mtime=(FIXED_NOW - datetime.timedelta(days=40)).timestamp()),
    }
    def stat_side_effect(path):
        if path == '/test_dir/bad_file.txt':
            raise OSError("Permission denied")
        return file_stats[path]

    mock_os_stat.side_effect = stat_side_effect

    dust = find_cosmic_dust('/test_dir', max_size_kb=10, min_age_days=30)
    assert len(dust) == 1
    assert dust[0]['path'] == '/test_dir/good_file.txt'

    captured = capsys.readouterr()
    assert "Warning: Could not access file '/test_dir/bad_file.txt': Permission denied" in captured.out

def test_file_not_regular_file(mock_os_walk, mock_os_stat, mock_os_path_isdir, mock_os_path_isfile):
    mock_os_path_isdir.return_value = True
    mock_os_walk.return_value = [
        ('/test_dir', [], ['symlink.txt', 'dusty.txt'])
    ]
    # Mock symlink.txt as not a regular file, dusty.txt as a regular file
    mock_os_path_isfile.side_effect = lambda p: p == '/test_dir/dusty.txt'

    # dusty.txt: 1KB, 40 days old (dust)
    file_stats = {
        '/test_dir/dusty.txt': MagicMock(st_size=1 * 1024, st_mtime=(FIXED_NOW - datetime.timedelta(days=40)).timestamp()),
    }
    mock_os_stat.side_effect = lambda p: file_stats[p]

    dust = find_cosmic_dust('/test_dir', max_size_kb=10, min_age_days=30)
    assert len(dust) == 1
    assert dust[0]['path'] == '/test_dir/dusty.txt'
    assert '/test_dir/symlink.txt' not in [d['path'] for d in dust]
