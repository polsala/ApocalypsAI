import unittest
from unittest.mock import patch, call, MagicMock
import os
import sys
import datetime

# Add the src directory to the Python path to allow importing renamer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import renamer

class TestRenamer(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.path.getctime')
    @patch('os.rename')
    @patch('builtins.print')
    def test_basic_rename_modification_time(self, mock_print, mock_rename, mock_getctime, mock_getmtime, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Simulate directory existence, list files, file type, timestamps, and rename operations.
        # `mock_print` is used to capture output for verification.
        mock_isdir.return_value = True
        mock_listdir.return_value = ['file_a.txt', 'file_b.jpg']
        mock_isfile.side_effect = lambda x: x in ['/test_dir/file_a.txt', '/test_dir/file_b.jpg']

        # Mock modification times
        mock_getmtime.side_effect = lambda x: {
            '/test_dir/file_a.txt': datetime.datetime(2023, 1, 1, 10, 0, 0).timestamp(),
            '/test_dir/file_b.jpg': datetime.datetime(2023, 1, 1, 11, 30, 15).timestamp()
        }.get(x, 0)
        mock_getctime.return_value = 0 # Not used in this test

        renamer.rename_files_in_directory('/test_dir', use_creation_time=False, dry_run=False, keep_original_name=False)

        mock_rename.assert_has_calls([
            call('/test_dir/file_a.txt', '/test_dir/20230101_100000.txt'),
            call('/test_dir/file_b.jpg', '/test_dir/20230101_113015.jpg')
        ], any_order=True)
        self.assertEqual(mock_rename.call_count, 2)
        mock_print.assert_any_call("  Renamed 'file_a.txt' -> '20230101_100000.txt'")
        mock_print.assert_any_call("  Renamed 'file_b.jpg' -> '20230101_113015.jpg'")

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.path.getctime')
    @patch('os.rename')
    @patch('builtins.print')
    def test_basic_rename_creation_time(self, mock_print, mock_rename, mock_getctime, mock_getmtime, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Simulate directory existence, list files, file type, timestamps, and rename operations.
        mock_isdir.return_value = True
        mock_listdir.return_value = ['doc1.pdf', 'report.docx']
        mock_isfile.side_effect = lambda x: x in ['/test_dir/doc1.pdf', '/test_dir/report.docx']

        # Mock creation times
        mock_getctime.side_effect = lambda x: {
            '/test_dir/doc1.pdf': datetime.datetime(2022, 5, 10, 9, 0, 0).timestamp(),
            '/test_dir/report.docx': datetime.datetime(2022, 5, 10, 14, 45, 30).timestamp()
        }.get(x, 0)
        mock_getmtime.return_value = 0 # Not used in this test

        renamer.rename_files_in_directory('/test_dir', use_creation_time=True, dry_run=False, keep_original_name=False)

        mock_rename.assert_has_calls([
            call('/test_dir/doc1.pdf', '/test_dir/20220510_090000.pdf'),
            call('/test_dir/report.docx', '/test_dir/20220510_144530.docx')
        ], any_order=True)
        self.assertEqual(mock_rename.call_count, 2)
        mock_print.assert_any_call("  Renamed 'doc1.pdf' -> '20220510_090000.pdf'")
        mock_print.assert_any_call("  Renamed 'report.docx' -> '20220510_144530.docx'")

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.path.getctime')
    @patch('os.rename')
    @patch('builtins.print')
    def test_dry_run_mode(self, mock_print, mock_rename, mock_getctime, mock_getmtime, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Simulate directory existence, list files, file type, timestamps. `os.rename` should not be called.
        mock_isdir.return_value = True
        mock_listdir.return_value = ['image.png']
        mock_isfile.side_effect = lambda x: x == '/test_dir/image.png'
        mock_getmtime.return_value = datetime.datetime(2024, 2, 15, 8, 0, 0).timestamp()
        mock_getctime.return_value = 0

        renamer.rename_files_in_directory('/test_dir', dry_run=True, keep_original_name=False)

        mock_rename.assert_not_called()
        mock_print.assert_any_call("DRY RUN: No files will be actually renamed.")
        mock_print.assert_any_call("  Would rename 'image.png' -> '20240215_080000.png'")

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.path.getctime')
    @patch('os.rename')
    @patch('builtins.print')
    def test_conflict_resolution(self, mock_print, mock_rename, mock_getctime, mock_getmtime, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Simulate multiple files having the same timestamp to test conflict resolution.
        mock_isdir.return_value = True
        mock_listdir.return_value = ['pic1.jpeg', 'pic2.jpeg', 'pic3.jpeg']
        mock_isfile.side_effect = lambda x: x in ['/test_dir/pic1.jpeg', '/test_dir/pic2.jpeg', '/test_dir/pic3.jpeg']

        # All files have the same modification time
        common_timestamp = datetime.datetime(2023, 7, 4, 12, 0, 0).timestamp()
        mock_getmtime.return_value = common_timestamp
        mock_getctime.return_value = 0

        renamer.rename_files_in_directory('/test_dir', dry_run=False, keep_original_name=False)

        mock_rename.assert_has_calls([
            call('/test_dir/pic1.jpeg', '/test_dir/20230704_120000.jpeg'),
            call('/test_dir/pic2.jpeg', '/test_dir/20230704_120000_02.jpeg'),
            call('/test_dir/pic3.jpeg', '/test_dir/20230704_120000_03.jpeg')
        ], any_order=True)
        self.assertEqual(mock_rename.call_count, 3)
        mock_print.assert_any_call("  Renamed 'pic1.jpeg' -> '20230704_120000.jpeg'")
        mock_print.assert_any_call("  Renamed 'pic2.jpeg' -> '20230704_120000_02.jpeg'")
        mock_print.assert_any_call("  Renamed 'pic3.jpeg' -> '20230704_120000_03.jpeg'")

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.path.getctime')
    @patch('os.rename')
    @patch('builtins.print')
    def test_keep_original_name(self, mock_print, mock_rename, mock_getctime, mock_getmtime, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Test the option to include a sanitized version of the original filename in the new name.
        mock_isdir.return_value = True
        mock_listdir.return_value = ['my old photo.gif']
        mock_isfile.side_effect = lambda x: x == '/test_dir/my old photo.gif'
        mock_getmtime.return_value = datetime.datetime(2021, 11, 20, 1, 2, 3).timestamp()
        mock_getctime.return_value = 0

        renamer.rename_files_in_directory('/test_dir', dry_run=False, keep_original_name=True)

        mock_rename.assert_called_once_with('/test_dir/my old photo.gif', '/test_dir/20211120_010203_my_old_photo.gif')
        mock_print.assert_any_call("  Renamed 'my old photo.gif' -> '20211120_010203_my_old_photo.gif'")

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.path.getctime')
    @patch('os.rename')
    @patch('builtins.print')
    def test_empty_directory(self, mock_print, mock_rename, mock_getctime, mock_getmtime, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Ensure no errors and correct output for an empty directory.
        mock_isdir.return_value = True
        mock_listdir.return_value = []
        mock_isfile.return_value = False
        mock_getmtime.return_value = 0
        mock_getctime.return_value = 0

        renamer.rename_files_in_directory('/empty_dir')

        mock_rename.assert_not_called()
        mock_print.assert_any_call("Scanning directory: /empty_dir")
        mock_print.assert_any_call("\nFinished. Renamed 0 files.")

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.path.getctime')
    @patch('os.rename')
    @patch('builtins.print')
    def test_directory_not_found(self, mock_print, mock_rename, mock_getctime, mock_getmtime, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Test error handling when the specified directory does not exist.
        mock_isdir.return_value = False

        with self.assertRaises(SystemExit) as cm:
            renamer.rename_files_in_directory('/non_existent_dir')
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_any_call("Error: Directory '/non_existent_dir' not found.")
        mock_rename.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.path.getctime')
    @patch('os.rename')
    @patch('builtins.print')
    def test_skip_non_files(self, mock_print, mock_rename, mock_getctime, mock_getmtime, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Ensure that subdirectories or other non-file entries are correctly skipped.
        mock_isdir.return_value = True
        mock_listdir.return_value = ['file.txt', 'subdir', 'another_file.log']
        mock_isfile.side_effect = lambda x: x in ['/test_dir/file.txt', '/test_dir/another_file.log']

        mock_getmtime.side_effect = lambda x: {
            '/test_dir/file.txt': datetime.datetime(2020, 1, 1, 1, 1, 1).timestamp(),
            '/test_dir/another_file.log': datetime.datetime(2020, 1, 1, 2, 2, 2).timestamp()
        }.get(x, 0)
        mock_getctime.return_value = 0

        renamer.rename_files_in_directory('/test_dir')

        mock_rename.assert_has_calls([
            call('/test_dir/file.txt', '/test_dir/20200101_010101.txt'),
            call('/test_dir/another_file.log', '/test_dir/20200101_020202.log')
        ], any_order=True)
        self.assertEqual(mock_rename.call_count, 2)
        mock_print.assert_any_call("  Renamed 'file.txt' -> '20200101_010101.txt'")
        mock_print.assert_any_call("  Renamed 'another_file.log' -> '20200101_020202.log'")

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.path.getctime')
    @patch('os.rename')
    @patch('builtins.print')
    def test_file_already_correctly_named(self, mock_print, mock_rename, mock_getctime, mock_getmtime, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Test that files already matching the target naming convention are skipped.
        mock_isdir.return_value = True
        mock_listdir.return_value = ['20230101_100000.txt']
        mock_isfile.side_effect = lambda x: x == '/test_dir/20230101_100000.txt'
        mock_getmtime.return_value = datetime.datetime(2023, 1, 1, 10, 0, 0).timestamp()
        mock_getctime.return_value = 0

        renamer.rename_files_in_directory('/test_dir')

        mock_rename.assert_not_called()
        mock_print.assert_any_call("  Skipping '20230101_100000.txt': Already correctly named or no change needed.")

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.path.getctime')
    @patch('os.rename')
    @patch('builtins.print')
    @patch('os.path.exists')
    def test_target_filename_exists(self, mock_exists, mock_print, mock_rename, mock_getctime, mock_getmtime, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Test handling of a scenario where the *target* filename already exists on the filesystem.
        mock_isdir.return_value = True
        mock_listdir.return_value = ['original.txt']
        mock_isfile.side_effect = lambda x: x == '/test_dir/original.txt'
        mock_getmtime.return_value = datetime.datetime(2023, 1, 1, 10, 0, 0).timestamp()
        mock_getctime.return_value = 0

        # Mock that the target filename already exists
        mock_exists.side_effect = lambda x: x == '/test_dir/20230101_100000.txt'

        renamer.rename_files_in_directory('/test_dir')

        mock_rename.assert_not_called()
        mock_print.assert_any_call("  Warning: Target '20230101_100000.txt' already exists. Skipping 'original.txt'.")

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.path.getmtime')
    @patch('os.path.getctime')
    @patch('os.rename')
    @patch('builtins.print')
    def test_sanitize_filename(self, mock_print, mock_rename, mock_getctime, mock_getmtime, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Test that filenames with special characters are sanitized when keep_original_name is True.
        mock_isdir.return_value = True
        mock_listdir.return_value = ['file/with:bad?chars.txt']
        mock_isfile.side_effect = lambda x: x == '/test_dir/file/with:bad?chars.txt'
        mock_getmtime.return_value = datetime.datetime(2023, 1, 1, 10, 0, 0).timestamp()
        mock_getctime.return_value = 0

        renamer.rename_files_in_directory('/test_dir', dry_run=False, keep_original_name=True)

        mock_rename.assert_called_once_with('/test_dir/file/with:bad?chars.txt', '/test_dir/20230101_100000_file_withbadchars.txt')
        mock_print.assert_any_call("  Renamed 'file/with:bad?chars.txt' -> '20230101_100000_file_withbadchars.txt'")

if __name__ == '__main__':
    unittest.main()
