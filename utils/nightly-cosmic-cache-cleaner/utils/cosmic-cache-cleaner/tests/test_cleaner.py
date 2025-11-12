import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import platform
import datetime
import tempfile
import shutil

# Import the functions from the cleaner script
from utils.cosmic_cache_cleaner.src.cleaner import (
    get_cache_paths,
    scan_directory,
    generate_report,
    delete_files,
    format_size
)

class TestCosmicCacheCleaner(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for mock file system operations
        self.temp_dir = tempfile.mkdtemp()
        self.original_expanduser = os.path.expanduser
        os.path.expanduser = lambda path: path.replace('~', self.temp_dir)

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.temp_dir)
        os.path.expanduser = self.original_expanduser

    def _create_mock_file(self, path, size_bytes, mtime_timestamp):
        """Helper to create a mock file with specific size and modification time."""
        full_path = os.path.join(self.temp_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'wb') as f:
            f.write(b'\0' * size_bytes)
        os.utime(full_path, (mtime_timestamp, mtime_timestamp))
        return full_path

    @patch('platform.system', return_value='Windows')
    @patch('os.path.isdir', return_value=True)
    @patch.dict('os.environ', {'LOCALAPPDATA': 'C:\\Users\\test\\AppData\\Local', 'TEMP': 'C:\\Temp'})
    def test_get_cache_paths_windows(self, mock_isdir, mock_platform_system):
        # Mock rationale: `platform.system` determines OS, `os.path.isdir` checks path existence, `os.environ` provides env vars.
        paths = get_cache_paths()
        expected_paths = [
            'C:\\Users\\test\\AppData\\Local\\Temp',
            'C:\\Temp',
            'C:\\Users\\test\\AppData\\Local\\pip\\cache',
            'C:\\Users\\test\\AppData\\Local\\npm-cache'
        ]
        self.assertListEqual(sorted(paths), sorted(expected_paths))

    @patch('platform.system', return_value='Darwin')
    @patch('os.path.isdir', return_value=True)
    def test_get_cache_paths_macos(self, mock_isdir, mock_platform_system):
        # Mock rationale: `platform.system` determines OS, `os.path.isdir` checks path existence.
        paths = get_cache_paths()
        home_cache = os.path.join(self.temp_dir, 'Library', 'Caches')
        expected_paths = [
            home_cache,
            '/Library/Caches',
            os.path.join(home_cache, 'pip'),
            os.path.join(home_cache, 'npm')
        ]
        self.assertListEqual(sorted(paths), sorted(expected_paths))

    @patch('platform.system', return_value='Linux')
    @patch('os.path.isdir', return_value=True)
    @patch.dict('os.environ', {'XDG_CACHE_HOME': '/tmp/test_cache'})
    def test_get_cache_paths_linux(self, mock_isdir, mock_platform_system):
        # Mock rationale: `platform.system` determines OS, `os.path.isdir` checks path existence, `os.environ` provides env vars.
        paths = get_cache_paths()
        home_cache = os.path.join(self.temp_dir, '.cache')
        expected_paths = [
            '/tmp/test_cache',
            '/var/cache',
            '/tmp/test_cache/pip',
            '/tmp/test_cache/npm'
        ]
        self.assertListEqual(sorted(paths), sorted(expected_paths))

    @patch('os.walk')
    @patch('os.stat')
    @patch('os.path.exists', return_value=True)
    def test_scan_directory_age_filter(self, mock_exists, mock_stat, mock_walk):
        # Mock rationale: `os.walk` simulates directory traversal, `os.stat` provides file metadata, `os.path.exists` checks file presence.
        mock_walk.return_value = [
            ('/mock/path', [], ['old_file.log', 'new_file.log'])
        ]

        # Mock stat for old_file.log (older than 30 days)
        mock_stat.side_effect = [
            MagicMock(st_mtime=(datetime.datetime.now() - datetime.timedelta(days=40)).timestamp(), st_size=200 * 1024 * 1024), # Old, large
            MagicMock(st_mtime=(datetime.datetime.now() - datetime.timedelta(days=10)).timestamp(), st_size=50 * 1024 * 1024)  # New, small
        ]

        files = scan_directory('/mock/path', min_age_days=30, min_size_mb=100)
        self.assertEqual(len(files), 1)
        self.assertIn('old_file.log', files[0]['path'])

    @patch('os.walk')
    @patch('os.stat')
    @patch('os.path.exists', return_value=True)
    def test_scan_directory_size_filter(self, mock_exists, mock_stat, mock_walk):
        # Mock rationale: `os.walk` simulates directory traversal, `os.stat` provides file metadata, `os.path.exists` checks file presence.
        mock_walk.return_value = [
            ('/mock/path', [], ['large_file.zip', 'small_file.txt'])
        ]

        # Mock stat for large_file.zip (larger than 100MB)
        mock_stat.side_effect = [
            MagicMock(st_mtime=(datetime.datetime.now() - datetime.timedelta(days=10)).timestamp(), st_size=150 * 1024 * 1024), # New, large
            MagicMock(st_mtime=(datetime.datetime.now() - datetime.timedelta(days=40)).timestamp(), st_size=50 * 1024 * 1024)  # Old, small
        ]

        files = scan_directory('/mock/path', min_age_days=30, min_size_mb=100)
        self.assertEqual(len(files), 1)
        self.assertIn('large_file.zip', files[0]['path'])

    @patch('os.walk')
    @patch('os.stat')
    @patch('os.path.exists', return_value=True)
    def test_scan_directory_both_filters(self, mock_exists, mock_stat, mock_walk):
        # Mock rationale: `os.walk` simulates directory traversal, `os.stat` provides file metadata, `os.path.exists` checks file presence.
        mock_walk.return_value = [
            ('/mock/path', [], ['old_large.bin', 'new_large.bin', 'old_small.txt', 'new_small.txt'])
        ]

        now = datetime.datetime.now()
        # old_large.bin: old (40d), large (150MB) -> should be included
        # new_large.bin: new (10d), large (150MB) -> should be included (size filter)
        # old_small.txt: old (40d), small (50MB) -> should NOT be included (size filter)
        # new_small.txt: new (10d), small (50MB) -> should NOT be included
        mock_stat.side_effect = [
            MagicMock(st_mtime=(now - datetime.timedelta(days=40)).timestamp(), st_size=150 * 1024 * 1024),
            MagicMock(st_mtime=(now - datetime.timedelta(days=10)).timestamp(), st_size=150 * 1024 * 1024),
            MagicMock(st_mtime=(now - datetime.timedelta(days=40)).timestamp(), st_size=50 * 1024 * 1024),
            MagicMock(st_mtime=(now - datetime.timedelta(days=10)).timestamp(), st_size=50 * 1024 * 1024),
        ]

        files = scan_directory('/mock/path', min_age_days=30, min_size_mb=100)
        self.assertEqual(len(files), 2)
        self.assertIn('old_large.bin', files[0]['path'])
        self.assertIn('new_large.bin', files[1]['path'])

    def test_format_size(self):
        # Mock rationale: Pure function, no mocks needed.
        self.assertEqual(format_size(500), '0.5 KB')
        self.assertEqual(format_size(1024 * 1024 * 1.5), '1.5 MB')
        self.assertEqual(format_size(1024 * 1024 * 1024 * 2.3), '2.3 GB')

    @patch('builtins.print')
    def test_generate_report_empty(self, mock_print):
        # Mock rationale: `builtins.print` captures console output for verification.
        total_size = generate_report([])
        self.assertEqual(total_size, 0)
        mock_print.assert_any_call("No significant cosmic dust detected. Your system is sparkling clean! ✨")

    @patch('builtins.print')
    def test_generate_report_with_files(self, mock_print):
        # Mock rationale: `builtins.print` captures console output for verification.
        now = datetime.datetime.now()
        files = [
            {'path': '/mock/path/file1.log', 'size': 150 * 1024 * 1024, 'mtime': now - datetime.timedelta(days=40)},
            {'path': '/mock/path/file2.tmp', 'size': 200 * 1024 * 1024, 'mtime': now - datetime.timedelta(days=50)}
        ]
        total_size = generate_report(files)
        self.assertEqual(total_size, 350 * 1024 * 1024)
        mock_print.assert_any_call("Identified 2 pieces of space junk:\n")
        mock_print.assert_any_call(f"- /mock/path/file1.log (150.0 MB, last modified: {(now - datetime.timedelta(days=40)).strftime('%Y-%m-%d')})")
        mock_print.assert_any_call(f"Total estimated mass of cosmic dust to be purged: 350.0 MB")

    @patch('builtins.input', return_value='no')
    @patch('builtins.print')
    @patch('os.remove')
    def test_delete_files_aborted(self, mock_remove, mock_print, mock_input):
        # Mock rationale: `builtins.input` simulates user input, `builtins.print` captures console output, `os.remove` simulates file deletion.
        files = [{'path': '/mock/path/file.log', 'size': 100, 'mtime': datetime.datetime.now()}]
        delete_files(files)
        mock_remove.assert_not_called()
        mock_print.assert_any_call("Deletion aborted. Cosmic dust remains for now.\n")

    @patch('builtins.input', return_value='yes')
    @patch('builtins.print')
    @patch('os.remove')
    @patch('os.path.isfile', return_value=True)
    def test_delete_files_confirmed(self, mock_isfile, mock_remove, mock_print, mock_input):
        # Mock rationale: `builtins.input` simulates user input, `builtins.print` captures console output, `os.remove` simulates file deletion, `os.path.isfile` ensures `os.remove` is called for files.
        files = [
            {'path': '/mock/path/file1.log', 'size': 100 * 1024 * 1024, 'mtime': datetime.datetime.now()},
            {'path': '/mock/path/file2.tmp', 'size': 50 * 1024 * 1024, 'mtime': datetime.datetime.now()}
        ]
        delete_files(files)
        self.assertEqual(mock_remove.call_count, 2)
        mock_remove.assert_any_call('/mock/path/file1.log')
        mock_remove.assert_any_call('/mock/path/file2.tmp')
        mock_print.assert_any_call("Orbital decay protocol complete. 2 items purged, 150.0 MB reclaimed.\n")

    @patch('builtins.print')
    @patch('os.remove')
    @patch('os.path.isfile', return_value=True)
    def test_delete_files_force(self, mock_isfile, mock_remove, mock_print):
        # Mock rationale: `builtins.print` captures console output, `os.remove` simulates file deletion, `os.path.isfile` ensures `os.remove` is called for files.
        files = [{'path': '/mock/path/file.log', 'size': 100, 'mtime': datetime.datetime.now()}]
        delete_files(files, force=True)
        mock_remove.assert_called_once_with('/mock/path/file.log')
        mock_print.assert_any_call("Orbital decay protocol complete. 1 items purged, 0.1 KB reclaimed.\n")

    @patch('builtins.print')
    @patch('os.remove')
    @patch('os.path.isfile', side_effect=[True, False]) # First file exists, second doesn't (e.g., deleted by another process)
    def test_delete_files_error_handling(self, mock_isfile, mock_remove, mock_print):
        # Mock rationale: `builtins.print` captures console output, `os.remove` simulates file deletion and raises OSError, `os.path.isfile` controls file existence.
        mock_remove.side_effect = [None, OSError("Permission denied")]
        files = [
            {'path': '/mock/path/file1.log', 'size': 100, 'mtime': datetime.datetime.now()},
            {'path': '/mock/path/file2.log', 'size': 200, 'mtime': datetime.datetime.now()}
        ]
        delete_files(files, force=True)
        self.assertEqual(mock_remove.call_count, 2)
        mock_print.assert_any_call("🌌 Error purging /mock/path/file2.log: Permission denied", file=sys.stderr)
        mock_print.assert_any_call("Orbital decay protocol complete. 1 items purged, 0.1 KB reclaimed.\n")

    @patch('shutil.rmtree')
    @patch('os.remove')
    @patch('os.path.isfile', return_value=False)
    @patch('os.path.isdir', return_value=True)
    def test_delete_files_directory(self, mock_isdir, mock_isfile, mock_remove, mock_rmtree):
        # Mock rationale: `shutil.rmtree` simulates directory deletion, `os.remove` is not called, `os.path.isfile` and `os.path.isdir` control path type.
        files = [{'path': '/mock/path/empty_dir', 'size': 0, 'mtime': datetime.datetime.now()}]
        delete_files(files, force=True)
        mock_rmtree.assert_called_once_with('/mock/path/empty_dir')
        mock_remove.assert_not_called()
