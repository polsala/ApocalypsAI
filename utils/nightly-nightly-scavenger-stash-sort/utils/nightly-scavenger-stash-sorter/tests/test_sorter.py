import unittest
import os
import shutil
from unittest.mock import patch, MagicMock
import sys

# Import the sorter functions (assuming sorter.py is in src/)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from sorter import get_category, sort_stash, FILE_CATEGORIES
sys.path.pop(0)

class TestScavengerStashSorter(unittest.TestCase):

    def test_get_category(self):
        self.assertEqual(get_category("document.pdf"), "Documents")
        self.assertEqual(get_category("image.JPG"), "Images") # Test case-insensitivity
        self.assertEqual(get_category("song.mp3"), "Audio")
        self.assertEqual(get_category("movie.mkv"), "Video")
        self.assertEqual(get_category("archive.zip"), "Archives")
        self.assertEqual(get_category("program.exe"), "Executables")
        self.assertEqual(get_category("script.py"), "Code")
        self.assertEqual(get_category("unknown_file.xyz"), "Other")
        self.assertEqual(get_category("file_without_extension"), "Other")
        self.assertEqual(get_category(".bashrc"), "Other") # Dotfiles without common extensions

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists')
    @patch('builtins.print') # Mock rationale: Suppress print output during tests to keep test logs clean.
    def test_sort_stash_empty_source(self, mock_print, mock_exists, mock_move, mock_makedirs, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Simulate an empty source directory to ensure no operations are performed.
        mock_isdir.side_effect = lambda p: p == '/mock/source'
        mock_listdir.return_value = []
        mock_isfile.return_value = False
        mock_exists.return_value = False

        result = sort_stash('/mock/source', '/mock/destination')
        self.assertTrue(result)
        mock_makedirs.assert_called_with('/mock/destination', exist_ok=True)
        mock_move.assert_not_called()
        mock_print.assert_any_call("Sorting complete. 0 files processed.")

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists')
    @patch('builtins.print')
    def test_sort_stash_various_files(self, mock_print, mock_exists, mock_move, mock_makedirs, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Simulate a source directory with various file types and a subdirectory.
        mock_isdir.side_effect = lambda p: p == '/mock/source' or p == '/mock/destination'
        mock_listdir.return_value = [
            'report.pdf', 'image.jpg', 'song.mp3', 'archive.zip', 'script.py', 'unknown.xyz', 'subdir'
        ]
        mock_isfile.side_effect = lambda p: p in [
            '/mock/source/report.pdf',
            '/mock/source/image.jpg',
            '/mock/source/song.mp3',
            '/mock/source/archive.zip',
            '/mock/source/script.py',
            '/mock/source/unknown.xyz'
        ]
        mock_exists.return_value = False # Mock rationale: No duplicates initially in the destination.

        result = sort_stash('/mock/source', '/mock/destination')
        self.assertTrue(result)

        # Check if destination and category directories were created
        mock_makedirs.assert_any_call('/mock/destination', exist_ok=True)
        for category in FILE_CATEGORIES.keys():
            mock_makedirs.assert_any_call(os.path.join('/mock/destination', category), exist_ok=True)
        mock_makedirs.assert_any_call(os.path.join('/mock/destination', 'Other'), exist_ok=True)

        # Check if files were moved to correct categories
        mock_move.assert_any_call('/mock/source/report.pdf', '/mock/destination/Documents/report.pdf')
        mock_move.assert_any_call('/mock/source/image.jpg', '/mock/destination/Images/image.jpg')
        mock_move.assert_any_call('/mock/source/song.mp3', '/mock/destination/Audio/song.mp3')
        mock_move.assert_any_call('/mock/source/archive.zip', '/mock/destination/Archives/archive.zip')
        mock_move.assert_any_call('/mock/source/script.py', '/mock/destination/Code/script.py')
        mock_move.assert_any_call('/mock/source/unknown.xyz', '/mock/destination/Other/unknown.xyz')

        self.assertEqual(mock_move.call_count, 6)
        mock_print.assert_any_call("  Skipping directory 'subdir'")
        mock_print.assert_any_call("Sorting complete. 6 files processed.")

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists')
    @patch('builtins.print')
    def test_sort_stash_with_duplicates(self, mock_print, mock_exists, mock_move, mock_makedirs, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Simulate a source directory with files that would create duplicates in the destination,
        # testing the duplicate renaming logic.
        mock_isdir.side_effect = lambda p: p == '/mock/source' or p == '/mock/destination'
        mock_listdir.return_value = ['report.pdf', 'report.pdf'] # Two files with the same name
        mock_isfile.side_effect = lambda p: p in ['/mock/source/report.pdf', '/mock/source/report.pdf'] # Both are files

        # Mock rationale: Simulate the existence check for duplicate files.
        # 1. First 'report.pdf' is processed: '/mock/destination/Documents/report.pdf' does not exist (False).
        # 2. Second 'report.pdf' is processed: '/mock/destination/Documents/report.pdf' *does* exist (True).
        # 3. Then, '/mock/destination/Documents/report_1.pdf' does not exist (False), so it's used.
        mock_exists.side_effect = [
            False, 
            True,  
            False  
        ]

        result = sort_stash('/mock/source', '/mock/destination')
        self.assertTrue(result)

        mock_move.assert_any_call('/mock/source/report.pdf', '/mock/destination/Documents/report.pdf')
        mock_move.assert_any_call('/mock/source/report.pdf', '/mock/destination/Documents/report_1.pdf')
        self.assertEqual(mock_move.call_count, 2)
        mock_print.assert_any_call("Sorting complete. 2 files processed.")

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists')
    @patch('builtins.print')
    def test_sort_stash_invalid_source(self, mock_print, mock_exists, mock_move, mock_makedirs, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Test behavior when the source directory does not exist.
        mock_isdir.return_value = False # Source does not exist

        result = sort_stash('/mock/nonexistent_source', '/mock/destination')
        self.assertFalse(result)
        mock_print.assert_any_call("Error: Source directory '/mock/nonexistent_source' does not exist.", file=sys.stderr)
        mock_makedirs.assert_not_called()
        mock_move.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists')
    @patch('builtins.print')
    def test_sort_stash_move_error(self, mock_print, mock_exists, mock_move, mock_makedirs, mock_isfile, mock_listdir, mock_isdir):
        # Mock rationale: Simulate an error during file movement (e.g., permission denied).
        mock_isdir.side_effect = lambda p: p == '/mock/source' or p == '/mock/destination'
        mock_listdir.return_value = ['bad_file.txt']
        mock_isfile.return_value = True
        mock_exists.return_value = False
        mock_move.side_effect = Exception("Permission denied")

        result = sort_stash('/mock/source', '/mock/destination')
        self.assertTrue(result) # The function should still return True as it attempts to process files
        mock_move.assert_called_once_with('/mock/source/bad_file.txt', '/mock/destination/Documents/bad_file.txt')
        mock_print.assert_any_call("  Error moving 'bad_file.txt': Permission denied", file=sys.stderr)
        mock_print.assert_any_call("Sorting complete. 0 files processed.")

    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('os.path.join', side_effect=os.path.join)
    @patch('sorter.sort_stash')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_default_destination(self, mock_sys_exit, mock_parse_args, mock_sort_stash, mock_join, mock_abspath):
        # Mock rationale: Test the main function's argument parsing and default destination logic.
        mock_parse_args.return_value = MagicMock(source='/mock/source', destination=None)
        mock_sort_stash.return_value = True

        from sorter import main
        main()

        mock_sort_stash.assert_called_once_with('/mock/source', '/mock/source/sorted_stash')
        mock_sys_exit.assert_not_called()

    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('os.path.join', side_effect=os.path.join)
    @patch('sorter.sort_stash')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_custom_destination(self, mock_sys_exit, mock_parse_args, mock_sort_stash, mock_join, mock_abspath):
        # Mock rationale: Test the main function's argument parsing with a custom destination.
        mock_parse_args.return_value = MagicMock(source='/mock/source', destination='/mock/custom_dest')
        mock_sort_stash.return_value = True

        from sorter import main
        main()

        mock_sort_stash.assert_called_once_with('/mock/source', '/mock/custom_dest')
        mock_sys_exit.assert_not_called()

    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('os.path.join', side_effect=os.path.join)
    @patch('sorter.sort_stash')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_sort_failure(self, mock_sys_exit, mock_parse_args, mock_sort_stash, mock_join, mock_abspath):
        # Mock rationale: Test the main function's exit code (1) when sort_stash indicates a failure.
        mock_parse_args.return_value = MagicMock(source='/mock/source', destination='/mock/custom_dest')
        mock_sort_stash.return_value = False

        from sorter import main
        main()

        mock_sort_stash.assert_called_once_with('/mock/source', '/mock/custom_dest')
        mock_sys_exit.assert_called_once_with(1)
