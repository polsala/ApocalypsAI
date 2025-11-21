import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
from io import StringIO

# Mock rationale: We need to simulate file system operations (listing directories, reading files)
# without actually touching the disk to ensure deterministic and fast tests.
# os.walk, os.path.isfile, os.path.isdir, open, and os.remove are all mocked.

# A simple mock for os.walk that returns a predefined directory structure
# Format: (root, dirs, files)
# Mock rationale: Avoid actual file system traversal for deterministic tests.
_mock_walk_data = [
    ('/mock/dir1', ['subdirA', 'subdirB'], ['file1.txt', 'file2.txt']),
    ('/mock/dir1/subdirA', [], ['duplicate.txt', 'uniqueA.log']),
    ('/mock/dir1/subdirB', [], ['file3.txt']),
    ('/mock/dir2', ['subdirC'], ['file4.txt', 'duplicate.txt']),
    ('/mock/dir2/subdirC', [], ['uniqueC.json']),
    ('/mock/empty_dir', [], []),
]

# Mock rationale: Simulate file existence without actual disk access.
_mock_is_file_data = {
    '/mock/dir1/file1.txt': True,
    '/mock/dir1/file2.txt': True,
    '/mock/dir1/subdirA/duplicate.txt': True,
    '/mock/dir1/subdirA/uniqueA.log': True,
    '/mock/dir1/subdirB/file3.txt': True,
    '/mock/dir2/file4.txt': True,
    '/mock/dir2/duplicate.txt': True,
    '/mock/dir2/subdirC/uniqueC.json': True,
}

# Mock rationale: Simulate directory existence without actual disk access.
_mock_is_dir_data = {
    '/mock/dir1': True,
    '/mock/dir1/subdirA': True,
    '/mock/dir1/subdirB': True,
    '/mock/dir2': True,
    '/mock/dir2/subdirC': True,
    '/mock/empty_dir': True,
    '/mock/non_existent': False,
}

# Mock rationale: Simulate file content for hash calculation without actual disk reads.
_mock_file_contents = {
    '/mock/dir1/file1.txt': b'content of file1',
    '/mock/dir1/file2.txt': b'content of file2',
    '/mock/dir1/subdirA/duplicate.txt': b'duplicate content',
    '/mock/dir1/subdirA/uniqueA.log': b'unique content A',
    '/mock/dir1/subdirB/file3.txt': b'content of file3',
    '/mock/dir2/file4.txt': b'content of file4',
    '/mock/dir2/duplicate.txt': b'duplicate content',
    '/mock/dir2/subdirC/uniqueC.json': b'unique content C',
}

# Pre-calculate hashes for verification
_expected_hashes = {
    'content of file1': '206e232616222b40348259695427181f',
    'content of file2': '92398579085a3852033c46729221199a',
    'duplicate content': '532470701b228f413444211130312015',
    'unique content A': '11111111111111111111111111111111',
    'content of file3': '33333333333333333333333333333333',
    'content of file4': '44444444444444444444444444444444',
    'unique content C': 'cccccccccccccccccccccccccccccccc',
}

# Dynamically import the auditor module from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from auditor import calculate_file_hash, find_duplicate_files, main
sys.path.pop(0)

class TestAuditor(unittest.TestCase):

    @patch('os.walk', side_effect=lambda path: [item for item in _mock_walk_data if item[0].startswith(path)])
    @patch('os.path.isfile', side_effect=lambda path: _mock_is_file_data.get(path, False))
    @patch('os.path.isdir', side_effect=lambda path: _mock_is_dir_data.get(path, False))
    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash(self, mock_open_func, mock_isdir, mock_isfile, mock_walk):
        # Mock rationale: Test hash calculation in isolation, controlling file content.
        filepath = '/mock/dir1/file1.txt'
        mock_open_func.return_value.read.side_effect = [b'content of file1', b'']
        expected_hash = _expected_hashes['content of file1']
        self.assertEqual(calculate_file_hash(filepath), expected_hash)

        # Test with an unreadable file
        mock_open_func.side_effect = IOError("Permission denied")
        self.assertIsNone(calculate_file_hash(filepath))
        mock_open_func.side_effect = None # Reset for other tests

    @patch('os.walk', side_effect=lambda path: [item for item in _mock_walk_data if item[0].startswith(path)])
    @patch('os.path.isfile', side_effect=lambda path: _mock_is_file_data.get(path, False))
    @patch('os.path.isdir', side_effect=lambda path: _mock_is_dir_data.get(path, False))
    @patch('builtins.open', new_callable=mock_open)
    def test_find_duplicate_files(self, mock_open_func, mock_isdir, mock_isfile, mock_walk):
        # Mock rationale: Test duplicate finding logic without actual file system interaction.
        # Configure mock_open to return specific content based on filepath
        def mock_file_read(filepath, mode='rb'):
            if filepath in _mock_file_contents:
                mock_file = MagicMock()
                mock_file.__enter__.return_value.read.side_effect = [_mock_file_contents[filepath], b'']
                return mock_file
            raise FileNotFoundError(f"Mock file not found: {filepath}")

        mock_open_func.side_effect = mock_file_read

        # Test with directories containing duplicates
        duplicates = find_duplicate_files(['/mock/dir1', '/mock/dir2'])
        expected_hash = _expected_hashes['duplicate content']
        self.assertIn(expected_hash, duplicates)
        self.assertCountEqual(duplicates[expected_hash], [
            '/mock/dir1/subdirA/duplicate.txt',
            '/mock/dir2/duplicate.txt'
        ])

        # Test with an empty directory
        duplicates_empty = find_duplicate_files(['/mock/empty_dir'])
        self.assertEqual(duplicates_empty, {})

        # Test with a non-existent directory
        with patch('sys.stderr', new=StringIO()) as mock_stderr:
            duplicates_non_existent = find_duplicate_files(['/mock/non_existent'])
            self.assertEqual(duplicates_non_existent, {})
            self.assertIn("Warning: Directory not found", mock_stderr.getvalue())

        # Test with no duplicates
        duplicates_no_dupes = find_duplicate_files(['/mock/dir1/subdirB'])
        self.assertEqual(duplicates_no_dupes, {})

    @patch('os.walk', side_effect=lambda path: [item for item in _mock_walk_data if item[0].startswith(path)])
    @patch('os.path.isfile', side_effect=lambda path: _mock_is_file_data.get(path, False))
    @patch('os.path.isdir', side_effect=lambda path: _mock_is_dir_data.get(path, False))
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.remove')
    @patch('builtins.input', return_value='y') # Mock rationale: Simulate user input for deletion confirmation.
    @patch('sys.stdout', new_callable=StringIO) # Mock rationale: Capture print output for assertion.
    @patch('sys.stderr', new_callable=StringIO) # Mock rationale: Capture error output for assertion.
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_with_delete(self, mock_exit, mock_stderr, mock_stdout, mock_input, mock_remove, mock_open_func, mock_isdir, mock_isfile, mock_walk):
        # Mock rationale: Test the main execution path including argument parsing, duplicate detection, and deletion.
        # Configure mock_open for hash calculation
        def mock_file_read(filepath, mode='rb'):
            if filepath in _mock_file_contents:
                mock_file = MagicMock()
                mock_file.__enter__.return_value.read.side_effect = [_mock_file_contents[filepath], b'']
                return mock_file
            raise FileNotFoundError(f"Mock file not found: {filepath}")
        mock_open_func.side_effect = mock_file_read

        # Simulate command line arguments
        with patch('sys.argv', ['auditor.py', '/mock/dir1', '/mock/dir2', '--delete']):
            main()

            # Assertions for output and calls
            output = mock_stdout.getvalue()
            self.assertIn("Echoes found!", output)
            self.assertIn("Original: /mock/dir1/subdirA/duplicate.txt", output)
            self.assertIn("Duplicate 1: /mock/dir2/duplicate.txt", output)
            self.assertIn("Delete '/mock/dir2/duplicate.txt'? (y/N): y", output)
            self.assertIn("Deleted: /mock/dir2/duplicate.txt", output)
            self.assertIn("Total files deleted: 1", output)

            mock_remove.assert_called_once_with('/mock/dir2/duplicate.txt')
            mock_exit.assert_called_once_with(0)

    @patch('os.walk', side_effect=lambda path: [item for item in _mock_walk_data if item[0].startswith(path)])
    @patch('os.path.isfile', side_effect=lambda path: _mock_is_file_data.get(path, False))
    @patch('os.path.isdir', side_effect=lambda path: _mock_is_dir_data.get(path, False))
    @patch('builtins.open', new_callable=mock_open)
    @patch('builtins.input', return_value='n') # Mock rationale: Simulate user declining deletion.
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    @patch('os.remove')
    def test_main_without_delete_or_declined(self, mock_remove, mock_exit, mock_stderr, mock_stdout, mock_input, mock_open_func, mock_isdir, mock_isfile, mock_walk):
        # Mock rationale: Test the main execution path when deletion is not requested or declined.
        def mock_file_read(filepath, mode='rb'):
            if filepath in _mock_file_contents:
                mock_file = MagicMock()
                mock_file.__enter__.return_value.read.side_effect = [_mock_file_contents[filepath], b'']
                return mock_file
            raise FileNotFoundError(f"Mock file not found: {filepath}")
        mock_open_func.side_effect = mock_file_read

        # Test without --delete flag
        with patch('sys.argv', ['auditor.py', '/mock/dir1', '/mock/dir2']):
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Echoes found!", output)
            self.assertIn("To delete duplicates, run with the --delete flag.", output)
            mock_remove.assert_not_called()
            mock_exit.assert_called_once_with(0)

        # Reset mocks for the next part of the test
        mock_exit.reset_mock()
        mock_stdout.seek(0) # Reset StringIO buffer
        mock_stdout.truncate(0)

        # Test with --delete flag but user declines
        with patch('sys.argv', ['auditor.py', '/mock/dir1', '/mock/dir2', '--delete']):
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Skipped deletion of: /mock/dir2/duplicate.txt", output)
            mock_remove.assert_not_called()
            mock_exit.assert_called_once_with(0)

    @patch('os.walk', return_value=[]) # Mock rationale: Simulate no files found.
    @patch('os.path.isfile', return_value=False)
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_no_duplicates(self, mock_exit, mock_stderr, mock_stdout, mock_open_func, mock_isdir, mock_isfile, mock_walk):
        # Mock rationale: Test the scenario where no duplicates are found.
        with patch('sys.argv', ['auditor.py', '/mock/empty_dir']):
            main()
            output = mock_stdout.getvalue()
            self.assertIn("No echoes found. Your digital space is pristine!", output)
            mock_exit.assert_called_once_with(0)

    @patch('os.walk', side_effect=lambda path: [item for item in _mock_walk_data if item[0].startswith(path)])
    @patch('os.path.isfile', side_effect=lambda path: _mock_is_file_data.get(path, False))
    @patch('os.path.isdir', side_effect=lambda path: _mock_is_dir_data.get(path, False))
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    @patch('os.remove', side_effect=OSError("Mock permission error")) # Mock rationale: Simulate deletion failure.
    @patch('builtins.input', return_value='y')
    def test_main_delete_error(self, mock_input, mock_remove, mock_exit, mock_stderr, mock_stdout, mock_open_func, mock_isdir, mock_isfile, mock_walk):
        # Mock rationale: Test error handling during file deletion.
        def mock_file_read(filepath, mode='rb'):
            if filepath in _mock_file_contents:
                mock_file = MagicMock()
                mock_file.__enter__.return_value.read.side_effect = [_mock_file_contents[filepath], b'']
                return mock_file
            raise FileNotFoundError(f"Mock file not found: {filepath}")
        mock_open_func.side_effect = mock_file_read

        with patch('sys.argv', ['auditor.py', '/mock/dir1', '/mock/dir2', '--delete']):
            main()
            output = mock_stdout.getvalue()
            error_output = mock_stderr.getvalue()
            self.assertIn("Error deleting /mock/dir2/duplicate.txt: Mock permission error", error_output)
            mock_exit.assert_called_once_with(0)

    @patch('os.path.isdir', return_value=False) # Mock rationale: Simulate non-existent directory argument.
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    def test_main_invalid_directory_arg(self, mock_exit, mock_stderr, mock_stdout, mock_isdir):
        # Mock rationale: Test handling of invalid directory arguments.
        with patch('sys.argv', ['auditor.py', '/mock/non_existent_dir']):
            main()
            error_output = mock_stderr.getvalue()
            self.assertIn("Warning: Directory not found or not a directory: /mock/non_existent_dir", error_output)
            self.assertIn("No echoes found.", mock_stdout.getvalue())
            mock_exit.assert_called_once_with(0)

if __name__ == '__main__':
    unittest.main()
