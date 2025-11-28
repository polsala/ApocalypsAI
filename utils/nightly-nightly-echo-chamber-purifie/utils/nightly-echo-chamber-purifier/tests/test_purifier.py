import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
import hashlib

# Add the src directory to the path to allow importing purifier
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from purifier import calculate_file_hash, find_duplicates

class TestPurifier(unittest.TestCase):

    def setUp(self):
        # Mock rationale: Suppress print statements during tests for cleaner output.
        self.mock_stdout = patch('sys.stdout', new_callable=MagicMock)
        self.mock_stderr = patch('sys.stderr', new_callable=MagicMock)
        self.mock_stdout.start()
        self.mock_stderr.start()

    def tearDown(self):
        self.mock_stdout.stop()
        self.mock_stderr.stop()

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_success(self, mock_file_open, mock_isfile):
        # Mock rationale: Simulate a file existing and having specific content
        # without actual disk I/O, ensuring deterministic hash calculation.
        mock_isfile.return_value = True
        mock_file_open.return_value.read.side_effect = [b'content', b' of the file', b'']
        
        expected_hash = hashlib.sha256(b'content of the file').hexdigest()
        self.assertEqual(calculate_file_hash('/fake/path/file.txt'), expected_hash)
        mock_file_open.assert_called_with('/fake/path/file.txt', 'rb')

    @patch('os.path.isfile')
    def test_calculate_file_hash_non_existent_file(self, mock_isfile):
        # Mock rationale: Simulate a non-existent file to test error handling
        # without needing to create or check for actual files.
        mock_isfile.return_value = False
        self.assertIsNone(calculate_file_hash('/fake/path/non_existent.txt'))

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_io_error(self, mock_file_open, mock_isfile):
        # Mock rationale: Simulate an IOError during file reading to test robust error handling.
        mock_isfile.return_value = True
        mock_file_open.side_effect = IOError("Permission denied")
        self.assertIsNone(calculate_file_hash('/fake/path/unreadable.txt'))
        self.mock_stderr.new_callable().write.assert_called_with("Error reading file /fake/path/unreadable.txt: Permission denied\n")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.remove')
    def test_find_duplicates_no_duplicates(self, mock_remove, mock_file_open, mock_isfile, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with unique files.
        # os.path.isdir: Ensure the target directory is considered valid.
        # os.walk: Provide a predefined directory and file structure.
        # os.path.isfile: Mark specific paths as files.
        # builtins.open: Provide unique content for each file.
        # os.remove: Verify that no files are attempted to be removed.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/dir1', [], ['fileA.txt', 'fileB.txt'])
        ]
        mock_isfile.side_effect = lambda x: x in ['/dir1/fileA.txt', '/dir1/fileB.txt']
        
        # Mock file content for unique hashes
        def mock_open_side_effect(filepath, mode):
            if filepath == '/dir1/fileA.txt':
                return mock_open(read_data=b'content A').return_value
            elif filepath == '/dir1/fileB.txt':
                return mock_open(read_data=b'content B').return_value
            return mock_open().return_value

        mock_file_open.side_effect = mock_open_side_effect

        duplicates = find_duplicates(['/dir1'])
        self.assertEqual(len(duplicates), 0)
        mock_remove.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.remove')
    def test_find_duplicates_with_duplicates_report_only(self, mock_remove, mock_file_open, mock_isfile, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with duplicate files.
        # os.path.isdir, os.walk, os.path.isfile: As above, define file system.
        # builtins.open: Provide identical content for duplicate files.
        # os.remove: Verify no deletion occurs in report-only mode.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/dir1', [], ['file1.txt', 'copy_file1.txt']),
            ('/dir2', [], ['another_file1.txt'])
        ]
        mock_isfile.side_effect = lambda x: x in [
            '/dir1/file1.txt', '/dir1/copy_file1.txt', '/dir2/another_file1.txt'
        ]

        # Mock file content: file1.txt and copy_file1.txt have same content
        def mock_open_side_effect(filepath, mode):
            if filepath in ['/dir1/file1.txt', '/dir1/copy_file1.txt']:
                return mock_open(read_data=b'duplicate content').return_value
            elif filepath == '/dir2/another_file1.txt':
                return mock_open(read_data=b'unique content').return_value
            return mock_open().return_value

        mock_file_open.side_effect = mock_open_side_effect

        duplicates = find_duplicates(['/dir1', '/dir2'], delete_duplicates=False)
        self.assertEqual(len(duplicates), 1)
        
        expected_hash = hashlib.sha256(b'duplicate content').hexdigest()
        self.assertIn(expected_hash, duplicates)
        self.assertCountEqual(duplicates[expected_hash], ['/dir1/file1.txt', '/dir1/copy_file1.txt'])
        mock_remove.assert_not_called()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.remove')
    def test_find_duplicates_with_duplicates_and_delete(self, mock_remove, mock_file_open, mock_isfile, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure with duplicate files and test deletion.
        # os.path.isdir, os.walk, os.path.isfile: Define file system.
        # builtins.open: Provide identical content for duplicate files.
        # os.remove: Verify that the correct duplicate files are attempted to be removed.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/dir1', [], ['file1.txt', 'copy_file1.txt', 'another_copy.txt'])
        ]
        mock_isfile.side_effect = lambda x: x in [
            '/dir1/file1.txt', '/dir1/copy_file1.txt', '/dir1/another_copy.txt'
        ]

        # Mock file content: all three files have the same content
        mock_file_open.side_effect = [
            mock_open(read_data=b'duplicate content').return_value, 
            mock_open(read_data=b'duplicate content').return_value, 
            mock_open(read_data=b'duplicate content').return_value  
        ]

        duplicates = find_duplicates(['/dir1'], delete_duplicates=True)
        self.assertEqual(len(duplicates), 1)
        
        expected_hash = hashlib.sha256(b'duplicate content').hexdigest()
        self.assertIn(expected_hash, duplicates)
        self.assertCountEqual(duplicates[expected_hash], ['/dir1/file1.txt', '/dir1/copy_file1.txt', '/dir1/another_copy.txt'])
        
        # Expect two files to be removed (all but the first one in the list)
        # The order of files in the list from os.walk is not guaranteed, 
        # but we can check if the *correct number* of removals happened 
        # and if the *correct files* (the duplicates) were targeted.
        self.assertEqual(mock_remove.call_count, 2)
        # Check if the calls were made for the expected files (excluding the first one found)
        # Since the order of paths in the list `paths` is determined by `os.walk` and `setdefault`, 
        # we can't guarantee which one is 'first'. However, we can assert that the *set* of files 
        # removed is the set of duplicates minus one.
        removed_files = {call.args[0] for call in mock_remove.call_args_list}
        original_files = set(['/dir1/file1.txt', '/dir1/copy_file1.txt', '/dir1/another_copy.txt'])
        self.assertEqual(len(original_files - removed_files), 1) # One file should remain
        self.assertTrue(all(f in original_files for f in removed_files))

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.remove')
    def test_find_duplicates_non_existent_directory(self, mock_remove, mock_file_open, mock_isfile, mock_walk, mock_isdir):
        # Mock rationale: Simulate a non-existent directory to test error handling.
        # os.path.isdir: Return False for the target directory.
        mock_isdir.return_value = False
        duplicates = find_duplicates(['/non_existent_dir'])
        self.assertEqual(len(duplicates), 0)
        mock_walk.assert_not_called() # os.walk should not be called if dir doesn't exist
        self.mock_stderr.new_callable().write.assert_called_with("Warning: Directory not found or not accessible: /non_existent_dir\n")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.remove', side_effect=OSError("Permission denied"))
    def test_find_duplicates_delete_error(self, mock_remove, mock_file_open, mock_isfile, mock_walk, mock_isdir):
        # Mock rationale: Simulate an OSError during file deletion to test error handling.
        # os.remove: Raise an OSError when called.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/dir1', [], ['file1.txt', 'copy_file1.txt'])
        ]
        mock_isfile.side_effect = lambda x: x in ['/dir1/file1.txt', '/dir1/copy_file1.txt']
        # Mock file content for two files
        mock_file_open.side_effect = [
            mock_open(read_data=b'duplicate content').return_value, 
            mock_open(read_data=b'duplicate content').return_value
        ]

        duplicates = find_duplicates(['/dir1'], delete_duplicates=True)
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(mock_remove.call_count, 1)
        # The exact file deleted depends on the order from os.walk, but it will be one of the duplicates.
        # We assert that an error message for deletion was printed.
        self.mock_stderr.new_callable().write.assert_called_with(unittest.mock.ANY) # Check if any error was printed
        # More specific check for the error message content
        error_message_found = False
        for call_args in self.mock_stderr.new_callable().write.call_args_list:
            if "Error deleting" in call_args.args[0] and "Permission denied" in call_args.args[0]:
                error_message_found = True
                break
        self.assertTrue(error_message_found, "Expected deletion error message not found in stderr.")

if __name__ == '__main__':
    unittest.main()
