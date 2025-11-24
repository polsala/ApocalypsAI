import unittest
from unittest.mock import patch, mock_open, call
import os
import sys
from io import StringIO

# Add the src directory to the path to allow importing sweeper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from sweeper import DigitalDustBunnySweeper, main

class TestDigitalDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        self.mock_root = '/mock/project'
        self.default_patterns = ['*.log', '*.tmp', '__pycache__', '.DS_Store', 'Thumbs.db']
        self.mock_stdout = StringIO()
        self.mock_stderr = StringIO()
        sys.stdout = self.mock_stdout
        sys.stderr = self.mock_stderr

    def tearDown(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    @patch('os.path.isdir')
    def test_init_invalid_path(self, mock_isdir):
        # Mock rationale: os.path.isdir is a file system operation that needs to be controlled
        mock_isdir.return_value = False
        with self.assertRaisesRegex(ValueError, "Error: Root path '.*' is not a valid directory."):
            DigitalDustBunnySweeper('/nonexistent', [], False, [], True)

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.abspath', side_effect=lambda x: x) # Mock rationale: abspath changes based on current working directory, needs to be deterministic
    @patch('os.walk')
    @patch('os.listdir', return_value=[]) # Mock rationale: os.listdir is a file system operation, used to check if a directory is empty
    def test_find_dust_bunnies_dry_run_no_matches(self, mock_listdir, mock_walk, mock_abspath, mock_isdir):
        # Mock rationale: os.walk is the core file system traversal, needs to be fully controlled for deterministic tests.
        # It returns (dirpath, dirnames, filenames).
        mock_walk.return_value = [
            (self.mock_root, ['src', 'data'], ['README.md']),
            (os.path.join(self.mock_root, 'src'), [], ['app.py']),
            (os.path.join(self.mock_root, 'data'), [], ['config.json']),
        ]
        sweeper = DigitalDustBunnySweeper(self.mock_root, [], False, [], True)
        sweeper.sweep()

        self.assertIn("No digital dust bunnies found!", self.mock_stdout.getvalue())
        self.assertEqual(len(sweeper.found_items), 0)
        mock_walk.assert_called_once_with(self.mock_root, topdown=False)

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('os.walk')
    @patch('os.listdir', side_effect=lambda x: [] if x == os.path.join(self.mock_root, 'empty_dir') else ['file.txt']) # Mock rationale: os.listdir is a file system operation, used to check if a directory is empty
    def test_find_dust_bunnies_with_files_and_empty_dirs_dry_run(self, mock_listdir, mock_walk, mock_abspath, mock_isdir):
        mock_walk.return_value = [
            (self.mock_root, ['src', 'logs', 'empty_dir'], ['README.md', 'temp.tmp']),
            (os.path.join(self.mock_root, 'src'), [], ['app.py', '__pycache__']),
            (os.path.join(self.mock_root, 'logs'), [], ['app.log', 'old.log.bak']),
            (os.path.join(self.mock_root, 'empty_dir'), [], []), # This directory is empty
        ]
        patterns = ['*.tmp', '*.log', '__pycache__']
        sweeper = DigitalDustBunnySweeper(self.mock_root, patterns, True, [], True)
        sweeper.sweep()

        output = self.mock_stdout.getvalue()
        self.assertIn("--- Digital Dust Bunny Report (DRY RUN) ---", output)
        self.assertIn(f"  [FILE] Would delete: {os.path.join(self.mock_root, 'temp.tmp')}", output)
        self.assertIn(f"  [FILE] Would delete: {os.path.join(self.mock_root, 'src', '__pycache__')}", output)
        self.assertIn(f"  [FILE] Would delete: {os.path.join(self.mock_root, 'logs', 'app.log')}", output)
        self.assertIn(f"  [DIR] Would delete: {os.path.join(self.mock_root, 'empty_dir')}", output)
        self.assertIn("Total items identified: 4", output)
        self.assertEqual(len(sweeper.found_items), 4)

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('os.walk')
    @patch('os.listdir', side_effect=lambda x: [] if x == os.path.join(self.mock_root, 'empty_dir') else ['file.txt']) # Mock rationale: os.listdir is a file system operation, used to check if a directory is empty
    @patch('os.remove') # Mock rationale: os.remove is a file system modification, needs to be mocked for clean tests.
    @patch('os.rmdir') # Mock rationale: os.rmdir is a file system modification, needs to be mocked for clean tests.
    def test_clean_mode_execution(self, mock_rmdir, mock_remove, mock_listdir, mock_walk, mock_abspath, mock_isdir):
        mock_walk.return_value = [
            (self.mock_root, ['empty_dir'], ['temp.tmp']),
            (os.path.join(self.mock_root, 'empty_dir'), [], []),
        ]
        patterns = ['*.tmp']
        sweeper = DigitalDustBunnySweeper(self.mock_root, patterns, True, [], False) # dry_run=False
        sweeper.sweep()

        output = self.mock_stdout.getvalue()
        self.assertIn("--- Digital Dust Bunny Report (CLEANUP) ---", output)
        self.assertIn(f"  [FILE] Deleting: {os.path.join(self.mock_root, 'temp.tmp')}", output)
        self.assertIn(f"  [DIR] Deleting: {os.path.join(self.mock_root, 'empty_dir')}", output)
        self.assertIn("Total items identified: 2", output)
        self.assertIn("Cleanup complete. May your repository remain pristine!", output)

        mock_remove.assert_called_once_with(os.path.join(self.mock_root, 'temp.tmp'))
        mock_rmdir.assert_called_once_with(os.path.join(self.mock_root, 'empty_dir'))

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('os.walk')
    @patch('os.listdir', return_value=['file.txt']) # Mock rationale: os.listdir is a file system operation, used to check if a directory is empty
    def test_exclude_paths(self, mock_listdir, mock_walk, mock_abspath, mock_isdir):
        excluded_dir = os.path.join(self.mock_root, 'excluded_data')
        excluded_file = os.path.join(self.mock_root, 'src', 'secret.log')
        mock_walk.return_value = [
            (self.mock_root, ['src', 'excluded_data'], ['project.log']),
            (os.path.join(self.mock_root, 'src'), [], ['app.py', 'secret.log']),
            (excluded_dir, [], ['important.data']), # Should be skipped due to dir exclusion
        ]
        patterns = ['*.log']
        exclude_paths = [excluded_dir, excluded_file]
        sweeper = DigitalDustBunnySweeper(self.mock_root, patterns, False, exclude_paths, True)
        sweeper.sweep()

        output = self.mock_stdout.getvalue()
        self.assertIn(f"  [FILE] Would delete: {os.path.join(self.mock_root, 'project.log')}", output)
        self.assertNotIn(f"  [FILE] Would delete: {excluded_file}", output)
        self.assertNotIn(f"  [FILE] Would delete: {os.path.join(excluded_dir, 'important.data')}", output)
        self.assertEqual(len(sweeper.found_items), 1)

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.abspath', side_effect=lambda x: x)
    @patch('os.walk')
    @patch('os.listdir', return_value=[]) # Mock rationale: os.listdir is a file system operation, used to check if a directory is empty
    @patch('os.remove', side_effect=OSError("Permission denied")) # Mock rationale: os.remove is a file system modification, needs to be mocked for clean tests.
    @patch('os.rmdir', side_effect=OSError("Directory not empty")) # Mock rationale: os.rmdir is a file system modification, needs to be mocked for clean tests.
    def test_cleanup_errors(self, mock_rmdir, mock_remove, mock_listdir, mock_walk, mock_abspath, mock_isdir):
        mock_walk.return_value = [
            (self.mock_root, ['empty_dir'], ['error.tmp']),
            (os.path.join(self.mock_root, 'empty_dir'), [], []),
        ]
        patterns = ['*.tmp']
        sweeper = DigitalDustBunnySweeper(self.mock_root, patterns, True, [], False)
        sweeper.sweep()

        output = self.mock_stdout.getvalue()
        self.assertIn(f"  ❌ Failed to delete file '{os.path.join(self.mock_root, 'error.tmp')}': Permission denied", output)
        self.assertIn(f"  ❌ Failed to delete dir '{os.path.join(self.mock_root, 'empty_dir')}': Directory not empty", output)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    @patch('sweeper.DigitalDustBunnySweeper')
    def test_main_success(self, MockSweeper, mock_exit, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args needs to return controlled arguments.
        # sys.exit needs to be mocked to prevent actual program exit during tests.
        # DigitalDustBunnySweeper needs to be mocked to control its behavior and verify calls.
        mock_parse_args.return_value = argparse.Namespace(
            path=self.mock_root,
            patterns=['*.log'],
            empty_dirs=False,
            exclude=[],
            clean=False,
            dry_run=True
        )
        mock_sweeper_instance = MockSweeper.return_value
        mock_sweeper_instance.sweep.return_value = None

        main()

        MockSweeper.assert_called_once_with(
            root_path=self.mock_root,
            patterns=['*.log'],
            empty_dirs=False,
            exclude=[],
            dry_run=True
        )
        mock_sweeper_instance.sweep.assert_called_once()
        mock_exit.assert_called_once_with(0)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    @patch('sweeper.DigitalDustBunnySweeper')
    def test_main_value_error(self, MockSweeper, mock_exit, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            path='/invalid/path',
            patterns=[],
            empty_dirs=False,
            exclude=[],
            clean=False,
            dry_run=True
        )
        MockSweeper.side_effect = ValueError("Test error: Invalid path")

        main()

        self.assertIn("Test error: Invalid path", self.mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    @patch('sweeper.DigitalDustBunnySweeper')
    def test_main_clean_overrides_dry_run(self, MockSweeper, mock_exit, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            path=self.mock_root,
            patterns=['*.log'],
            empty_dirs=False,
            exclude=[],
            clean=True, # Clean is True
            dry_run=True # Dry run is also True, but should be overridden
        )
        mock_sweeper_instance = MockSweeper.return_value
        mock_sweeper_instance.sweep.return_value = None

        main()

        MockSweeper.assert_called_once_with(
            root_path=self.mock_root,
            patterns=['*.log'],
            empty_dirs=False,
            exclude=[],
            dry_run=False # Verify dry_run is False due to --clean
        )
        mock_exit.assert_called_once_with(0)

if __name__ == '__main__':
    unittest.main()
