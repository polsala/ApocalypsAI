import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
from io import StringIO

# Add the src directory to the path to allow importing purifier
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import purifier

class TestPurifier(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.sha256')
    def test_calculate_file_hash(self, mock_sha256, mock_open_func):
        # Mock rationale: Avoid actual file I/O and cryptographic operations for deterministic testing.
        # We control the file content and hash output.
        mock_file_content = b'test content'
        mock_open_func.return_value.read.side_effect = [mock_file_content, b'']
        mock_hasher_instance = MagicMock()
        mock_hasher_instance.hexdigest.return_value = 'mock_hash_value'
        mock_sha256.return_value = mock_hasher_instance

        result = purifier.calculate_file_hash('dummy_path.txt')

        mock_open_func.assert_called_once_with('dummy_path.txt', 'rb')
        mock_hasher_instance.update.assert_called_once_with(mock_file_content)
        self.assertEqual(result, 'mock_hash_value')

    @patch('builtins.open', side_effect=IOError)
    @patch('hashlib.sha256')
    def test_calculate_file_hash_io_error(self, mock_sha256, mock_open_func):
        # Mock rationale: Simulate a file that cannot be read to test error handling.
        result = purifier.calculate_file_hash('unreadable_file.txt')
        self.assertIsNone(result)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.islink', return_value=False)
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize')
    @patch('purifier.calculate_file_hash')
    def test_find_duplicates_no_duplicates(self, mock_calculate_hash, mock_getsize, mock_isfile, mock_islink, mock_walk, mock_isdir):
        # Mock rationale: Simulate a file system structure without actual files.
        # Control file sizes and hash outputs to ensure no duplicates are found.
        mock_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.txt'])
        ]
        mock_getsize.side_effect = [100, 200] # Different sizes
        mock_calculate_hash.side_effect = ['hash1', 'hash2'] # Different hashes

        duplicates = purifier.find_duplicates(['/root'])
        self.assertEqual(duplicates, {})

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.islink', return_value=False)
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize')
    @patch('purifier.calculate_file_hash')
    def test_find_duplicates_with_duplicates(self, mock_calculate_hash, mock_getsize, mock_isfile, mock_islink, mock_walk, mock_isdir):
        # Mock rationale: Simulate a file system with duplicate files.
        # Control file sizes and hash outputs to ensure duplicates are correctly identified.
        mock_walk.return_value = [
            ('/root', [], ['fileA.txt', 'fileB.txt', 'fileC.txt'])
        ]
        mock_getsize.side_effect = [100, 100, 200] # fileA and fileB same size
        mock_calculate_hash.side_effect = ['hash_dup', 'hash_dup', 'hash_unique'] # fileA and fileB same hash

        duplicates = purifier.find_duplicates(['/root'])
        expected_duplicates = {
            'hash_dup': ['/root/fileA.txt', '/root/fileB.txt']
        }
        self.assertEqual(duplicates, expected_duplicates)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.islink', return_value=False)
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize')
    @patch('purifier.calculate_file_hash')
    def test_find_duplicates_min_size(self, mock_calculate_hash, mock_getsize, mock_isfile, mock_islink, mock_walk, mock_isdir):
        # Mock rationale: Test the min_size filtering without actual files.
        mock_walk.return_value = [
            ('/root', [], ['small.txt', 'medium.txt', 'large.txt'])
        ]
        mock_getsize.side_effect = [50, 150, 250] # Sizes for files
        mock_calculate_hash.side_effect = ['hash_s', 'hash_m', 'hash_l']

        # Only medium.txt and large.txt should be considered (min_size=100)
        duplicates = purifier.find_duplicates(['/root'], min_size=100)
        self.assertEqual(duplicates, {})

        # If min_size is 0, all should be considered
        mock_getsize.side_effect = [50, 150, 250]
        mock_calculate_hash.side_effect = ['hash_s', 'hash_s', 'hash_l'] # Make small and medium duplicates
        duplicates_all = purifier.find_duplicates(['/root'], min_size=0)
        expected_duplicates_all = {
            'hash_s': ['/root/small.txt', '/root/medium.txt']
        }
        self.assertEqual(duplicates_all, expected_duplicates_all)

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.islink', return_value=False)
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize')
    @patch('purifier.calculate_file_hash')
    @patch('os.walk')
    def test_find_duplicates_exclude_dirs(self, mock_walk, mock_calculate_hash, mock_getsize, mock_isfile, mock_islink, mock_isdir):
        # Mock rationale: Verify that specified directories are skipped during os.walk.
        mock_walk.return_value = [
            ('/root', ['dir1', 'excluded_dir', 'dir2'], []), # Root has subdirs
            ('/root/dir1', [], ['file1.txt']), # file1.txt should be found
            ('/root/excluded_dir', [], ['excluded_file.txt']), # excluded_file.txt should NOT be found
            ('/root/dir2', [], ['file2.txt']) # file2.txt should be found
        ]
        mock_getsize.side_effect = [100, 100]
        mock_calculate_hash.side_effect = ['hash1', 'hash2']

        duplicates = purifier.find_duplicates(['/root'], exclude_dirs=['excluded_dir'])
        # Assert that 'excluded_file.txt' was never passed to calculate_file_hash
        self.assertNotIn('/root/excluded_dir/excluded_file.txt', [call.args[0] for call in mock_calculate_hash.call_args_list])
        # Assert that only files from non-excluded dirs are processed
        self.assertEqual(mock_calculate_hash.call_count, 2)
        self.assertEqual(duplicates, {})

    @patch('sys.stdout', new_callable=StringIO)
    def test_report_duplicates_no_duplicates(self, mock_stdout):
        # Mock rationale: Capture stdout to verify printed output without actual console interaction.
        purifier.report_duplicates({})
        self.assertIn("No duplicate files found", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_report_duplicates_with_duplicates(self, mock_stdout):
        # Mock rationale: Capture stdout to verify printed output for duplicates.
        duplicates = {
            'hash_a': ['/path/to/file1.txt', '/path/to/copy_of_file1.txt'],
            'hash_b': ['/path/to/file2.txt', '/path/to/copy_of_file2.txt', '/path/to/another_copy.txt']
        }
        purifier.report_duplicates(duplicates)
        output = mock_stdout.getvalue()
        self.assertIn("Found 2 groups of duplicate files", output)
        self.assertIn("Group 1 (Hash: hash_a...)", output)
        self.assertIn("  - /path/to/file1.txt", output)
        self.assertIn("  - /path/to/copy_of_file1.txt", output)
        self.assertIn("Group 2 (Hash: hash_b...)", output)
        self.assertIn("  - /path/to/file2.txt", output)

    @patch('builtins.input', side_effect=['y', 'n', 'y'])
    @patch('os.remove')
    @patch('sys.stdout', new_callable=StringIO)
    def test_remove_duplicates_interactive(self, mock_stdout, mock_remove, mock_input):
        # Mock rationale: Simulate user input for interactive removal and mock file deletion.
        # This ensures deterministic testing without actual file system changes or user interaction.
        duplicates = {
            'hash_a': ['/path/to/file1.txt', '/path/to/copy_of_file1.txt'],
            'hash_b': ['/path/to/file2.txt', '/path/to/copy_of_file2.txt', '/path/to/another_copy.txt']
        }
        purifier.remove_duplicates(duplicates)

        mock_input.assert_any_call("  Remove duplicate '/path/to/copy_of_file1.txt'? (y/N): ")
        mock_input.assert_any_call("  Remove duplicate '/path/to/copy_of_file2.txt'? (y/N): ")
        mock_input.assert_any_call("  Remove duplicate '/path/to/another_copy.txt'? (y/N): ")

        mock_remove.assert_any_call('/path/to/copy_of_file1.txt')
        # '/path/to/copy_of_file2.txt' was skipped (input 'n')
        mock_remove.assert_any_call('/path/to/another_copy.txt')
        self.assertEqual(mock_remove.call_count, 2)
        output = mock_stdout.getvalue()
        self.assertIn("Removed: /path/to/copy_of_file1.txt", output)
        self.assertIn("Skipped: /path/to/copy_of_file2.txt", output)
        self.assertIn("Removed: /path/to/another_copy.txt", output)
        self.assertIn("Total files removed: 2", output)

    @patch('builtins.input', side_effect=['y'])
    @patch('os.remove', side_effect=OSError('Permission denied'))
    @patch('sys.stdout', new_callable=StringIO)
    def test_remove_duplicates_os_error(self, mock_stdout, mock_remove, mock_input):
        # Mock rationale: Simulate an OSError during file removal to test error handling.
        duplicates = {
            'hash_a': ['/path/to/file1.txt', '/path/to/copy_of_file1.txt']
        }
        purifier.remove_duplicates(duplicates)
        mock_remove.assert_called_once_with('/path/to/copy_of_file1.txt')
        output = mock_stdout.getvalue()
        self.assertIn("Error removing '/path/to/copy_of_file1.txt': Permission denied", output)
        self.assertIn("Total files removed: 0", output)

    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path=['/test_dir'], remove=False, exclude=[], min_size=0))
    @patch('purifier.find_duplicates', return_value={})
    @patch('purifier.report_duplicates')
    @patch('purifier.remove_duplicates')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_duplicates_no_remove(self, mock_stdout, mock_remove_duplicates, mock_report_duplicates, mock_find_duplicates, mock_parse_args):
        # Mock rationale: Test the main function's flow without actual file operations or user input.
        # Ensure correct functions are called based on arguments.
        purifier.main()
        mock_find_duplicates.assert_called_once_with(['/test_dir'], 0, [])
        mock_report_duplicates.assert_called_once_with({})
        mock_remove_duplicates.assert_not_called()
        self.assertIn("Scanning for duplicate files in ['/test_dir']...", mock_stdout.getvalue())

    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path=['/test_dir'], remove=True, exclude=[], min_size=0))
    @patch('purifier.find_duplicates', return_value={'hash': ['f1', 'f2']})
    @patch('purifier.report_duplicates')
    @patch('purifier.remove_duplicates')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_with_duplicates_and_remove(self, mock_stdout, mock_remove_duplicates, mock_report_duplicates, mock_find_duplicates, mock_parse_args):
        # Mock rationale: Test the main function's flow when duplicates are found and removal is requested.
        purifier.main()
        mock_find_duplicates.assert_called_once_with(['/test_dir'], 0, [])
        mock_report_duplicates.assert_called_once_with({'hash': ['f1', 'f2']})
        mock_remove_duplicates.assert_called_once_with({'hash': ['f1', 'f2']})

    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(path=['/test_dir'], remove=True, exclude=[], min_size=0))
    @patch('purifier.find_duplicates', return_value={})
    @patch('purifier.report_duplicates')
    @patch('purifier.remove_duplicates')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_duplicates_with_remove_flag(self, mock_stdout, mock_remove_duplicates, mock_report_duplicates, mock_find_duplicates, mock_parse_args):
        # Mock rationale: Test the main function's flow when removal is requested but no duplicates are found.
        purifier.main()
        mock_find_duplicates.assert_called_once_with(['/test_dir'], 0, [])
        mock_report_duplicates.assert_called_once_with({})
        mock_remove_duplicates.assert_not_called()
        self.assertIn("No duplicates found, so nothing to remove.", mock_stdout.getvalue())

    @patch('os.path.isdir', side_effect=[False, True]) # First path invalid, second valid
    @patch('os.walk', return_value=[('/valid_dir', [], ['file.txt'])])
    @patch('os.path.islink', return_value=False)
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', return_value=100)
    @patch('purifier.calculate_file_hash', return_value='hash_val')
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_duplicates_invalid_path(self, mock_stdout, mock_calculate_hash, mock_getsize, mock_isfile, mock_islink, mock_walk, mock_isdir):
        # Mock rationale: Test handling of invalid directory paths passed to find_duplicates.
        duplicates = purifier.find_duplicates(['/invalid_dir', '/valid_dir'])
        self.assertIn("Warning: Path '/invalid_dir' is not a valid directory. Skipping.", mock_stdout.getvalue())
        self.assertEqual(len(duplicates), 0) # No duplicates from a single file
        mock_calculate_hash.assert_called_once_with('/valid_dir/file.txt')

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/root', [], ['file.txt'])])
    @patch('os.path.islink', return_value=False)
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', side_effect=OSError('Access denied'))
    @patch('purifier.calculate_file_hash')
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_duplicates_getsize_error(self, mock_stdout, mock_calculate_hash, mock_getsize, mock_isfile, mock_islink, mock_walk, mock_isdir):
        # Mock rationale: Simulate an OSError when getting file size to test error handling.
        duplicates = purifier.find_duplicates(['/root'])
        self.assertIn("Warning: Could not process '/root/file.txt': Access denied", mock_stdout.getvalue())
        self.assertEqual(duplicates, {})
        mock_calculate_hash.assert_not_called()

if __name__ == '__main__':
    unittest.main()
