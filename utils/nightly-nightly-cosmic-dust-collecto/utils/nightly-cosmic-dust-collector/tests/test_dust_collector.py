import unittest
import os
import shutil
import time
from unittest.mock import patch, MagicMock

# Import the functions to be tested
from src.dust_collector import is_file_dust, scan_directory_for_dust, quarantine_file, main

class TestDustCollector(unittest.TestCase):

    @patch('os.stat')
    def test_is_file_dust_empty(self, mock_stat):
        # Mock rationale: os.stat is called to get file size and modification time.
        # We need to control these values for deterministic testing of 'is_file_dust'.
        mock_stat.return_value = MagicMock(st_size=0, st_mtime=time.time() - 1000) # 0 bytes, recent mod time
        self.assertTrue(is_file_dust('/path/to/empty.txt', None, None, True))
        self.assertFalse(is_file_dust('/path/to/empty.txt', 1, 1, False))

    @patch('os.stat')
    def test_is_file_dust_small(self, mock_stat):
        # Mock rationale: Same as above, controlling file size.
        mock_stat.return_value = MagicMock(st_size=500, st_mtime=time.time() - 1000) # 500 bytes, recent mod time
        self.assertTrue(is_file_dust('/path/to/small.txt', None, 1, False)) # max_size_kb=1 (1024 bytes)
        self.assertFalse(is_file_dust('/path/to/small.txt', None, 0.1, False)) # max_size_kb=0.1 (102 bytes)

    @patch('os.stat')
    def test_is_file_dust_old(self, mock_stat):
        # Mock rationale: Same as above, controlling modification time.
        # Simulate a file modified 60 days ago
        mock_stat.return_value = MagicMock(st_size=100, st_mtime=time.time() - (60 * 24 * 60 * 60))
        self.assertTrue(is_file_dust('/path/to/old.txt', 30, None, False)) # min_age_days=30
        self.assertFalse(is_file_dust('/path/to/old.txt', 90, None, False)) # min_age_days=90

    @patch('os.stat')
    def test_is_file_dust_combined_criteria(self, mock_stat):
        # Mock rationale: Testing combined criteria for 'is_file_dust'.
        # File is 0 bytes, 50 days old, and small (500 bytes, but 0 takes precedence if check_empty is true)
        mock_stat.return_value = MagicMock(st_size=0, st_mtime=time.time() - (50 * 24 * 60 * 60))
        self.assertTrue(is_file_dust('/path/to/dusty.txt', 30, 1, True)) # All criteria met

        mock_stat.return_value = MagicMock(st_size=2000, st_mtime=time.time() - (10 * 24 * 60 * 60))
        self.assertFalse(is_file_dust('/path/to/not_dusty.txt', 30, 1, True)) # None met

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile', return_value=True)
    @patch('os.walk')
    @patch('src.dust_collector.is_file_dust', return_value=True)
    def test_scan_directory_finds_dust(self, mock_is_file_dust, mock_walk, mock_isfile, mock_isdir):
        # Mock rationale: os.walk simulates the directory structure traversal.
        # os.path.isfile and os.path.isdir control what os.walk returns.
        # is_file_dust is mocked to always return True, simplifying the test to focus on traversal.
        mock_walk.return_value = [
            ('/root', ['subdir'], ['file1.txt', 'file2.log']),
            ('/root/subdir', [], ['subfile.txt'])
        ]
        dust_files = list(scan_directory_for_dust('/root', 1, 1, True, []))
        self.assertEqual(len(dust_files), 3)
        self.assertIn('/root/file1.txt', dust_files)
        self.assertIn('/root/file2.log', dust_files)
        self.assertIn('/root/subdir/subfile.txt', dust_files)

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile', return_value=True)
    @patch('os.walk')
    @patch('src.dust_collector.is_file_dust', return_value=False)
    def test_scan_directory_no_dust(self, mock_is_file_dust, mock_walk, mock_isfile, mock_isdir):
        # Mock rationale: is_file_dust is mocked to always return False, ensuring no dust is found.
        mock_walk.return_value = [
            ('/root', [], ['file1.txt'])
        ]
        dust_files = list(scan_directory_for_dust('/root', 1, 1, True, []))
        self.assertEqual(len(dust_files), 0)

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.isfile', return_value=True)
    @patch('os.walk')
    @patch('src.dust_collector.is_file_dust', return_value=True)
    def test_scan_directory_with_ignore_patterns(self, mock_is_file_dust, mock_walk, mock_isfile, mock_isdir):
        # Mock rationale: Testing the ignore_patterns functionality.
        # os.walk is mocked to simulate files and directories, and we check if ignored paths are skipped.
        mock_walk.return_value = [
            ('/root', ['ignored_dir', 'subdir'], ['file1.txt', 'ignored.log']),
            ('/root/ignored_dir', [], ['file_in_ignored_dir.txt']),
            ('/root/subdir', [], ['subfile.txt'])
        ]
        ignore_patterns = ['/root/ignored_dir/*', '*.log']
        dust_files = list(scan_directory_for_dust('/root', 1, 1, True, ignore_patterns))
        self.assertEqual(len(dust_files), 2) # file1.txt and subfile.txt should be found
        self.assertIn('/root/file1.txt', dust_files)
        self.assertIn('/root/subdir/subfile.txt', dust_files)
        self.assertNotIn('/root/ignored.log', dust_files) # Ignored by pattern
        self.assertNotIn('/root/ignored_dir/file_in_ignored_dir.txt', dust_files) # Ignored by directory pruning

    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists', return_value=False)
    def test_quarantine_file_success(self, mock_exists, mock_move, mock_makedirs):
        # Mock rationale: os.makedirs and shutil.move simulate file system operations.
        # os.path.exists is mocked to control collision scenarios.
        self.assertTrue(quarantine_file('/src/file.txt', '/quarantine'))
        mock_makedirs.assert_called_once_with('/quarantine', exist_ok=True)
        mock_move.assert_called_once_with('/src/file.txt', '/quarantine/file.txt')

    @patch('os.makedirs')
    @patch('shutil.move', side_effect=Exception("Permission denied"))
    @patch('os.path.exists', return_value=False)
    def test_quarantine_file_failure(self, mock_exists, mock_move, mock_makedirs):
        # Mock rationale: shutil.move is mocked to raise an exception, simulating a failure.
        self_output = MagicMock()
        with patch('builtins.print', self_output):
            self.assertFalse(quarantine_file('/src/file.txt', '/quarantine'))
            self.assertIn('Error quarantining', self_output.call_args[0][0])

    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists', side_effect=[True, False]) # First call True (collision), second False (new name)
    @patch('time.time', return_value=1234567890.0) # Deterministic timestamp for collision handling
    def test_quarantine_file_collision(self, mock_time, mock_exists, mock_move, mock_makedirs):
        # Mock rationale: os.path.exists is mocked to simulate a file collision.
        # time.time is mocked to ensure a deterministic timestamp for the new file name.
        self.assertTrue(quarantine_file('/src/file.txt', '/quarantine'))
        mock_move.assert_called_once_with('/src/file.txt', '/quarantine/file_1234567890.txt')

    @patch('src.dust_collector.scan_directory_for_dust')
    @patch('src.dust_collector.quarantine_file')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_list_dust(self, mock_parse_args, mock_print, mock_quarantine_file, mock_scan_directory_for_dust):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to control CLI arguments.
        # scan_directory_for_dust is mocked to provide a controlled list of 'dust' files.
        # quarantine_file is mocked to ensure it's not called when --quarantine is absent.
        # builtins.print is mocked to capture output for verification.
        mock_parse_args.return_value = MagicMock(
            dirs=['/test_dir'], min_age=1, max_size=None, empty=True, quarantine=None, ignore=[]
        )
        mock_scan_directory_for_dust.return_value = ['/test_dir/dusty.txt', '/test_dir/another_dust.log']

        main()

        mock_scan_directory_for_dust.assert_called_once_with('/test_dir', 1, None, True, [])
        mock_quarantine_file.assert_not_called()
        mock_print.assert_any_call("Found dust: /test_dir/dusty.txt")
        mock_print.assert_any_call("Found dust: /test_dir/another_dust.log")
        mock_print.assert_any_call('\nOperation complete. 2 cosmic dust files identified.')

    @patch('src.dust_collector.scan_directory_for_dust')
    @patch('src.dust_collector.quarantine_file')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_quarantine_dust(self, mock_parse_args, mock_print, mock_quarantine_file, mock_scan_directory_for_dust):
        # Mock rationale: Similar to test_main_list_dust, but testing the quarantine path.
        mock_parse_args.return_value = MagicMock(
            dirs=['/test_dir'], min_age=1, max_size=None, empty=True, quarantine='/q_zone', ignore=[]
        )
        mock_scan_directory_for_dust.return_value = ['/test_dir/dusty.txt']

        main()

        mock_scan_directory_for_dust.assert_called_once_with('/test_dir', 1, None, True, [])
        mock_quarantine_file.assert_called_once_with('/test_dir/dusty.txt', '/q_zone')
        mock_print.assert_any_call('\nOperation complete. 1 cosmic dust files quarantined.')

    @patch('src.dust_collector.scan_directory_for_dust', return_value=[])
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_dust_found(self, mock_parse_args, mock_print, mock_scan_directory_for_dust):
        # Mock rationale: scan_directory_for_dust is mocked to return an empty list, simulating no dust.
        mock_parse_args.return_value = MagicMock(
            dirs=['/test_dir'], min_age=1, max_size=None, empty=True, quarantine=None, ignore=[]
        )

        main()

        mock_print.assert_any_call("No cosmic dust found. Your digital space is pristine!")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('argparse.ArgumentParser.error')
    def test_main_no_criteria_error(self, mock_error, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.error is mocked to catch the expected error call.
        mock_parse_args.return_value = MagicMock(
            dirs=['/test_dir'], min_age=None, max_size=None, empty=False, quarantine=None, ignore=[]
        )

        main()

        mock_error.assert_called_once_with("At least one of --min-age, --max-size, or --empty must be specified.")
