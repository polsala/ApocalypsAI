import unittest
from unittest.mock import patch, MagicMock, call
import os
import sys
import shutil

# Import the functions from the purifier module
# Assuming purifier.py is in src/ and tests/ is at the same level as src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from purifier import get_cache_paths, get_dir_size, format_bytes, dry_run_purifier, clean_purifier, main

class TestPurifier(unittest.TestCase):

    @patch('os.path.expanduser', return_value='/home/user') # Mock rationale: Isolate from actual user home directory.
    @patch('os.path.isdir', return_value=True) # Mock rationale: Assume all constructed paths exist as directories for testing path generation.
    def test_get_cache_paths_linux(self, mock_isdir, mock_expanduser):
        with patch('sys.platform', 'linux'): # Mock rationale: Simulate Linux environment.
            paths = get_cache_paths()
            expected_paths = [
                '/home/user/.cache',
                '/home/user/.npm/_cacache',
                '/home/user/.cache/pip'
            ]
            self.assertListEqual(sorted(paths), sorted(expected_paths))

    @patch('os.path.expanduser', return_value='/Users/user') # Mock rationale: Isolate from actual user home directory.
    @patch('os.path.isdir', return_value=True) # Mock rationale: Assume all constructed paths exist as directories for testing path generation.
    def test_get_cache_paths_macos(self, mock_isdir, mock_expanduser):
        with patch('sys.platform', 'darwin'): # Mock rationale: Simulate macOS environment.
            paths = get_cache_paths()
            expected_paths = [
                '/Users/user/.cache',
                '/Users/user/Library/Caches',
                '/Users/user/.npm/_cacache',
                '/Users/user/.cache/pip'
            ]
            self.assertListEqual(sorted(paths), sorted(expected_paths))

    @patch('os.path.expanduser', return_value='C:\\Users\\user') # Mock rationale: Isolate from actual user home directory.
    @patch.dict(os.environ, {'TEMP': 'C:\\Temp', 'LOCALAPPDATA': 'C:\\Users\\user\\AppData\\Local', 'APPDATA': 'C:\\Users\\user\\AppData\\Roaming'}) # Mock rationale: Simulate Windows environment variables.
    @patch('os.path.isdir', return_value=True) # Mock rationale: Assume all constructed paths exist as directories for testing path generation.
    def test_get_cache_paths_windows(self, mock_isdir, mock_expanduser):
        with patch('sys.platform', 'win32'): # Mock rationale: Simulate Windows environment.
            paths = get_cache_paths()
            expected_paths = [
                'C:\\Temp',
                'C:\\Users\\user\\AppData\\Local\\Temp',
                'C:\\Users\\user\\AppData\\Local\\pip\\cache',
                'C:\\Users\\user\\AppData\\Roaming\\npm-cache'
            ]
            self.assertListEqual(sorted(paths), sorted(expected_paths))

    @patch('os.path.isdir', return_value=True) # Mock rationale: Simulate directory existence.
    @patch('os.walk') # Mock rationale: Control directory traversal for deterministic size calculation.
    @patch('os.path.getsize') # Mock rationale: Control file sizes for deterministic size calculation.
    @patch('os.path.islink', return_value=False) # Mock rationale: Assume no symlinks for simplicity.
    @patch('os.path.exists', return_value=True) # Mock rationale: Assume files exist for size calculation.
    def test_get_dir_size(self, mock_exists, mock_islink, mock_getsize, mock_walk, mock_isdir):
        # Simulate a directory structure:
        # /test_dir
        #   ├── file1.txt (100 bytes)
        #   ├── subdir/
        #   │   └── file2.txt (200 bytes)
        mock_walk.return_value = [
            ('/test_dir', ['subdir'], ['file1.txt']),
            ('/test_dir/subdir', [], ['file2.txt'])
        ]
        mock_getsize.side_effect = [100, 200] # file1.txt, file2.txt

        size = get_dir_size('/test_dir')
        self.assertEqual(size, 300)
        
        # Test empty directory
        mock_walk.return_value = [('/empty_dir', [], [])]
        size = get_dir_size('/empty_dir')
        self.assertEqual(size, 0)

        # Test non-existent directory
        mock_isdir.return_value = False
        size = get_dir_size('/non_existent_dir')
        self.assertEqual(size, 0)

    def test_format_bytes(self):
        self.assertEqual(format_bytes(0), "0 Bytes")
        self.assertEqual(format_bytes(500), "500.00 Bytes")
        self.assertEqual(format_bytes(1024), "1.00 KB")
        self.assertEqual(format_bytes(1024 * 1024), "1.00 MB")
        self.assertEqual(format_bytes(1024 * 1024 * 1024), "1.00 GB")
        self.assertEqual(format_bytes(1.5 * 1024 * 1024 * 1024), "1.50 GB")
        self.assertEqual(format_bytes(1024**5), "1024.00 TB") # Should cap at TB for this implementation

    @patch('purifier.get_cache_paths', return_value=['/mock/cache1', '/mock/cache2']) # Mock rationale: Control the list of cache paths.
    @patch('purifier.get_dir_size', side_effect=[1024, 2048]) # Mock rationale: Control the reported size of mock directories.
    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_dry_run_purifier(self, mock_print, mock_get_dir_size, mock_get_cache_paths):
        path_sizes, total_savings = dry_run_purifier()
        self.assertEqual(total_savings, 3072) # 1KB + 2KB
        self.assertDictEqual(path_sizes, {'/mock/cache1': 1024, '/mock/cache2': 2048})
        mock_print.assert_any_call("Total potential space to reclaim: 3.00 KB")
        mock_print.assert_any_call("Dry run complete. No files were deleted.")

    @patch('purifier.get_cache_paths', return_value=[]) # Mock rationale: Simulate no cache paths found.
    @patch('builtins.print') # Mock rationale: Capture print output.
    def test_dry_run_purifier_no_caches(self, mock_print, mock_get_cache_paths):
        path_sizes, total_savings = dry_run_purifier()
        self.assertEqual(total_savings, 0)
        self.assertDictEqual(path_sizes, {})
        mock_print.assert_any_call("No common cache directories found to analyze.")

    @patch('purifier.dry_run_purifier', return_value=({'/mock/cache1': 1024, '/mock/cache2': 2048}, 3072)) # Mock rationale: Control dry run output for clean_purifier.
    @patch('shutil.rmtree') # Mock rationale: Prevent actual file deletion.
    @patch('builtins.input', return_value='y') # Mock rationale: Simulate user confirming deletion.
    @patch('builtins.print') # Mock rationale: Capture print output.
    def test_clean_purifier_confirmed(self, mock_print, mock_input, mock_rmtree, mock_dry_run_purifier):
        reclaimed_space = clean_purifier()
        self.assertEqual(reclaimed_space, 3072)
        mock_rmtree.assert_has_calls([call('/mock/cache1'), call('/mock/cache2')], any_order=True)
        mock_print.assert_any_call("Nightly Cache Purifier complete! Reclaimed: 3.00 KB")

    @patch('purifier.dry_run_purifier', return_value=({'/mock/cache1': 1024}, 1024)) # Mock rationale: Control dry run output.
    @patch('shutil.rmtree', side_effect=OSError("Permission denied")) # Mock rationale: Simulate a deletion error.
    @patch('builtins.input', return_value='y') # Mock rationale: Simulate user confirming deletion.
    @patch('builtins.print') # Mock rationale: Capture print output.
    def test_clean_purifier_with_error(self, mock_print, mock_input, mock_rmtree, mock_dry_run_purifier):
        reclaimed_space = clean_purifier()
        self.assertEqual(reclaimed_space, 0) # No space reclaimed if rmtree fails
        mock_rmtree.assert_called_once_with('/mock/cache1')
        mock_print.assert_any_call("    Error deleting /mock/cache1: Permission denied")
        mock_print.assert_any_call("Nightly Cache Purifier complete! Reclaimed: 0.00 Bytes")


    @patch('purifier.dry_run_purifier', return_value=({'/mock/cache1': 1024, '/mock/cache2': 2048}, 3072)) # Mock rationale: Control dry run output.
    @patch('shutil.rmtree') # Mock rationale: Prevent actual file deletion.
    @patch('builtins.input', return_value='n') # Mock rationale: Simulate user declining deletion.
    @patch('builtins.print') # Mock rationale: Capture print output.
    def test_clean_purifier_declined(self, mock_print, mock_input, mock_rmtree, mock_dry_run_purifier):
        reclaimed_space = clean_purifier()
        self.assertEqual(reclaimed_space, 0)
        mock_rmtree.assert_not_called()
        mock_print.assert_any_call("Cleaning aborted by user.")

    @patch('purifier.dry_run_purifier', return_value=({}, 0)) # Mock rationale: Simulate no caches found.
    @patch('shutil.rmtree') # Mock rationale: Prevent actual file deletion.
    @patch('builtins.print') # Mock rationale: Capture print output.
    def test_clean_purifier_no_caches(self, mock_print, mock_rmtree, mock_dry_run_purifier):
        reclaimed_space = clean_purifier()
        self.assertEqual(reclaimed_space, 0)
        mock_rmtree.assert_not_called()
        mock_print.assert_any_call("No cache directories with content found to clean.")

    @patch('purifier.dry_run_purifier', return_value=({'/mock/cache1': 1024}, 1024)) # Mock rationale: Control dry run output.
    @patch('shutil.rmtree') # Mock rationale: Prevent actual file deletion.
    @patch('builtins.input', return_value='y') # Mock rationale: Simulate user confirming deletion.
    @patch('builtins.print') # Mock rationale: Capture print output.
    def test_clean_purifier_force(self, mock_print, mock_input, mock_rmtree, mock_dry_run_purifier):
        reclaimed_space = clean_purifier(force=True)
        self.assertEqual(reclaimed_space, 1024)
        mock_rmtree.assert_called_once_with('/mock/cache1')
        mock_input.assert_not_called() # Input should be skipped with force=True

    @patch('argparse.ArgumentParser.parse_args') # Mock rationale: Control command-line arguments.
    @patch('purifier.dry_run_purifier') # Mock rationale: Prevent actual dry run execution.
    @patch('purifier.clean_purifier') # Mock rationale: Prevent actual clean execution.
    def test_main_dry_run(self, mock_clean, mock_dry_run, mock_parse_args):
        mock_parse_args.return_value = MagicMock(dry_run=True, clean=False, force=False, verbose=False)
        main()
        mock_dry_run.assert_called_once_with(verbose=False)
        mock_clean.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args') # Mock rationale: Control command-line arguments.
    @patch('purifier.dry_run_purifier') # Mock rationale: Prevent actual dry run execution.
    @patch('purifier.clean_purifier') # Mock rationale: Prevent actual clean execution.
    def test_main_clean(self, mock_clean, mock_dry_run, mock_parse_args):
        mock_parse_args.return_value = MagicMock(dry_run=False, clean=True, force=False, verbose=True)
        main()
        mock_clean.assert_called_once_with(force=False, verbose=True)
        mock_dry_run.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args') # Mock rationale: Control command-line arguments.
    @patch('purifier.dry_run_purifier') # Mock rationale: Prevent actual dry run execution.
    @patch('purifier.clean_purifier') # Mock rationale: Prevent actual clean execution.
    def test_main_clean_force(self, mock_clean, mock_dry_run, mock_parse_args):
        mock_parse_args.return_value = MagicMock(dry_run=False, clean=True, force=True, verbose=False)
        main()
        mock_clean.assert_called_once_with(force=True, verbose=False)
        mock_dry_run.assert_not_called()

if __name__ == '__main__':
    unittest.main()
