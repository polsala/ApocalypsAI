import unittest
from unittest.mock import patch, MagicMock
import os
from datetime import datetime, timedelta

# Mock rationale: We need to prevent actual file system operations during tests
# and control the state of the file system (directories, files, symlinks, modification times)
# to ensure deterministic and isolated testing of the utility's logic.

class TestDigitalDustBunnyDestroyer(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.rmdir')
    @patch('builtins.print')
    def test_clean_empty_directories(self, mock_print, mock_rmdir, mock_walk, mock_isdir):
        from src.destroyer import clean_empty_directories

        mock_isdir.return_value = True # Mock the root_dir as a valid directory

        # Mock rationale: Simulate a directory structure with empty directories.
        # os.walk yields (dirpath, dirnames, filenames).
        # topdown=False means it walks bottom-up.
        mock_walk.return_value = [
            ('/test_root/dir1/subdir1', [], []), # Empty subdir
            ('/test_root/dir1', ['subdir1'], ['file1.txt']), # dir1 contains subdir1 and file1.txt
            ('/test_root/dir2', [], []), # Empty dir2
            ('/test_root', ['dir1', 'dir2'], ['root_file.txt']) # Root dir
        ]

        # Mock rationale: Simulate os.scandir for _is_empty_dir helper.
        # For '/test_root/dir1/subdir1' and '/test_root/dir2', scandir should return empty.
        # For others, it should return something.
        with patch('os.scandir') as mock_scandir:
            mock_scandir.side_effect = lambda path: [] if path in ['/test_root/dir1/subdir1', '/test_root/dir2'] else [MagicMock()]

            removed_count = clean_empty_directories('/test_root')

            self.assertEqual(removed_count, 2)
            mock_rmdir.assert_any_call('/test_root/dir1/subdir1')
            mock_rmdir.assert_any_call('/test_root/dir2')
            self.assertEqual(mock_rmdir.call_count, 2)
            mock_print.assert_any_call("Removed empty directory: /test_root/dir1/subdir1")
            mock_print.assert_any_call("Removed empty directory: /test_root/dir2")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    @patch('src.destroyer.datetime') # Mock datetime to control 'now'
    def test_clean_old_temp_files(self, mock_datetime, mock_print, mock_remove, mock_getmtime, mock_isfile, mock_walk, mock_isdir):
        from src.destroyer import clean_old_temp_files

        mock_isdir.return_value = True
        mock_isfile.return_value = True # All paths encountered are files

        # Mock rationale: Control the current time for age comparison.
        # Set 'now' to a specific point in time.
        mock_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp # Allow actual conversion

        # Mock rationale: Simulate files with different modification times and names.
        # File 'old_temp.tmp' is older than 7 days.
        # File 'recent.log' is recent.
        # File 'another.bak' is old.
        # File 'not_temp.txt' is not a temp file.
        mock_walk.return_value = [
            ('/test_root', [], ['old_temp.tmp', 'recent.log', 'another.bak', 'not_temp.txt'])
        ]

        # Mock rationale: Provide specific modification times for each file.
        # Old files: 10 days ago (older than 7)
        # Recent files: 1 day ago (not older than 7)
        def getmtime_side_effect(path):
            if 'old_temp.tmp' in path:
                return (mock_now - timedelta(days=10)).timestamp()
            elif 'another.bak' in path:
                return (mock_now - timedelta(days=8)).timestamp()
            elif 'recent.log' in path:
                return (mock_now - timedelta(days=1)).timestamp()
            elif 'not_temp.txt' in path:
                return (mock_now - timedelta(days=10)).timestamp() # Old, but not temp pattern
            return mock_now.timestamp()

        mock_getmtime.side_effect = getmtime_side_effect

        removed_count = clean_old_temp_files('/test_root', age_days=7)

        self.assertEqual(removed_count, 2)
        mock_remove.assert_any_call('/test_root/old_temp.tmp')
        mock_remove.assert_any_call('/test_root/another.bak')
        self.assertEqual(mock_remove.call_count, 2)
        mock_print.assert_any_call(unittest.mock.ANY) # Check for general print calls
        mock_print.assert_any_call("Removed old temp file: /test_root/old_temp.tmp (last modified: 2023-10-16)")
        mock_print.assert_any_call("Removed old temp file: /test_root/another.bak (last modified: 2023-10-18)")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.islink')
    @patch('os.path.exists')
    @patch('os.remove')
    @patch('builtins.print')
    def test_clean_broken_symlinks(self, mock_print, mock_remove, mock_exists, mock_islink, mock_walk, mock_isdir):
        from src.destroyer import clean_broken_symlinks

        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory with a broken symlink and a valid one.
        mock_walk.return_value = [
            ('/test_root', [], ['broken_link', 'valid_link', 'regular_file.txt'])
        ]

        # Mock rationale: Define which paths are symlinks and which exist.
        def islink_side_effect(path):
            return path in ['/test_root/broken_link', '/test_root/valid_link']

        def exists_side_effect(path):
            return path == '/test_root/valid_link' or path == '/test_root/regular_file.txt'

        mock_islink.side_effect = islink_side_effect
        mock_exists.side_effect = exists_side_effect

        removed_count = clean_broken_symlinks('/test_root')

        self.assertEqual(removed_count, 1)
        mock_remove.assert_called_once_with('/test_root/broken_link')
        mock_print.assert_any_call("Removed broken symlink: /test_root/broken_link")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.rmdir')
    @patch('builtins.print')
    def test_clean_empty_directories_dry_run(self, mock_print, mock_rmdir, mock_walk, mock_isdir):
        from src.destroyer import clean_empty_directories

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_root/empty_dir', [], []),
        ]
        with patch('os.scandir') as mock_scandir:
            mock_scandir.return_value = []

            removed_count = clean_empty_directories('/test_root', dry_run=True)

            self.assertEqual(removed_count, 0) # No actual removals in dry run
            mock_rmdir.assert_not_called()
            mock_print.assert_any_call("[DRY RUN] Would remove empty directory: /test_root/empty_dir")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.remove')
    @patch('builtins.print')
    @patch('src.destroyer.datetime')
    def test_clean_old_temp_files_dry_run(self, mock_datetime, mock_print, mock_remove, mock_getmtime, mock_isfile, mock_walk, mock_isdir):
        from src.destroyer import clean_old_temp_files

        mock_isdir.return_value = True
        mock_isfile.return_value = True

        mock_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp

        mock_walk.return_value = [
            ('/test_root', [], ['old_temp.tmp'])
        ]
        mock_getmtime.return_value = (mock_now - timedelta(days=10)).timestamp()

        removed_count = clean_old_temp_files('/test_root', age_days=7, dry_run=True)

        self.assertEqual(removed_count, 0)
        mock_remove.assert_not_called()
        mock_print.assert_any_call("[DRY RUN] Would remove old temp file: /test_root/old_temp.tmp (last modified: 2023-10-16)")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.islink')
    @patch('os.path.exists')
    @patch('os.remove')
    @patch('builtins.print')
    def test_clean_broken_symlinks_dry_run(self, mock_print, mock_remove, mock_exists, mock_islink, mock_walk, mock_isdir):
        from src.destroyer import clean_broken_symlinks

        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_root', [], ['broken_link'])
        ]
        mock_islink.return_value = True
        mock_exists.return_value = False

        removed_count = clean_broken_symlinks('/test_root', dry_run=True)

        self.assertEqual(removed_count, 0)
        mock_remove.assert_not_called()
        mock_print.assert_any_call("[DRY RUN] Would remove broken symlink: /test_root/broken_link")

    @patch('argparse.ArgumentParser')
    @patch('src.destroyer.clean_empty_directories')
    @patch('src.destroyer.clean_old_temp_files')
    @patch('src.destroyer.clean_broken_symlinks')
    @patch('builtins.print')
    def test_main_function(self, mock_print, mock_clean_broken, mock_clean_old_temp, mock_clean_empty, mock_argparse):
        from src.destroyer import main

        # Mock rationale: Simulate command-line arguments parsing.
        mock_args = MagicMock()
        mock_args.path = '/mock/path'
        mock_args.age = 10
        mock_args.dry_run = False

        mock_parser = MagicMock()
        mock_parser.parse_args.return_value = mock_args
        mock_argparse.return_value = mock_parser

        main()

        mock_clean_empty.assert_called_once_with('/mock/path', False)
        mock_clean_old_temp.assert_called_once_with('/mock/path', 10, dry_run=False)
        mock_clean_broken.assert_called_once_with('/mock/path', False)
        mock_print.assert_any_call("\n--- Starting Digital Dust Bunny Destroyer for '/mock/path' (Dry Run: False) ---")
        mock_print.assert_any_call("\n--- Digital Dust Bunny Destroyer finished. ---")

    @patch('argparse.ArgumentParser')
    @patch('src.destroyer.clean_empty_directories')
    @patch('src.destroyer.clean_old_temp_files')
    @patch('src.destroyer.clean_broken_symlinks')
    @patch('builtins.print')
    def test_main_function_dry_run(self, mock_print, mock_clean_broken, mock_clean_old_temp, mock_clean_empty, mock_argparse):
        from src.destroyer import main

        mock_args = MagicMock()
        mock_args.path = '/mock/path'
        mock_args.age = 10
        mock_args.dry_run = True

        mock_parser = MagicMock()
        mock_parser.parse_args.return_value = mock_args
        mock_argparse.return_value = mock_parser

        main()

        mock_clean_empty.assert_called_once_with('/mock/path', True)
        mock_clean_old_temp.assert_called_once_with('/mock/path', 10, dry_run=True)
        mock_clean_broken.assert_called_once_with('/mock/path', True)
        mock_print.assert_any_call("\n--- Starting Digital Dust Bunny Destroyer for '/mock/path' (Dry Run: True) ---")
        mock_print.assert_any_call("\n--- Digital Dust Bunny Destroyer finished. ---")
