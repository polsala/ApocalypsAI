import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import hashlib
from collections import defaultdict

# Import functions from the harmonizer script
# Assuming harmonizer.py is in src/
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import harmonizer

class TestHarmonizer(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.sha256')
    def test_calculate_file_hash(self, mock_sha256, mock_file_open):
        # Mock rationale: We don't want to read actual files or perform real hashing during tests.
        # `mock_file_open` simulates file content, and `mock_sha256` ensures a deterministic hash output.
        mock_file_open.return_value.read.side_effect = [b'block1', b'block2', b'']
        mock_hasher = MagicMock()
        mock_hasher.hexdigest.return_value = 'mock_hash_value'
        mock_sha256.return_value = mock_hasher

        result = harmonizer.calculate_file_hash('dummy_path.txt')
        self.assertEqual(result, 'mock_hash_value')
        mock_file_open.assert_called_once_with('dummy_path.txt', 'rb')
        mock_hasher.update.assert_any_call(b'block1')
        mock_hasher.update.assert_any_call(b'block2')
        mock_hasher.hexdigest.assert_called_once()

    @patch('builtins.open', side_effect=IOError('Permission denied'))
    @patch('sys.stdout', new_callable=MagicMock)
    def test_calculate_file_hash_io_error(self, mock_stdout, mock_open_file):
        # Mock rationale: Test error handling when file reading fails.
        with self.assertRaisesRegex(IOError, "Could not read file 'bad_path.txt': Permission denied"):
            harmonizer.calculate_file_hash('bad_path.txt')

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.join', side_effect=os.path.join) # Use real join for paths
    @patch('os.path.islink', return_value=False)
    @patch('harmonizer.calculate_file_hash') # Mock rationale: Isolate hash calculation from file system traversal.
    def test_find_duplicate_files(self, mock_calculate_hash, mock_islink, mock_join, mock_walk, mock_isdir):
        # Mock rationale: `os.walk` is mocked to simulate a directory structure without needing actual files.
        # `calculate_file_hash` is mocked to provide deterministic hashes.
        # `os.path.isdir` and `os.path.islink` are mocked for control.

        # Simulate a directory structure with duplicates
        mock_walk.side_effect = [
            [('/dir1', [], ['fileA.txt', 'fileB.txt', 'fileC.txt'])],
            [('/dir2', [], ['fileX.txt', 'fileY.txt'])]
        ]

        # Assign deterministic hashes to files
        mock_calculate_hash.side_effect = {
            os.path.join('/dir1', 'fileA.txt'): 'hash1',
            os.path.join('/dir1', 'fileB.txt'): 'hash2',
            os.path.join('/dir1', 'fileC.txt'): 'hash1', # Duplicate of fileA
            os.path.join('/dir2', 'fileX.txt'): 'hash3',
            os.path.join('/dir2', 'fileY.txt'): 'hash1', # Duplicate of fileA and fileC
        }.get

        directories = ['/dir1', '/dir2']
        duplicates = harmonizer.find_duplicate_files(directories)

        expected_duplicates = {
            'hash1': [
                os.path.join('/dir1', 'fileA.txt'),
                os.path.join('/dir1', 'fileC.txt'),
                os.path.join('/dir2', 'fileY.txt')
            ]
        }
        self.assertDictEqual(duplicates, expected_duplicates)
        mock_isdir.assert_any_call('/dir1')
        mock_isdir.assert_any_call('/dir2')
        self.assertEqual(mock_calculate_hash.call_count, 5) # Called for each file

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/dir1', [], ['linkA.txt'])])
    @patch('os.path.islink', return_value=True)
    @patch('harmonizer.calculate_file_hash')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_find_duplicate_files_skips_symlinks(self, mock_stdout, mock_calculate_hash, mock_islink, mock_walk, mock_isdir):
        # Mock rationale: Ensure symbolic links are correctly skipped during file traversal.
        directories = ['/dir1']
        duplicates = harmonizer.find_duplicate_files(directories)
        self.assertDictEqual(duplicates, {})
        mock_islink.assert_called_once_with(os.path.join('/dir1', 'linkA.txt'))
        mock_calculate_hash.assert_not_called()

    @patch('os.path.isdir', return_value=False)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_find_duplicate_files_non_existent_dir(self, mock_stdout, mock_isdir):
        # Mock rationale: Test error handling for non-existent directories without actual file system checks.
        duplicates = harmonizer.find_duplicate_files(['/nonexistent'])
        self.assertDictEqual(duplicates, {})
        mock_stdout.write.assert_any_call("Warning: Directory '/nonexistent' not found or is not a directory. Skipping.\n")

    @patch('os.remove')
    @patch('os.link')
    @patch('os.path.getsize', return_value=1024)
    @patch('os.path.samefile', return_value=False)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_harmonize_duplicates_live_run(self, mock_stdout, mock_samefile, mock_getsize, mock_link, mock_remove):
        # Mock rationale: `os.remove`, `os.link`, `os.path.getsize`, `os.path.samefile` are mocked
        # to prevent actual file system modifications and provide deterministic outcomes.
        duplicate_groups = {
            'hash1': ['/dir/master.txt', '/dir/duplicate1.txt', '/dir/duplicate2.txt']
        }
        harmonizer.harmonize_duplicates(duplicate_groups, dry_run=False)

        mock_remove.assert_any_call('/dir/duplicate1.txt')
        mock_link.assert_any_call('/dir/master.txt', '/dir/duplicate1.txt')
        mock_remove.assert_any_call('/dir/duplicate2.txt')
        mock_link.assert_any_call('/dir/master.txt', '/dir/duplicate2.txt')
        self.assertEqual(mock_remove.call_count, 2)
        self.assertEqual(mock_link.call_count, 2)
        mock_stdout.write.assert_any_call("Total files linked: 2\n")
        mock_stdout.write.assert_any_call("Total potential space saved: 2048 bytes\n")

    @patch('os.remove')
    @patch('os.link')
    @patch('os.path.getsize', return_value=1024)
    @patch('os.path.samefile', return_value=False)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_harmonize_duplicates_dry_run(self, mock_stdout, mock_samefile, mock_getsize, mock_link, mock_remove):
        # Mock rationale: Verify that no file system changes occur during a dry run.
        duplicate_groups = {
            'hash1': ['/dir/master.txt', '/dir/duplicate1.txt']
        }
        harmonizer.harmonize_duplicates(duplicate_groups, dry_run=True)

        mock_remove.assert_not_called()
        mock_link.assert_not_called()
        mock_stdout.write.assert_any_call("--- DRY RUN COMPLETE ---\n")
        mock_stdout.write.assert_any_call("No changes were made to the file system.\n")

    @patch('os.remove')
    @patch('os.link', side_effect=OSError("Permission denied"))
    @patch('os.path.getsize', return_value=1024)
    @patch('os.path.samefile', return_value=False)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_harmonize_duplicates_os_error(self, mock_stdout, mock_samefile, mock_getsize, mock_link, mock_remove):
        # Mock rationale: Test error handling when `os.link` fails (e.g., due to permissions).
        duplicate_groups = {
            'hash1': ['/dir/master.txt', '/dir/duplicate1.txt']
        }
        harmonizer.harmonize_duplicates(duplicate_groups, dry_run=False)

        mock_remove.assert_called_once_with('/dir/duplicate1.txt')
        mock_link.assert_called_once_with('/dir/master.txt', '/dir/duplicate1.txt')
        mock_stdout.write.assert_any_call("  Error processing '/dir/duplicate1.txt': Permission denied\n")
        mock_stdout.write.assert_any_call("Total files linked: 0\n") # No files were successfully linked

    @patch('os.remove')
    @patch('os.link')
    @patch('os.path.getsize', return_value=1024)
    @patch('os.path.samefile', return_value=True) # Simulate already linked
    @patch('sys.stdout', new_callable=MagicMock)
    def test_harmonize_duplicates_already_linked(self, mock_stdout, mock_samefile, mock_getsize, mock_link, mock_remove):
        # Mock rationale: Ensure that files already hardlinked to the master are skipped.
        duplicate_groups = {
            'hash1': ['/dir/master.txt', '/dir/already_linked.txt']
        }
        harmonizer.harmonize_duplicates(duplicate_groups, dry_run=False)

        mock_remove.assert_not_called()
        mock_link.assert_not_called()
        mock_stdout.write.assert_any_call("  Skipping '/dir/already_linked.txt' - already hardlinked to master.\n")
        mock_stdout.write.assert_any_call("Total files linked: 0\n")

    @patch('harmonizer.find_duplicate_files', return_value={})
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_no_duplicates(self, mock_stdout, mock_find_duplicates):
        # Mock rationale: Test the main function's behavior when no duplicates are found.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(directories=['/test_dir'], dry_run=False)):
            harmonizer.main()
            mock_stdout.write.assert_any_call("\nNo quantum duplicates detected. Your data is already harmonized!\n")
            mock_find_duplicates.assert_called_once_with(['/test_dir'])

    @patch('harmonizer.find_duplicate_files', return_value={'hash1': ['/dir/master.txt', '/dir/duplicate1.txt']})
    @patch('harmonizer.harmonize_duplicates')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_with_duplicates(self, mock_stdout, mock_harmonize, mock_find_duplicates):
        # Mock rationale: Test the main function's flow when duplicates are found, ensuring `harmonize_duplicates` is called.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(directories=['/test_dir'], dry_run=True)):
            harmonizer.main()
            mock_find_duplicates.assert_called_once_with(['/test_dir'])
            mock_harmonize.assert_called_once_with({'hash1': ['/dir/master.txt', '/dir/duplicate1.txt']}, dry_run=True)
            mock_stdout.write.assert_any_call("\nDetected 1 groups of quantum duplicates.\n")

if __name__ == '__main__':
    unittest.main()
