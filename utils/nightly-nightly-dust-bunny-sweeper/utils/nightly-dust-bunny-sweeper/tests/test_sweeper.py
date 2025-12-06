import unittest
from unittest.mock import patch, call
import os
import sys

# Mock rationale: Import the function to test from the source module.
# This allows patching os functions directly within the test scope.
from src.sweeper import delete_empty_dirs

class TestDeleteEmptyDirs(unittest.TestCase):

    @patch('os.rmdir')
    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO) # Mock rationale: Capture stdout for assertions.
    @patch('sys.stderr', new_callable=unittest.mock.StringIO) # Mock rationale: Capture stderr for assertions.
    def test_deletes_empty_directories(self, mock_stderr, mock_stdout, mock_listdir, mock_isdir, mock_walk, mock_rmdir):
        # Mock rationale: Simulate a valid root directory.
        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory structure with empty and non-empty directories.
        # os.walk yields (dirpath, dirnames, filenames) for topdown=False (bottom-up).
        # We need to simulate the state of os.listdir at the point delete_empty_dirs calls it.
        # The order here is crucial for bottom-up processing.
        mock_walk.return_value = iter([
            ('/mock_root/dirA/dirB', [], []), # This will be empty and deleted
            ('/mock_root/dirA/dirC', [], ['file.txt']), # This has a file, not deleted
            ('/mock_root/dirA', ['dirB', 'dirC'], []), # After dirB is gone, dirC remains, so dirA is not empty
            ('/mock_root/dirD', [], []), # This will be empty and deleted
            ('/mock_root', ['dirA', 'dirD'], ['root_file.txt']) # Has a file, not deleted
        ])

        # Mock rationale: Control os.listdir behavior based on the directory being listed.
        # This simulates the state *after* os.walk has processed children.
        def mock_listdir_side_effect(path):
            if path == '/mock_root/dirA/dirB':
                return [] # Empty, should be deleted
            if path == '/mock_root/dirA/dirC':
                return ['file.txt'] # Not empty
            if path == '/mock_root/dirA':
                # After dirB is deleted, dirC still exists
                return ['dirC'] # Not empty
            if path == '/mock_root/dirD':
                return [] # Empty, should be deleted
            if path == '/mock_root':
                # After dirD is deleted, dirA and root_file.txt still exist
                return ['dirA', 'root_file.txt'] # Not empty
            return []

        mock_listdir.side_effect = mock_listdir_side_effect

        delete_empty_dirs('/mock_root')

        # Assert that os.rmdir was called for the correct empty directories
        mock_rmdir.assert_has_calls([
            call('/mock_root/dirA/dirB'),
            call('/mock_root/dirD')
        ], any_order=False)

        # Assert that os.rmdir was called exactly twice
        self.assertEqual(mock_rmdir.call_count, 2)

        # Assert stdout messages
        self.assertIn("Deleting empty directory: /mock_root/dirA/dirB", mock_stdout.getvalue())
        self.assertIn("Deleting empty directory: /mock_root/dirD", mock_stdout.getvalue())
        self.assertIn("Successfully deleted 2 empty directories under '/mock_root'.", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('os.rmdir')
    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_no_empty_directories(self, mock_stderr, mock_stdout, mock_listdir, mock_isdir, mock_walk, mock_rmdir):
        # Mock rationale: Simulate a valid root directory.
        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory structure with no empty directories.
        mock_walk.return_value = iter([
            ('/mock_root/dirA', [], ['file1.txt']),
            ('/mock_root/dirB', [], ['file2.txt']),
            ('/mock_root', ['dirA', 'dirB'], ['root_file.txt'])
        ])

        # Mock rationale: Ensure os.listdir always returns non-empty for these paths.
        mock_listdir.side_effect = lambda p: ['dummy_file.txt'] if 'file' not in p else ['file1.txt']

        delete_empty_dirs('/mock_root')

        # Assert that os.rmdir was never called
        mock_rmdir.assert_not_called()
        self.assertIn("No empty directories found under '/mock_root'.", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('os.rmdir')
    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_path_is_not_directory(self, mock_stderr, mock_stdout, mock_listdir, mock_isdir, mock_walk, mock_rmdir):
        # Mock rationale: Simulate an invalid path.
        mock_isdir.return_value = False

        delete_empty_dirs('/non_existent_path')

        # Assert that os.walk and os.rmdir were never called
        mock_walk.assert_not_called()
        mock_rmdir.assert_not_called()
        self.assertIn("Error: Path '/non_existent_path' is not a valid directory.", mock_stderr.getvalue())
        self.assertEqual(mock_stdout.getvalue(), "")

    @patch('os.rmdir')
    @patch('os.walk')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    def test_os_error_during_deletion(self, mock_stderr, mock_stdout, mock_listdir, mock_isdir, mock_walk, mock_rmdir):
        # Mock rationale: Simulate a valid root directory.
        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory structure where one directory is empty but deletion fails.
        mock_walk.return_value = iter([
            ('/mock_root/dirA', [], []),
            ('/mock_root', ['dirA'], ['file.txt'])
        ])

        # Mock rationale: Simulate dirA being empty.
        mock_listdir.side_effect = lambda p: [] if p == '/mock_root/dirA' else ['file.txt']

        # Mock rationale: Simulate an OSError when trying to delete dirA.
        mock_rmdir.side_effect = OSError("Permission denied")

        delete_empty_dirs('/mock_root')

        # Assert that os.rmdir was attempted for dirA
        mock_rmdir.assert_called_once_with('/mock_root/dirA')

        # Assert error message is printed to stderr
        self.assertIn("Warning: Could not delete directory /mock_root/dirA: Permission denied", mock_stderr.getvalue())
        # The count should be 0 because the deletion failed
        self.assertIn("Successfully deleted 0 empty directories under '/mock_root'.", mock_stdout.getvalue())
