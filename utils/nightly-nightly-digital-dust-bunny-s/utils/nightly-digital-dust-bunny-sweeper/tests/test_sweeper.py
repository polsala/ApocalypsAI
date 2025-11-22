import unittest
from unittest.mock import patch, call
import sys
from io import StringIO
import os

# Add the src directory to the Python path to allow importing sweeper.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from sweeper import clean_empty_dirs, main
sys.path.pop(0)

class TestSweeper(unittest.TestCase):

    def setUp(self):
        # Capture stdout and stderr for testing print statements
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()
        self.held_stderr = sys.stderr
        sys.stderr = self.mock_stderr = StringIO()

    def tearDown(self):
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_deletes_single_empty_dir(self, mock_walk, mock_is_dir, mock_listdir, mock_rmdir):
        # Mock rationale: Simulate a directory structure with one empty directory.
        # os.walk will traverse it, os.listdir will confirm it's empty,
        # os.path.isdir will confirm the root is valid, and os.rmdir will be called.
        root = '/mock_root'
        empty_dir = os.path.join(root, 'empty_dir')

        mock_is_dir.return_value = True
        mock_walk.return_value = [
            (root, ['empty_dir'], []),
            (empty_dir, [], []), # This is the empty directory
        ]
        # os.listdir needs to return [] for empty_dir when it's checked
        mock_listdir.side_effect = lambda p: [] if p == empty_dir else ['empty_dir'] if p == root else []

        deleted_count = clean_empty_dirs(root)

        self.assertEqual(deleted_count, 1)
        mock_rmdir.assert_called_once_with(empty_dir)
        self.assertIn(f"Deleting empty directory: {empty_dir}", self.mock_stdout.getvalue())

    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_deletes_nested_empty_dirs(self, mock_walk, mock_is_dir, mock_listdir, mock_rmdir):
        # Mock rationale: Simulate a nested empty directory structure.
        # os.walk (bottom-up) should delete inner empty dirs first, then outer.
        root = '/mock_root'
        empty_dir1 = os.path.join(root, 'empty_dir1')
        empty_dir2 = os.path.join(empty_dir1, 'empty_dir2')

        mock_is_dir.return_value = True
        mock_walk.return_value = [
            (root, ['empty_dir1'], []),
            (empty_dir1, ['empty_dir2'], []),
            (empty_dir2, [], []), # Innermost empty dir
        ]
        # os.listdir needs to reflect the state *after* subdirs are processed by os.walk.
        # For bottom-up walk, when processing empty_dir2, it's empty.
        # When processing empty_dir1, empty_dir2 has been 'removed' from its contents, so it becomes empty.
        mock_listdir.side_effect = lambda p: [] if p in [empty_dir2, empty_dir1] else ['empty_dir1'] if p == root else []

        deleted_count = clean_empty_dirs(root)

        self.assertEqual(deleted_count, 2)
        # Assert calls in the correct bottom-up order
        mock_rmdir.assert_has_calls([call(empty_dir2), call(empty_dir1)], any_order=False)
        self.assertIn(f"Deleting empty directory: {empty_dir2}", self.mock_stdout.getvalue())
        self.assertIn(f"Deleting empty directory: {empty_dir1}", self.mock_stdout.getvalue())

    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_does_not_delete_dir_with_files(self, mock_walk, mock_is_dir, mock_listdir, mock_rmdir):
        # Mock rationale: Simulate a directory containing a file.
        # os.listdir should indicate it's not empty, so os.rmdir should not be called.
        root = '/mock_root'
        full_dir = os.path.join(root, 'full_dir')

        mock_is_dir.return_value = True
        mock_walk.return_value = [
            (root, ['full_dir'], []),
            (full_dir, [], ['important.txt']), # Contains a file
        ]
        mock_listdir.side_effect = lambda p: ['important.txt'] if p == full_dir else ['full_dir'] if p == root else []

        deleted_count = clean_empty_dirs(root)

        self.assertEqual(deleted_count, 0)
        mock_rmdir.assert_not_called()
        self.assertNotIn(f"Deleting empty directory: {full_dir}", self.mock_stdout.getvalue())

    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_does_not_delete_dir_with_subdirs_containing_files(self, mock_walk, mock_is_dir, mock_listdir, mock_rmdir):
        # Mock rationale: Simulate a directory structure where a parent directory
        # has a subdirectory that contains files, making the parent non-empty.
        root = '/mock_root'
        parent_dir = os.path.join(root, 'parent')
        child_dir = os.path.join(parent_dir, 'child')

        mock_is_dir.return_value = True
        mock_walk.return_value = [
            (root, ['parent'], []),
            (parent_dir, ['child'], []),
            (child_dir, [], ['data.log']), # Child dir has a file
        ]
        # os.listdir needs to reflect that child_dir is not empty, and thus parent_dir is not empty.
        mock_listdir.side_effect = lambda p: ['data.log'] if p == child_dir else ['child'] if p == parent_dir else ['parent'] if p == root else []

        deleted_count = clean_empty_dirs(root)

        self.assertEqual(deleted_count, 0)
        mock_rmdir.assert_not_called()
        self.assertNotIn(f"Deleting empty directory: {parent_dir}", self.mock_stdout.getvalue())
        self.assertNotIn(f"Deleting empty directory: {child_dir}", self.mock_stdout.getvalue())

    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_dry_run_mode(self, mock_walk, mock_is_dir, mock_listdir, mock_rmdir):
        # Mock rationale: Test that in dry-run mode, os.rmdir is never called,
        # but the correct messages are printed indicating what *would* be done.
        root = '/mock_root'
        empty_dir = os.path.join(root, 'empty_dir')

        mock_is_dir.return_value = True
        mock_walk.return_value = [
            (root, ['empty_dir'], []),
            (empty_dir, [], []),
        ]
        mock_listdir.side_effect = lambda p: [] if p == empty_dir else ['empty_dir'] if p == root else []

        deleted_count = clean_empty_dirs(root, dry_run=True)

        self.assertEqual(deleted_count, 1) # Still counts what *would* be deleted
        mock_rmdir.assert_not_called()
        self.assertIn(f"Would delete empty directory: {empty_dir}", self.mock_stdout.getvalue())

    @patch('os.rmdir')
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_invalid_path_handling(self, mock_walk, mock_is_dir, mock_listdir, mock_rmdir):
        # Mock rationale: Test that if the initial path is not a directory,
        # an error is printed to stderr and no operations are attempted.
        invalid_path = '/non_existent_path'
        mock_is_dir.return_value = False # Simulate invalid path

        deleted_count = clean_empty_dirs(invalid_path)

        self.assertEqual(deleted_count, 0)
        mock_is_dir.assert_called_once_with(invalid_path)
        mock_walk.assert_not_called()
        mock_rmdir.assert_not_called()
        self.assertIn(f"Error: '{invalid_path}' is not a valid directory.", self.mock_stderr.getvalue())

    @patch('os.rmdir', side_effect=OSError("Permission denied"))
    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.walk')
    def test_os_error_during_deletion(self, mock_walk, mock_is_dir, mock_listdir, mock_rmdir):
        # Mock rationale: Simulate an OSError during os.rmdir, e.g., permission denied.
        # The utility should catch the error and print it to stderr, but continue processing.
        root = '/mock_root'
        empty_dir = os.path.join(root, 'empty_dir')

        mock_is_dir.return_value = True
        mock_walk.return_value = [
            (root, ['empty_dir'], []),
            (empty_dir, [], []),
        ]
        mock_listdir.side_effect = lambda p: [] if p == empty_dir else ['empty_dir'] if p == root else []

        deleted_count = clean_empty_dirs(root)

        self.assertEqual(deleted_count, 0) # Deletion failed, so count is 0
        mock_rmdir.assert_called_once_with(empty_dir)
        self.assertIn(f"Error deleting '{empty_dir}': Permission denied", self.mock_stderr.getvalue())
        self.assertIn(f"Deleting empty directory: {empty_dir}", self.mock_stdout.getvalue())

    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(path='/mock_root', dry_run=False))
    @patch('sweeper.clean_empty_dirs', return_value=1)
    def test_main_function_success(self, mock_clean_empty_dirs, mock_parse_args):
        # Mock rationale: Test the main function's flow when clean_empty_dirs succeeds.
        # We mock argparse to control inputs and clean_empty_dirs to control its output.
        main()
        self.assertIn("Starting the Nightly Digital Dust Bunny Sweeper in '/mock_root'...", self.mock_stdout.getvalue())
        self.assertIn("Sweeper finished. Deleted 1 empty directories.", self.mock_stdout.getvalue())
        mock_clean_empty_dirs.assert_called_once_with('/mock_root', False)

    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(path='/mock_root', dry_run=True))
    @patch('sweeper.clean_empty_dirs', return_value=0)
    def test_main_function_no_op(self, mock_clean_empty_dirs, mock_parse_args):
        # Mock rationale: Test the main function's flow when no directories are found to clean.
        main()
        self.assertIn("Running in DRY-RUN mode. No files will be deleted.", self.mock_stdout.getvalue())
        self.assertIn("Sweeper finished. No empty directories found to clean.", self.mock_stdout.getvalue())
        mock_clean_empty_dirs.assert_called_once_with('/mock_root', True)

    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(path='/invalid_path', dry_run=False))
    @patch('sweeper.clean_empty_dirs', return_value=0)
    def test_main_function_invalid_path(self, mock_clean_empty_dirs, mock_parse_args):
        # Mock rationale: Test the main function's flow when an invalid path is provided.
        # clean_empty_dirs will handle the error message.
        main()
        self.assertIn("Starting the Nightly Digital Dust Bunny Sweeper in '/invalid_path'...", self.mock_stdout.getvalue())
        # The error message itself is printed by clean_empty_dirs to stderr, not stdout.
        # The final message on stdout should still indicate completion.
        self.assertIn("Sweeper finished. No empty directories found to clean.", self.mock_stdout.getvalue())
        mock_clean_empty_dirs.assert_called_once_with('/invalid_path', False)
