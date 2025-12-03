import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
import hashlib

# Add the src directory to the path to allow importing purifier
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import purifier

class TestPurifier(unittest.TestCase):

    def setUp(self):
        # Mock os.walk to simulate a file system structure
        # Mock rationale: Avoids actual file system traversal, making tests fast and isolated.
        self.mock_walk_data = [
            ('/mock_dir', ['subdir1', 'subdir2'], ['fileA.txt', 'fileB.txt']),
            ('/mock_dir/subdir1', [], ['fileC.txt', 'duplicateA.txt']),
            ('/mock_dir/subdir2', [], ['fileD.txt', 'duplicateA_copy.txt', 'empty.txt'])
        ]
        self.mock_files = {
            '/mock_dir/fileA.txt': b'content of file A',
            '/mock_dir/fileB.txt': b'content of file B',
            '/mock_dir/subdir1/fileC.txt': b'content of file C',
            '/mock_dir/subdir1/duplicateA.txt': b'content of file A', # Duplicate of fileA.txt
            '/mock_dir/subdir2/fileD.txt': b'content of file D',
            '/mock_dir/subdir2/duplicateA_copy.txt': b'content of file A', # Another duplicate of fileA.txt
            '/mock_dir/subdir2/empty.txt': b'' # Empty file
        }
        self.mock_file_sizes = {
            filepath: len(content) for filepath, content in self.mock_files.items()
        }

        # Pre-calculate hashes for verification
        self.hash_A = hashlib.sha256(b'content of file A').hexdigest()
        self.hash_B = hashlib.sha256(b'content of file B').hexdigest()
        self.hash_C = hashlib.sha256(b'content of file C').hexdigest()
        self.hash_D = hashlib.sha256(b'content of file D').hexdigest()
        self.hash_empty = hashlib.sha256(b'').hexdigest()

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.isfile', side_effect=lambda x: x in self.mock_files)
    @patch('os.path.getsize', side_effect=lambda x: self.mock_file_sizes.get(x, 0))
    @patch('builtins.open', new_callable=mock_open)
    def test_find_duplicates(self, mock_open_func, mock_getsize, mock_isfile, mock_walk, mock_isdir):
        # Mock rationale:
        # os.path.isdir: Ensures the initial directory check passes.
        # os.walk: Simulates directory structure traversal.
        # os.path.isfile: Controls which entries are treated as files.
        # os.path.getsize: Provides mocked file sizes for optimization.
        # builtins.open: Prevents actual file I/O during hash calculation.

        mock_walk.return_value = self.mock_walk_data

        # Configure mock_open to return specific content for each file path
        def mock_open_side_effect(filepath, mode='r', *args, **kwargs):
            if 'b' in mode:
                mock_file = MagicMock()
                # Simulate reading the entire content in one go, then EOF
                mock_file.__enter__.return_value.read.side_effect = [
                    self.mock_files.get(filepath, b''), b''
                ]
                return mock_file
            raise ValueError(f"Only binary read mode 'rb' is supported for this mock, got {mode}.")
        mock_open_func.side_effect = mock_open_side_effect

        duplicates = purifier.find_duplicates('/mock_dir')

        self.assertIn(self.hash_A, duplicates)
        self.assertEqual(len(duplicates[self.hash_A]), 3)
        self.assertIn('/mock_dir/fileA.txt', duplicates[self.hash_A])
        self.assertIn('/mock_dir/subdir1/duplicateA.txt', duplicates[self.hash_A])
        self.assertIn('/mock_dir/subdir2/duplicateA_copy.txt', duplicates[self.hash_A])

        self.assertNotIn(self.hash_B, duplicates) # Not a duplicate
        self.assertNotIn(self.hash_C, duplicates) # Not a duplicate
        self.assertNotIn(self.hash_D, duplicates) # Not a duplicate
        self.assertNotIn(self.hash_empty, duplicates) # Empty files are skipped from hashing

        self.assertEqual(len(duplicates), 1) # Only one group of duplicates

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.isfile', side_effect=lambda x: x in self.mock_files)
    @patch('os.path.getsize', side_effect=lambda x: self.mock_file_sizes.get(x, 0))
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.remove')
    @patch('sys.stdout', new_callable=MagicMock) # Mock stdout to capture print statements
    def test_main_delete_duplicates(self, mock_stdout, mock_remove, mock_open_func, mock_getsize, mock_isfile, mock_walk, mock_isdir):
        # Mock rationale:
        # os.remove: Prevents actual file deletion, allowing verification of deletion logic without side effects.
        # sys.stdout: Captures print output for verification, preventing console clutter.
        # Other mocks: Same as test_find_duplicates.

        mock_walk.return_value = self.mock_walk_data

        def mock_open_side_effect(filepath, mode='r', *args, **kwargs):
            if 'b' in mode:
                mock_file = MagicMock()
                mock_file.__enter__.return_value.read.side_effect = [
                    self.mock_files.get(filepath, b''), b''
                ]
                return mock_file
            raise ValueError(f"Only binary read mode 'rb' is supported for this mock, got {mode}.")
        mock_open_func.side_effect = mock_open_side_effect

        # Simulate command line arguments
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(directory='/mock_dir', delete=True)):
            purifier.main()

        # Verify os.remove was called for the duplicates, but not the original
        mock_remove.assert_any_call('/mock_dir/subdir1/duplicateA.txt')
        mock_remove.assert_any_call('/mock_dir/subdir2/duplicateA_copy.txt')
        self.assertEqual(mock_remove.call_count, 2)
        self.assertNotIn(('/mock_dir/fileA.txt',), mock_remove.call_args_list) # Original should not be deleted

        # Verify output contains deletion messages
        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)
        self.assertIn("-> Deleted: /mock_dir/subdir1/duplicateA.txt", output_str)
        self.assertIn("-> Deleted: /mock_dir/subdir2/duplicateA_copy.txt", output_str)
        self.assertIn("Successfully deleted 2 duplicate files.", output_str)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('os.path.isfile', side_effect=lambda x: x in self.mock_files)
    @patch('os.path.getsize', side_effect=lambda x: self.mock_file_sizes.get(x, 0))
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_no_duplicates(self, mock_stdout, mock_open_func, mock_getsize, mock_isfile, mock_walk, mock_isdir):
        # Mock rationale: Same as test_main_delete_duplicates, but without os.remove.

        # Modify mock_walk_data to have no duplicates
        no_dup_walk_data = [
            ('/mock_dir', ['subdir1'], ['fileA.txt', 'fileB.txt']),
            ('/mock_dir/subdir1', [], ['fileC.txt', 'fileD.txt'])
        ]
        no_dup_files = {
            '/mock_dir/fileA.txt': b'content of file A',
            '/mock_dir/fileB.txt': b'content of file B',
            '/mock_dir/subdir1/fileC.txt': b'content of file C',
            '/mock_dir/subdir1/fileD.txt': b'content of file D',
        }
        no_dup_file_sizes = {
            k: len(v) for k, v in no_dup_files.items()
        }

        mock_walk.return_value = no_dup_walk_data
        mock_isfile.side_effect = lambda x: x in no_dup_files
        mock_getsize.side_effect = lambda x: no_dup_file_sizes.get(x, 0)

        def mock_open_side_effect(filepath, mode='r', *args, **kwargs):
            if 'b' in mode:
                mock_file = MagicMock()
                mock_file.__enter__.return_value.read.side_effect = [
                    no_dup_files.get(filepath, b''), b''
                ]
                return mock_file
            raise ValueError(f"Only binary read mode 'rb' is supported for this mock, got {mode}.")
        mock_open_func.side_effect = mock_open_side_effect

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(directory='/mock_dir', delete=False)):
            purifier.main()

        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)
        self.assertIn("No duplicate files found. Your digital echo chamber is pure!", output_str)

    @patch('os.path.isdir', return_value=False)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_find_duplicates_invalid_directory(self, mock_stdout, mock_isdir):
        # Mock rationale:
        # os.path.isdir: Simulates an invalid directory path.
        # sys.stdout: Captures print output for verification.

        duplicates = purifier.find_duplicates('/non_existent_dir')
        self.assertEqual(duplicates, {})
        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)
        self.assertIn("Error: Directory '/non_existent_dir' not found.", output_str)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/mock_dir', [], ['empty.txt'])])
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', return_value=0)
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_empty_file_handling(self, mock_stdout, mock_open_func, mock_getsize, mock_isfile, mock_walk, mock_isdir):
        # Mock rationale: Simulates a directory with only empty files, which should be skipped.

        mock_open_func.return_value.__enter__.return_value.read.side_effect = [b'', b'']

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(directory='/mock_dir', delete=False)):
            purifier.main()

        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)
        self.assertIn("No duplicate files found. Your digital echo chamber is pure!", output_str)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/mock_dir', [], ['unreadable.txt'])])
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', side_effect=OSError("Permission denied"))
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_unreadable_file_getsize(self, mock_stdout, mock_open_func, mock_getsize, mock_isfile, mock_walk, mock_isdir):
        # Mock rationale: Simulates a file that cannot be read (e.g., permission denied) during getsize.

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(directory='/mock_dir', delete=False)):
            purifier.main()

        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)
        self.assertIn("No duplicate files found. Your digital echo chamber is pure!", output_str)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[('/mock_dir', [], ['unhashable.txt'])])
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', return_value=100)
    @patch('builtins.open', side_effect=IOError("Cannot open file"))
    @patch('sys.stdout', new_callable=MagicMock)
    def test_main_unhashable_file(self, mock_stdout, mock_open_func, mock_getsize, mock_isfile, mock_walk, mock_isdir):
        # Mock rationale: Simulates a file that cannot be opened for hashing.

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(directory='/mock_dir', delete=False)):
            purifier.main()

        output = mock_stdout.write.call_args_list
        output_str = "".join(call.args[0] for call in output)
        self.assertIn("No duplicate files found. Your digital echo chamber is pure!", output_str)

if __name__ == '__main__':
    unittest.main()
