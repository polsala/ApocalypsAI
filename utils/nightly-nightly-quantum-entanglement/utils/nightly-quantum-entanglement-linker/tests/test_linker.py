import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
import hashlib

# Mock rationale: Temporarily add 'src' to sys.path to allow direct import of linker.py
# This simulates the module being available for import as 'linker' for testing purposes.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import linker
sys.path.pop(0) # Clean up sys.path after import

class TestLinker(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_hash(self, mock_file_open):
        # Mock rationale: Avoid actual file I/O for deterministic hashing.
        # We control the content that `open` returns.
        mock_file_open.return_value.read.side_effect = [b'content', b' of ', b'file', b'']
        expected_hash = hashlib.sha256(b'content of file').hexdigest()
        self.assertEqual(linker.calculate_hash('dummy_path.txt'), expected_hash)

        mock_file_open.return_value.read.side_effect = [b'another', b'']
        expected_hash = hashlib.sha256(b'another').hexdigest()
        self.assertEqual(linker.calculate_hash('another_dummy.txt'), expected_hash)

        # Test IOError
        mock_file_open.side_effect = IOError("Permission denied")
        with patch('sys.stderr', new_callable=MagicMock) as mock_stderr:
            self.assertEqual(linker.calculate_hash('unreadable.txt'), "")
            mock_stderr.write.assert_called_once()
            self.assertIn("Error reading file", mock_stderr.write.call_args[0][0])

    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.islink', return_value=False)
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('linker.calculate_hash') # Mock rationale: Isolate find_duplicates from hash calculation details
    def test_find_duplicates(self, mock_calculate_hash, mock_getsize, mock_walk, mock_islink, mock_isfile, mock_exists):
        # Mock rationale: Simulate file system structure and file properties without actual disk access.
        # `os.walk` controls the files found.
        # `os.path.getsize` controls file sizes for initial grouping.
        # `linker.calculate_hash` provides deterministic hashes.

        # Scenario 1: No duplicates
        mock_walk.return_value = [
            ('/root', [], ['fileA.txt', 'fileB.txt'])
        ]
        mock_getsize.side_effect = [100, 200]
        mock_calculate_hash.side_effect = ['hashA', 'hashB']
        self.assertEqual(linker.find_duplicates(['/root']), {})

        # Scenario 2: Duplicates by size, then by hash
        mock_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.txt', 'file3.txt', 'unique.txt'])
        ]
        mock_getsize.side_effect = [100, 100, 100, 200] # file1, file2, file3 are same size
        mock_calculate_hash.side_effect = ['hashX', 'hashX', 'hashY', 'hashZ'] # file1, file2 are duplicates

        expected_duplicates = {
            'hashX': ['/root/file1.txt', '/root/file2.txt']
        }
        self.assertEqual(linker.find_duplicates(['/root']), expected_duplicates)

        # Scenario 3: Empty file (should be skipped)
        mock_walk.return_value = [
            ('/root', [], ['empty.txt', 'file1.txt'])
        ]
        mock_getsize.side_effect = [0, 100]
        mock_calculate_hash.side_effect = ['hashE', 'hashF'] # Hash for empty file, then for file1
        self.assertEqual(linker.find_duplicates(['/root']), {})

        # Scenario 4: Path not found
        mock_exists.return_value = False
        with patch('sys.stderr', new_callable=MagicMock) as mock_stderr:
            self.assertEqual(linker.find_duplicates(['/nonexistent']), {})
            mock_stderr.write.assert_called_once()
            self.assertIn("Warning: Path not found", mock_stderr.write.call_args[0][0])
        mock_exists.return_value = True # Reset for subsequent tests

        # Scenario 5: OSError during getsize
        mock_walk.return_value = [
            ('/root', [], ['bad_file.txt', 'good_file.txt'])
        ]
        mock_getsize.side_effect = [OSError("Permission denied"), 100]
        mock_calculate_hash.side_effect = ['hashG'] # Only good_file will be hashed
        with patch('sys.stderr', new_callable=MagicMock) as mock_stderr:
            self.assertEqual(linker.find_duplicates(['/root']), {})
            mock_stderr.write.assert_called_once()
            self.assertIn("Error getting size", mock_stderr.write.call_args[0][0])

    @patch('sys.stdout', new_callable=MagicMock)
    def test_process_duplicates_report(self, mock_stdout):
        # Mock rationale: Capture print output to verify reporting behavior.
        duplicate_map = {
            'hash1': ['/path/to/file1.txt', '/path/to/copy1.txt', '/path/to/another_copy1.txt'],
            'hash2': ['/path/to/file2.jpg', '/path/to/copy2.jpg']
        }
        linker.process_duplicates(duplicate_map, 'report')

        output = mock_stdout.write.call_args_list
        # Note: filepaths are sorted alphabetically for deterministic canonical selection
        self.assertIn("Processing 2 sets of duplicate files", output[0][0][0])
        self.assertIn("Canonical: /path/to/another_copy1.txt", output[2][0][0])
        self.assertIn("Duplicate: /path/to/copy1.txt", output[3][0][0])
        self.assertIn("Duplicate: /path/to/file1.txt", output[4][0][0])
        self.assertIn("Canonical: /path/to/copy2.jpg", output[6][0][0])
        self.assertIn("Duplicate: /path/to/file2.jpg", output[7][0][0])

    @patch('os.remove')
    @patch('sys.stdout', new_callable=MagicMock)
    def test_process_duplicates_delete(self, mock_stdout, mock_remove):
        # Mock rationale: Prevent actual file deletion. Verify `os.remove` calls.
        duplicate_map = {
            'hash1': ['/path/to/file1.txt', '/path/to/copy1.txt', '/path/to/another_copy1.txt']
        }
        linker.process_duplicates(duplicate_map, 'delete')

        # The two non-canonical files should be removed
        mock_remove.assert_any_call('/path/to/copy1.txt')
        mock_remove.assert_any_call('/path/to/file1.txt')
        self.assertEqual(mock_remove.call_count, 2)
        output = mock_stdout.write.call_args_list
        self.assertIn("Deleted: /path/to/copy1.txt", output[3][0][0])
        self.assertIn("Deleted: /path/to/file1.txt", output[4][0][0])

        # Test delete error
        mock_remove.reset_mock() # Reset mocks for new test scenario
        mock_remove.side_effect = OSError("Permission denied")
        with patch('sys.stderr', new_callable=MagicMock) as mock_stderr:
            linker.process_duplicates(duplicate_map, 'delete')
            mock_stderr.write.assert_called()
            self.assertIn("Error deleting", mock_stderr.write.call_args[0][0])

    @patch('os.link')
    @patch('os.remove') # For removing duplicate before hardlinking
    @patch('os.path.exists', return_value=True)
    @patch('os.stat') # For checking if already hardlinked
    @patch('sys.stdout', new_callable=MagicMock)
    def test_process_duplicates_hardlink(self, mock_stdout, mock_stat, mock_exists, mock_remove, mock_link):
        # Mock rationale: Prevent actual file system changes. Verify `os.link` and `os.remove` calls.
        # `os.stat` is mocked to simulate inode numbers for hardlink checks.
        duplicate_map = {
            'hash1': ['/path/to/file1.txt', '/path/to/copy1.txt', '/path/to/another_copy1.txt']
        }

        # Simulate different inodes initially for all files
        mock_stat_obj_canonical = MagicMock(st_ino=100)
        mock_stat_obj_dup1 = MagicMock(st_ino=101)
        mock_stat_obj_dup2 = MagicMock(st_ino=102)
        mock_stat.side_effect = [
            mock_stat_obj_canonical, # os.stat('/path/to/another_copy1.txt')
            mock_stat_obj_dup1,      # os.stat('/path/to/copy1.txt')
            mock_stat_obj_canonical, # os.stat('/path/to/another_copy1.txt')
            mock_stat_obj_dup2,      # os.stat('/path/to/file1.txt')
            mock_stat_obj_canonical  # os.stat('/path/to/another_copy1.txt')
        ]

        linker.process_duplicates(duplicate_map, 'hardlink')

        # The two non-canonical files should be removed before linking
        mock_remove.assert_any_call('/path/to/copy1.txt')
        mock_remove.assert_any_call('/path/to/file1.txt')
        self.assertEqual(mock_remove.call_count, 2)

        # Hardlinks should be created from canonical to duplicates
        mock_link.assert_any_call('/path/to/another_copy1.txt', '/path/to/copy1.txt')
        mock_link.assert_any_call('/path/to/another_copy1.txt', '/path/to/file1.txt')
        self.assertEqual(mock_link.call_count, 2)

        output = mock_stdout.write.call_args_list
        self.assertIn("Hardlinked: /path/to/copy1.txt -> /path/to/another_copy1.txt", output[3][0][0])
        self.assertIn("Hardlinked: /path/to/file1.txt -> /path/to/another_copy1.txt", output[4][0][0])

        # Test already hardlinked scenario
        mock_remove.reset_mock()
        mock_link.reset_mock()
        mock_stat.side_effect = [
            mock_stat_obj_canonical, # os.stat('/path/to/another_copy1.txt')
            mock_stat_obj_canonical, # os.stat('/path/to/copy1.txt') - simulates already hardlinked
            mock_stat_obj_canonical, # os.stat('/path/to/another_copy1.txt')
            mock_stat_obj_dup2,      # os.stat('/path/to/file1.txt')
            mock_stat_obj_canonical  # os.stat('/path/to/another_copy1.txt')
        ]
        linker.process_duplicates(duplicate_map, 'hardlink')
        # Only the second duplicate should be processed (removed and linked)
        mock_remove.assert_called_once_with('/path/to/file1.txt')
        mock_link.assert_called_once_with('/path/to/another_copy1.txt', '/path/to/file1.txt')
        output = mock_stdout.write.call_args_list
        self.assertIn("Already hardlinked: /path/to/copy1.txt", output[3][0][0])

        # Test hardlink error
        mock_link.side_effect = OSError("Cross-device link")
        mock_remove.reset_mock()
        mock_stat.side_effect = [
            mock_stat_obj_canonical, # os.stat('/path/to/another_copy1.txt')
            mock_stat_obj_dup1,      # os.stat('/path/to/copy1.txt')
            mock_stat_obj_canonical, # os.stat('/path/to/another_copy1.txt')
            mock_stat_obj_dup2,      # os.stat('/path/to/file1.txt')
            mock_stat_obj_canonical  # os.stat('/path/to/another_copy1.txt')
        ]
        with patch('sys.stderr', new_callable=MagicMock) as mock_stderr:
            linker.process_duplicates(duplicate_map, 'hardlink')
            mock_stderr.write.assert_called()
            self.assertIn("Error hardlinking", mock_stderr.write.call_args[0][0])

    @patch('sys.stdout', new_callable=MagicMock)
    def test_process_duplicates_no_duplicates(self, mock_stdout):
        # Mock rationale: Verify behavior when no duplicates are found.
        linker.process_duplicates({}, 'report')
        mock_stdout.write.assert_called_once_with("No duplicate files found.\n")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('linker.find_duplicates')
    @patch('linker.process_duplicates')
    def test_main(self, mock_process_duplicates, mock_find_duplicates, mock_parse_args):
        # Mock rationale: Isolate main function from its dependencies.
        # Simulate command-line arguments and verify calls to core logic.
        mock_args = MagicMock()
        mock_args.paths = ['/test/path1', '/test/path2']
        mock_args.action = 'delete'
        mock_parse_args.return_value = mock_args

        mock_duplicates = {'hashA': ['file1', 'file2']}
        mock_find_duplicates.return_value = mock_duplicates

        linker.main()

        mock_find_duplicates.assert_called_once_with(['/test/path1', '/test/path2'])
        mock_process_duplicates.assert_called_once_with(mock_duplicates, 'delete')

if __name__ == '__main__':
    unittest.main()
