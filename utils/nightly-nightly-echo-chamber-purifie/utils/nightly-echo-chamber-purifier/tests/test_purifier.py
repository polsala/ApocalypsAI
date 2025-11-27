import unittest
import os
import hashlib
from unittest.mock import patch, mock_open, MagicMock
from io import BytesIO

# Import the functions to be tested
from src.purifier import calculate_file_hash, find_duplicate_files, main

class TestPurifier(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash(self, mock_file_open):
        # Mock rationale: We need to simulate reading file content without actual disk I/O.
        # mock_open allows us to control what 'open()' returns and what 'read()' yields.
        mock_file_content = b"This is some test content."
        mock_file_open.return_value.read.side_effect = [
            mock_file_content[:10],
            mock_file_content[10:20],
            mock_file_content[20:],
            b'' # Simulate end of file
        ]
        
        expected_hash = hashlib.sha256(mock_file_content).hexdigest()
        
        self.assertEqual(calculate_file_hash("dummy_path.txt"), expected_hash)
        mock_file_open.assert_called_once_with("dummy_path.txt", 'rb')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getsize', return_value=100) # Mock rationale: Simulate file size for min_size_kb check.
    def test_calculate_file_hash_io_error(self, mock_getsize, mock_isfile, mock_file_open):
        # Mock rationale: Simulate an IOError during file reading.
        mock_file_open.side_effect = IOError("Permission denied")
        
        # Redirect stderr to capture the error message
        with patch('sys.stderr', new_callable=BytesIO) as mock_stderr:
            result = calculate_file_hash("unreadable_file.txt")
            self.assertIsNone(result)
            self.assertIn("Error reading file unreadable_file.txt: Permission denied", mock_stderr.getvalue().decode())

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('src.purifier.calculate_file_hash') # Mock rationale: Isolate hash calculation logic, prevent actual hashing.
    def test_find_duplicate_files_single_directory(self, mock_calculate_hash, mock_getsize, mock_walk, mock_isdir, mock_isfile, mock_exists):
        # Mock rationale: Simulate a file system structure and file properties without actual disk access.
        # This allows deterministic testing of the duplicate finding logic.

        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_isfile.side_effect = lambda p: p in [
            '/test_dir/fileA.txt', '/test_dir/fileB.txt', '/test_dir/sub/fileC.txt', '/test_dir/sub/fileD.txt'
        ]
        mock_walk.return_value = [
            ('/test_dir', [], ['fileA.txt', 'fileB.txt']),
            ('/test_dir/sub', [], ['fileC.txt', 'fileD.txt'])
        ]
        
        # Simulate file sizes
        mock_getsize.side_effect = lambda p: {
            '/test_dir/fileA.txt': 100,
            '/test_dir/fileB.txt': 100,
            '/test_dir/sub/fileC.txt': 50,
            '/test_dir/sub/fileD.txt': 100,
        }.get(p, 0)

        # Simulate hash results
        mock_calculate_hash.side_effect = lambda p, *args, **kwargs: {
            '/test_dir/fileA.txt': 'hash123',
            '/test_dir/fileB.txt': 'hash456',
            '/test_dir/sub/fileC.txt': 'hash789',
            '/test_dir/sub/fileD.txt': 'hash123', # This is a duplicate of fileA.txt
        }.get(p)

        duplicates = find_duplicate_files(['/test_dir'])
        
        expected_duplicates = {
            'hash123': ['/test_dir/fileA.txt', '/test_dir/sub/fileD.txt']
        }
        self.assertEqual(duplicates, expected_duplicates)
        
        # Verify calls
        mock_exists.assert_called_with('/test_dir')
        mock_isdir.assert_called_with('/test_dir')
        mock_walk.assert_called_once_with('/test_dir')
        self.assertEqual(mock_calculate_hash.call_count, 4) # Called for all 4 files

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('src.purifier.calculate_file_hash')
    def test_find_duplicate_files_multiple_paths_and_min_size(self, mock_calculate_hash, mock_getsize, mock_walk, mock_isdir, mock_isfile, mock_exists):
        # Mock rationale: Test scanning multiple paths and the min_size_kb filter.
        mock_exists.return_value = True
        mock_isdir.side_effect = lambda p: p in ['/dir1', '/dir2']
        mock_isfile.side_effect = lambda p: p in [
            '/dir1/large_file.txt', '/dir1/small_file.txt',
            '/dir2/another_large.txt', '/dir2/unique.txt'
        ]
        mock_walk.side_effect = [
            ('/dir1', [], ['large_file.txt', 'small_file.txt']),
            ('/dir2', [], ['another_large.txt', 'unique.txt'])
        ]
        
        mock_getsize.side_effect = lambda p: {
            '/dir1/large_file.txt': 20000, # 20KB
            '/dir1/small_file.txt': 500,   # 0.5KB
            '/dir2/another_large.txt': 20000, # 20KB, duplicate of large_file.txt
            '/dir2/unique.txt': 15000, # 15KB
        }.get(p, 0)

        mock_calculate_hash.side_effect = lambda p, *args, **kwargs: {
            '/dir1/large_file.txt': 'hash_large_dup',
            '/dir1/small_file.txt': 'hash_small',
            '/dir2/another_large.txt': 'hash_large_dup',
            '/dir2/unique.txt': 'hash_unique',
        }.get(p)

        # Test with min_size_kb = 10 (10KB)
        duplicates = find_duplicate_files(['/dir1', '/dir2'], min_size_kb=10)
        
        expected_duplicates = {
            'hash_large_dup': ['/dir1/large_file.txt', '/dir2/another_large.txt']
        }
        self.assertEqual(duplicates, expected_duplicates)
        
        # Verify that small_file.txt was ignored due to size
        self.assertNotIn('/dir1/small_file.txt', [f for files in duplicates.values() for f in files])
        self.assertEqual(mock_calculate_hash.call_count, 3) # Only called for files >= 10KB

    @patch('os.path.exists', return_value=False)
    @patch('sys.stderr', new_callable=BytesIO)
    def test_find_duplicate_files_path_not_found(self, mock_stderr, mock_exists):
        # Mock rationale: Simulate a non-existent path and check for warning output.
        duplicates = find_duplicate_files(['/non_existent_dir'])
        self.assertEqual(duplicates, {})
        self.assertIn("Warning: Path not found: /non_existent_dir", mock_stderr.getvalue().decode())

    @patch('src.purifier.find_duplicate_files', return_value={})
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_no_duplicates(self, mock_print, mock_exit, mock_parse_args, mock_find_duplicates):
        # Mock rationale: Simulate command-line arguments and the outcome of find_duplicate_files.
        # This allows testing the main function's control flow and output.
        mock_parse_args.return_value = MagicMock(
            paths=['/test_dir'],
            hash_algo='sha256',
            min_size_kb=0,
            output_format='text'
        )
        
        main()
        mock_find_duplicates.assert_called_once_with(['/test_dir'], 'sha256', min_size_kb=0)
        mock_print.assert_any_call("No duplicate files found. The echo chamber is pure!")
        mock_exit.assert_called_once_with(0)

    @patch('src.purifier.find_duplicate_files', return_value={
        'hash123': ['/test_dir/fileA.txt', '/test_dir/fileB.txt']
    })
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_duplicates_text_output(self, mock_print, mock_exit, mock_parse_args, mock_find_duplicates):
        # Mock rationale: Simulate command-line arguments and the outcome of find_duplicate_files
        # to test text output format.
        mock_parse_args.return_value = MagicMock(
            paths=['/test_dir'],
            hash_algo='sha256',
            min_size_kb=0,
            output_format='text'
        )
        
        main()
        mock_find_duplicates.assert_called_once()
        mock_print.assert_any_call("\n--- Duplicate Files Found ---")
        mock_print.assert_any_call("Hash: hash123")
        mock_print.assert_any_call("  - /test_dir/fileA.txt")
        mock_print.assert_any_call("  - /test_dir/fileB.txt")
        mock_exit.assert_called_once_with(1)

    @patch('src.purifier.find_duplicate_files', return_value={
        'hash123': ['/test_dir/fileA.txt', '/test_dir/fileB.txt']
    })
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_duplicates_json_output(self, mock_print, mock_exit, mock_parse_args, mock_find_duplicates):
        # Mock rationale: Simulate command-line arguments and the outcome of find_duplicate_files
        # to test JSON output format.
        mock_parse_args.return_value = MagicMock(
            paths=['/test_dir'],
            hash_algo='sha256',
            min_size_kb=0,
            output_format='json'
        )
        
        main()
        mock_find_duplicates.assert_called_once()
        # Check if json.dumps was called with the correct data
        expected_json_output = '{\n  "hash123": [\n    "/test_dir/fileA.txt",\n    "/test_dir/fileB.txt"\n  ]\n}'
        mock_print.assert_any_call(expected_json_output)
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
