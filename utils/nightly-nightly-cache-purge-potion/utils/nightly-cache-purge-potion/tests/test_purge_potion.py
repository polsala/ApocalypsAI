import pytest
import sys
import os
import shutil
from unittest.mock import patch, MagicMock
from pathlib import Path

# Import the functions to be tested
from src.purge_potion import get_cache_paths, purge_directory, main

@pytest.fixture
def mock_home_dir(tmp_path):
    """Fixture to mock Path.home() to a temporary directory."""
    original_home = Path.home
    with patch('pathlib.Path.home', return_value=tmp_path):
        yield tmp_path
    Path.home = original_home # Restore original to prevent side effects

@pytest.fixture
def mock_os_environ():
    """Fixture to mock os.getenv for Windows paths."""
    with patch.dict(os.environ, {'LOCALAPPDATA': 'C:\\Users\\test\\AppData\\Local', 'TEMP': 'C:\\Users\\test\\AppData\\Local\\Temp'}, clear=True):
        yield

@pytest.fixture
def mock_path_exists():
    """Fixture to mock Path.exists() to always return True for testing purposes."""
    with patch('pathlib.Path.exists') as mock_exists:
        yield mock_exists

@pytest.fixture
def mock_path_is_dir():
    """Fixture to mock Path.is_dir() to always return True for testing purposes."""
    with patch('pathlib.Path.is_dir') as mock_is_dir:
        yield mock_is_dir

@pytest.fixture
def mock_path_iterdir():
    """Fixture to mock Path.iterdir() to return a predefined list of mock items."""
    with patch('pathlib.Path.iterdir') as mock_iterdir:
        yield mock_iterdir

@pytest.fixture
def mock_shutil_rmtree():
    """Fixture to mock shutil.rmtree."""
    with patch('shutil.rmtree') as mock_rmtree:
        yield mock_rmtree

@pytest.fixture
def mock_os_remove():
    """Fixture to mock os.remove."""
    with patch('os.remove') as mock_remove:
        yield mock_remove

# --- Test get_cache_paths function ---

def test_get_cache_paths_linux(mock_home_dir, mock_path_exists):
    # Mock rationale: Simulate a Linux environment and ensure correct paths are identified.
    with patch('sys.platform', 'linux'):
        expected_paths = [
            mock_home_dir / '.cache',
            mock_home_dir / '.npm',
            mock_home_dir / '.pip' / 'cache',
            mock_home_dir / '.cargo' / 'registry' / 'cache',
            mock_home_dir / '.local' / 'share' / 'Trash',
        ]
        # Ensure all expected paths exist for the mock
        mock_path_exists.side_effect = lambda p: p in expected_paths or p.parent.exists() # Allow parent checks

        paths = get_cache_paths()
        assert sorted(paths) == sorted(expected_paths)

def test_get_cache_paths_macos(mock_home_dir, mock_path_exists):
    # Mock rationale: Simulate a macOS environment and ensure correct paths are identified.
    with patch('sys.platform', 'darwin'):
        expected_paths = [
            mock_home_dir / 'Library' / 'Caches',
            mock_home_dir / '.npm',
            mock_home_dir / '.pip' / 'cache',
            mock_home_dir / '.cargo' / 'registry' / 'cache',
            mock_home_dir / '.Trash',
        ]
        mock_path_exists.side_effect = lambda p: p in expected_paths or p.parent.exists()

        paths = get_cache_paths()
        assert sorted(paths) == sorted(expected_paths)

def test_get_cache_paths_windows(mock_home_dir, mock_os_environ, mock_path_exists):
    # Mock rationale: Simulate a Windows environment and ensure correct paths are identified.
    with patch('sys.platform', 'win32'):
        # These paths are constructed based on the mocked os.getenv in mock_os_environ
        expected_paths = [
            Path('C:\\Users\\test\\AppData\\Local') / 'Temp',
            Path('C:\\Users\\test\\AppData\\Local') / 'npm-cache',
            Path('C:\\Users\\test\\AppData\\Local\\Temp'), # From TEMP env var
            mock_home_dir / '.pip' / 'cache',
            mock_home_dir / '.cargo' / 'registry' / 'cache',
        ]
        mock_path_exists.side_effect = lambda p: p in expected_paths or p.parent.exists()

        paths = get_cache_paths()
        assert sorted(paths) == sorted(expected_paths)

def test_get_cache_paths_filters_non_existent(mock_home_dir, mock_path_exists):
    # Mock rationale: Ensure that only paths that actually exist are returned.
    with patch('sys.platform', 'linux'):
        # Only one path exists
        mock_path_exists.side_effect = lambda p: p == mock_home_dir / '.cache'

        paths = get_cache_paths()
        assert paths == [mock_home_dir / '.cache']

# --- Test purge_directory function ---

def test_purge_directory_dry_run(mock_path_is_dir, mock_path_iterdir, mock_shutil_rmtree, mock_os_remove):
    # Mock rationale: Verify that in dry-run mode, no actual deletion calls are made.
    mock_dir = Path('/mock/cache')
    mock_file1 = MagicMock(spec=Path, name='file1')
    mock_file1.is_dir.return_value = False
    mock_dir1 = MagicMock(spec=Path, name='dir1')
    mock_dir1.is_dir.return_value = True

    mock_path_iterdir.return_value = [mock_file1, mock_dir1]
    mock_path_is_dir.return_value = True # The target path is a directory

    purged_count = purge_directory(mock_dir, dry_run=True, verbose=True)

    assert purged_count == 2
    mock_shutil_rmtree.assert_not_called()
    mock_os_remove.assert_not_called()

def test_purge_directory_actual_purge(mock_path_is_dir, mock_path_iterdir, mock_shutil_rmtree, mock_os_remove):
    # Mock rationale: Verify that in actual purge mode, deletion calls are made for files and directories.
    mock_dir = Path('/mock/cache')
    mock_file1 = MagicMock(spec=Path, name='file1')
    mock_file1.is_dir.return_value = False
    mock_dir1 = MagicMock(spec=Path, name='dir1')
    mock_dir1.is_dir.return_value = True

    mock_path_iterdir.return_value = [mock_file1, mock_dir1]
    mock_path_is_dir.return_value = True

    purged_count = purge_directory(mock_dir, dry_run=False, verbose=True)

    assert purged_count == 2
    mock_shutil_rmtree.assert_called_once_with(mock_dir1)
    mock_os_remove.assert_called_once_with(mock_file1)

def test_purge_directory_handles_os_error(mock_path_is_dir, mock_path_iterdir, mock_shutil_rmtree, mock_os_remove, capsys):
    # Mock rationale: Ensure that OS errors during deletion are caught and reported, but the process continues.
    mock_dir = Path('/mock/cache')
    mock_file1 = MagicMock(spec=Path, name='file1')
    mock_file1.is_dir.return_value = False
    mock_dir1 = MagicMock(spec=Path, name='dir1')
    mock_dir1.is_dir.return_value = True

    mock_path_iterdir.return_value = [mock_file1, mock_dir1]
    mock_path_is_dir.return_value = True
    mock_shutil_rmtree.side_effect = OSError("Permission denied")
    mock_os_remove.side_effect = OSError("File in use")

    purged_count = purge_directory(mock_dir, dry_run=False, verbose=True)

    assert purged_count == 0 # No items successfully purged
    mock_shutil_rmtree.assert_called_once_with(mock_dir1)
    mock_os_remove.assert_called_once_with(mock_file1)
    captured = capsys.readouterr()
    assert "Error removing directory" in captured.err
    assert "Error removing file" in captured.err

def test_purge_directory_skips_non_dir(mock_path_is_dir, mock_path_iterdir, mock_shutil_rmtree, mock_os_remove):
    # Mock rationale: Ensure that if the target path is not a directory, it's skipped.
    mock_path_is_dir.return_value = False # The path itself is not a directory
    mock_dir = Path('/mock/file.txt')

    purged_count = purge_directory(mock_dir, dry_run=False, verbose=True)

    assert purged_count == 0
    mock_path_iterdir.assert_not_called()
    mock_shutil_rmtree.assert_not_called()
    mock_os_remove.assert_not_called()

# --- Test main function ---

def test_main_dry_run(mock_home_dir, mock_path_exists, mock_path_is_dir, mock_path_iterdir, mock_shutil_rmtree, mock_os_remove, capsys):
    # Mock rationale: Test the main execution flow with dry-run flag.
    # Simulate a Linux environment with one cache directory containing one file and one directory.
    with patch('sys.platform', 'linux'):
        mock_path_exists.side_effect = lambda p: p == mock_home_dir / '.cache' or p == mock_home_dir / '.npm'
        mock_path_is_dir.return_value = True # All paths are directories

        mock_file = MagicMock(spec=Path, name='mock_file')
        mock_file.is_dir.return_value = False
        mock_sub_dir = MagicMock(spec=Path, name='mock_sub_dir')
        mock_sub_dir.is_dir.return_value = True

        mock_path_iterdir.side_effect = [[mock_file, mock_sub_dir], []] # First cache has items, second is empty

        test_args = ['purge_potion.py', '--dry-run']
        with patch('sys.argv', test_args):
            main()

        captured = capsys.readouterr()
        assert "Dry Run (no changes will be made)" in captured.out
        assert "Would have purged 2 items from" in captured.out
        assert "Would have purged 0 items from" in captured.out
        assert "Would have purged a total of 2 items." in captured.out
        mock_shutil_rmtree.assert_not_called()
        mock_os_remove.assert_not_called()

def test_main_actual_purge(mock_home_dir, mock_path_exists, mock_path_is_dir, mock_path_iterdir, mock_shutil_rmtree, mock_os_remove, capsys):
    # Mock rationale: Test the main execution flow with actual purge.
    # Simulate a Linux environment with one cache directory containing one file and one directory.
    with patch('sys.platform', 'linux'):
        mock_path_exists.side_effect = lambda p: p == mock_home_dir / '.cache'
        mock_path_is_dir.return_value = True

        mock_file = MagicMock(spec=Path, name='mock_file')
        mock_file.is_dir.return_value = False
        mock_sub_dir = MagicMock(spec=Path, name='mock_sub_dir')
        mock_sub_dir.is_dir.return_value = True

        mock_path_iterdir.return_value = [mock_file, mock_sub_dir]

        test_args = ['purge_potion.py']
        with patch('sys.argv', test_args):
            main()

        captured = capsys.readouterr()
        assert "Actual Purge" in captured.out
        assert "Purged 2 items from" in captured.out
        assert "Purged a total of 2 items." in captured.out
        mock_shutil_rmtree.assert_called_once_with(mock_sub_dir)
        mock_os_remove.assert_called_once_with(mock_file)

def test_main_no_cache_paths(mock_home_dir, mock_path_exists, capsys):
    # Mock rationale: Test scenario where no cache paths are found.
    mock_path_exists.return_value = False # No paths exist

    test_args = ['purge_potion.py']
    with patch('sys.argv', test_args):
        main()

    captured = capsys.readouterr()
    assert "No common cache directories found for this operating system. Potion remains sealed." in captured.out
    assert "Potion complete!" not in captured.out # Should exit early
