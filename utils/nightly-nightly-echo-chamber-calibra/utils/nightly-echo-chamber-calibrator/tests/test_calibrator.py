import unittest
from unittest.mock import patch, mock_open, call
import os
import sys
import hashlib

# Add the src directory to the path to allow importing calibrator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from calibrator import calculate_file_hash, find_duplicates, main
sys.path.pop(0)

class TestCalibrator(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_small_file(self, mock_file_open):
        # Mock rationale: Simulate file content without creating actual files.
        mock_file_open.return_value.read.side_effect = [b'hello world', b'']
        
        expected_hash = hashlib.sha256(b'hello world').hexdigest()
        self.assertEqual(calculate_file_hash('dummy.txt'), expected_hash)
        mock_file_open.assert_called_once_with('dummy.txt', 'rb')

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash_large_file(self, mock_file_open):
        # Mock rationale: Simulate large file content read in blocks.
        mock_file_open.return_value.read.side_effect = [
            b'block1' * 10000,  # 60KB
            b'block2' * 5000,   # 30KB
            b''
        ]
        
        expected_hash = hashlib.sha256(b'block1' * 10000 + b'block2' * 5000).hexdigest()
        self.assertEqual(calculate_file_hash('large_dummy.txt', block_size=65536), expected_hash)
        # Ensure read was called with block_size
        mock_file_open.return_value.read.assert_has_calls([
            call(65536),
            call(65536)
        ])

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', side_effect=[10, 10, 20, 10]) # Sizes for file1, file2, file3, file4
    @patch('calibrator.calculate_file_hash', side_effect=[
        'hash_A', 'hash_A', 'hash_B', 'hash_C' # Hashes for file1, file2, file3, file4
    ])
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_find_duplicates_dry_run(self, mock_stdout, mock_hash, mock_getsize, mock_isfile, mock_walk, mock_isdir):
        # Mock rationale:
        # os.path.isdir: Simulate valid directory.
        # os.walk: Simulate directory structure with files.
        # os.path.isfile: All found paths are files.
        # os.path.getsize: Provide sizes for files to enable size-based optimization.
        # calibrator.calculate_file_hash: Control hash values for deterministic duplicate detection.
        # sys.stdout: Capture print output for verification.

        mock_walk.side_effect = [
            [('/dir1', [], ['file1.txt', 'file2.txt'])],
            [('/dir2', [], ['file3.txt', 'file4.txt'])]
        ]

        paths = ['/dir1', '/dir2']
        duplicates_found, deleted_files = find_duplicates(paths, delete_duplicates=False)

        self.assertEqual(duplicates_found, 1) # file1.txt and file2.txt are duplicates
        self.assertEqual(len(deleted_files), 0)
        output = mock_stdout.getvalue()
        self.assertIn("Duplicate Group (Hash: hash_A...):", output)
        self.assertIn("  [KEEP] /dir1/file1.txt", output)
        self.assertIn("  [DUPE] /dir1/file2.txt", output)
        self.assertNotIn("No duplicate files found.", output) # Should not be present if duplicates are found
        self.assertIn("Total duplicate groups found: 1", output)
        self.assertIn("Run with --delete to remove duplicates", output)
        mock_hash.assert_has_calls([
            call('/dir1/file1.txt', 65536),
            call('/dir1/file2.txt', 65536),
            call('/dir2/file3.txt', 65536),
            call('/dir2/file4.txt', 65536)
        ])

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', side_effect=[10, 10, 20, 10]) # Sizes for file1, file2, file3, file4
    @patch('calibrator.calculate_file_hash', side_effect=[
        'hash_A', 'hash_A', 'hash_B', 'hash_C' # Hashes for file1, file2, file3, file4
    ])
    @patch('os.remove')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_find_duplicates_delete_mode(self, mock_stdout, mock_remove, mock_hash, mock_getsize, mock_isfile, mock_walk, mock_isdir):
        # Mock rationale:
        # os.remove: Prevent actual file deletion during tests.
        # Other mocks: Same as dry run test.

        mock_walk.side_effect = [
            [('/dir1', [], ['file1.txt', 'file2.txt'])],
            [('/dir2', [], ['file3.txt', 'file4.txt'])]
        ]

        paths = ['/dir1', '/dir2']
        duplicates_found, deleted_files = find_duplicates(paths, delete_duplicates=True)

        self.assertEqual(duplicates_found, 1)
        self.assertEqual(len(deleted_files), 1)
        self.assertIn('/dir1/file2.txt', deleted_files)
        mock_remove.assert_called_once_with('/dir1/file2.txt')
        output = mock_stdout.getvalue()
        self.assertIn("Duplicate Group (Hash: hash_A...):", output)
        self.assertIn("  [KEEP] /dir1/file1.txt", output)
        self.assertIn("  [DUPE] /dir1/file2.txt", output)
        self.assertIn("         Deleted: /dir1/file2.txt", output)
        self.assertIn("Total files deleted: 1", output)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/dir', [], ['file1.txt'])])
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', return_value=10)
    @patch('calibrator.calculate_file_hash', return_value='unique_hash')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_find_duplicates_no_duplicates(self, mock_stdout, mock_hash, mock_getsize, mock_isfile, mock_walk, mock_isdir):
        # Mock rationale: Simulate a single file, ensuring no duplicates are found.
        duplicates_found, deleted_files = find_duplicates(['/dir'], delete_duplicates=False)
        self.assertEqual(duplicates_found, 0)
        self.assertEqual(len(deleted_files), 0)
        output = mock_stdout.getvalue()
        self.assertIn("No duplicate files found.", output)

    @patch('os.path.isdir', return_value=False)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_find_duplicates_invalid_path(self, mock_stdout, mock_isdir):
        # Mock rationale: Simulate an invalid directory path.
        duplicates_found, deleted_files = find_duplicates(['/invalid_dir'], delete_duplicates=False)
        self.assertEqual(duplicates_found, 0)
        self.assertEqual(len(deleted_files), 0)
        output = mock_stdout.getvalue()
        self.assertIn("Warning: Path '/invalid_dir' is not a valid directory. Skipping.", output)

    @patch('calibrator.find_duplicates', return_value=(0, []))
    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(path=['/dir'], delete=False, block_size=65536))
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_main_no_duplicates(self, mock_stdout, mock_exit, mock_args, mock_find_duplicates):
        # Mock rationale:
        # calibrator.find_duplicates: Control the outcome of the core logic.
        # argparse.ArgumentParser.parse_args: Simulate command-line arguments.
        # sys.exit: Prevent actual program exit during test.
        main()
        mock_exit.assert_called_once_with(0)

    @patch('calibrator.find_duplicates', return_value=(1, []))
    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(path=['/dir'], delete=False, block_size=65536))
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_main_duplicates_found_dry_run(self, mock_stdout, mock_exit, mock_args, mock_find_duplicates):
        # Mock rationale: Simulate duplicates found in dry run mode.
        main()
        mock_exit.assert_called_once_with(2)

    @patch('calibrator.find_duplicates', return_value=(1, ['/dir/file2.txt']))
    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(path=['/dir'], delete=True, block_size=65536))
    @patch('builtins.input', return_value='yes') # Mock rationale: Simulate user confirmation for deletion.
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_main_duplicates_deleted_success(self, mock_stdout, mock_exit, mock_input, mock_args, mock_find_duplicates):
        # Mock rationale: Simulate duplicates found and successfully deleted.
        main()
        mock_exit.assert_called_once_with(0)

    @patch('calibrator.find_duplicates', return_value=(1, []))
    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(path=['/dir'], delete=True, block_size=65536))
    @patch('builtins.input', return_value='yes') # Mock rationale: Simulate user confirmation for deletion.
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_main_duplicates_delete_failure(self, mock_stdout, mock_exit, mock_input, mock_args, mock_find_duplicates):
        # Mock rationale: Simulate deletion requested but no files actually deleted (e.g., permissions issue).
        main()
        mock_exit.assert_called_once_with(1)

    @patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(path=['/dir'], delete=True, block_size=65536))
    @patch('builtins.input', return_value='no') # Mock rationale: Simulate user cancelling deletion.
    @patch('sys.exit')
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_main_delete_cancelled(self, mock_stdout, mock_exit, mock_input, mock_args):
        # Mock rationale: Simulate user cancelling the deletion operation.
        main()
        mock_exit.assert_called_once_with(0)
        self.assertIn("Operation cancelled.", mock_stdout.getvalue())

    @patch('calibrator.calculate_file_hash', return_value=None)
    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/dir', [], ['file1.txt'])])
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', return_value=10)
    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    def test_find_duplicates_hashing_error(self, mock_stdout, mock_getsize, mock_isfile, mock_walk, mock_isdir, mock_hash):
        # Mock rationale: Simulate an error during file hashing.
        duplicates_found, deleted_files = find_duplicates(['/dir'], delete_duplicates=False)
        self.assertEqual(duplicates_found, 0)
        self.assertEqual(len(deleted_files), 0)
        output = mock_stdout.getvalue()
        self.assertIn("Error reading file /dir/file1.txt", output)
