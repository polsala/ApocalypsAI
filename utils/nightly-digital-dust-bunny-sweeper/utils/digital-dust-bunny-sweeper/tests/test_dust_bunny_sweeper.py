import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the src directory to the path to import the utility
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from dust_bunny_sweeper import find_dust_bunnies, main

class TestDustBunnySweeper(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_dust_bunnies_empty_dir(self, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory containing only an empty subdirectory.
        # os.path.isdir is mocked to confirm the root_dir exists.
        # os.walk is mocked to return a specific directory structure.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_root', ['empty_folder'], []), # Root dir, one empty subfolder
            ('/test_root/empty_folder', [], [])   # Empty subfolder
        ]

        empty_dirs, junk_files, junk_dirs = find_dust_bunnies('/test_root')

        self.assertEqual(len(empty_dirs), 1)
        self.assertIn('/test_root/empty_folder', empty_dirs)
        self.assertEqual(len(junk_files), 0)
        self.assertEqual(len(junk_dirs), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_dust_bunnies_junk_files_and_dirs(self, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with various junk files and junk directories.
        # os.path.isdir is mocked to confirm the root_dir exists.
        # os.walk is mocked to return a specific directory structure with files and directories.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_root', ['sub_dir', '__pycache__', '.pytest_cache'], ['app.log', 'main.py', '.DS_Store']),
            ('/test_root/sub_dir', [], ['temp.tmp', 'data.json', 'module.pyc']),
            ('/test_root/__pycache__', [], ['module.cpython-39.pyc']),
            ('/test_root/.pytest_cache', [], ['v/cache/lastfailed'])
        ]

        empty_dirs, junk_files, junk_dirs = find_dust_bunnies('/test_root')

        self.assertEqual(len(empty_dirs), 0)
        self.assertEqual(len(junk_files), 4) # app.log, .DS_Store, temp.tmp, module.pyc
        self.assertIn('/test_root/app.log', junk_files)
        self.assertIn('/test_root/.DS_Store', junk_files)
        self.assertIn('/test_root/sub_dir/temp.tmp', junk_files)
        self.assertIn('/test_root/sub_dir/module.pyc', junk_files)

        self.assertEqual(len(junk_dirs), 2) # __pycache__, .pytest_cache
        self.assertIn('/test_root/__pycache__', junk_dirs)
        self.assertIn('/test_root/.pytest_cache', junk_dirs)


    @patch('os.path.isdir')
    @patch('os.walk')
    def test_find_dust_bunnies_mixed(self, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with empty subdirectories, junk files, and junk directories.
        # os.path.isdir is mocked to confirm the root_dir exists.
        # os.walk is mocked to return a specific directory structure.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_root', ['empty_dir', 'data_dir', '__pycache__'], ['config.bak', 'script.py']),
            ('/test_root/empty_dir', [], []),
            ('/test_root/data_dir', [], ['temp.tmp', 'report.csv']),
            ('/test_root/__pycache__', [], ['module.cpython-39.pyc'])
        ]

        empty_dirs, junk_files, junk_dirs = find_dust_bunnies('/test_root')

        self.assertEqual(len(empty_dirs), 1)
        self.assertIn('/test_root/empty_dir', empty_dirs)

        self.assertEqual(len(junk_files), 2)
        self.assertIn('/test_root/config.bak', junk_files)
        self.assertIn('/test_root/data_dir/temp.tmp', junk_files)

        self.assertEqual(len(junk_dirs), 1)
        self.assertIn('/test_root/__pycache__', junk_dirs)

    @patch('os.path.isdir')
    @patch('sys.stderr', new_callable=MagicMock)
    def test_find_dust_bunnies_non_existent_dir(self, mock_stderr, mock_isdir):
        # Mock rationale: Simulate calling the utility with a non-existent directory.
        # os.path.isdir is mocked to return False for the target directory.
        mock_isdir.return_value = False

        empty_dirs, junk_files, junk_dirs = find_dust_bunnies('/non_existent')

        self.assertEqual(len(empty_dirs), 0)
        self.assertEqual(len(junk_files), 0)
        self.assertEqual(len(junk_dirs), 0)
        mock_stderr.write.assert_called_with("Error: Directory '/non_existent' not found.\n")

    @patch('sys.argv', ['dust_bunny_sweeper.py', '/test_root'])
    @patch('builtins.print')
    @patch('dust_bunny_sweeper.find_dust_bunnies')
    def test_main_found_bunnies(self, mock_find_bunnies, mock_print):
        # Mock rationale: Simulate the main function execution when dust bunnies are found.
        # sys.argv is mocked to provide command-line arguments.
        # builtins.print is mocked to capture output.
        # find_dust_bunnies is mocked to return predefined lists of bunnies.
        mock_find_bunnies.return_value = (['/test_root/empty_dir'], ['/test_root/junk.log'], ['/test_root/__pycache__'])

        main()

        mock_print.assert_any_call("Scanning directory: /test_root\n")
        mock_print.assert_any_call("Found 3 Digital Dust Bunnies:\n")
        mock_print.assert_any_call("Empty Directories:")
        mock_print.assert_any_call("  - /test_root/empty_dir")
        mock_print.assert_any_call("Junk Files:")
        mock_print.assert_any_call("  - /test_root/junk.log")
        mock_print.assert_any_call("Junk Directories:")
        mock_print.assert_any_call("  - /test_root/__pycache__")
        mock_print.assert_any_call("Sweep complete! Review the list above for potential cleanup.")

    @patch('sys.argv', ['dust_bunny_sweeper.py', '/test_root'])
    @patch('builtins.print')
    @patch('dust_bunny_sweeper.find_dust_bunnies')
    def test_main_no_bunnies(self, mock_find_bunnies, mock_print):
        # Mock rationale: Simulate the main function execution when no dust bunnies are found.
        # sys.argv is mocked to provide command-line arguments.
        # builtins.print is mocked to capture output.
        # find_dust_bunnies is mocked to return empty lists.
        mock_find_bunnies.return_value = ([], [], [])

        main()

        mock_print.assert_any_call("Scanning directory: /test_root\n")
        mock_print.assert_any_call("No Digital Dust Bunnies found. Your repository is sparkling clean! ✨")

    @patch('sys.argv', ['dust_bunny_sweeper.py'])
    @patch('sys.exit')
    @patch('sys.stderr', new_callable=MagicMock)
    def test_main_no_args(self, mock_stderr, mock_exit):
        # Mock rationale: Simulate calling the main function without required arguments.
        # sys.argv is mocked to simulate missing arguments.
        # sys.exit is mocked to prevent actual exit during test.
        # sys.stderr is mocked to capture error output.
        main()

        mock_stderr.write.assert_called_with("Usage: python dust_bunny_sweeper.py <directory_to_scan>\n")
        mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
