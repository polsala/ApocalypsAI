import unittest
from unittest.mock import patch, mock_open
import os
import hashlib
from collections import defaultdict
from src.deduplicator import calculate_file_hash, find_duplicate_files, remove_duplicate_files, main

class TestDeduplicator(unittest.TestCase):

    # Mock rationale: os.path.isfile is a file system operation that needs to be controlled for deterministic tests.
    @patch('os.path.isfile')
    # Mock rationale: open is a file system operation that needs to be controlled for deterministic tests.
    @patch('builtins.open', new_callable=mock_open)
    def test_calculate_file_hash(self, mock_file_open, mock_isfile):
        mock_isfile.return_value = True
        mock_file_open.return_value.read.side_effect = [b"content1", b"content2", b""]
        
        # Test with a known content
        expected_hash = hashlib.sha256(b"content1content2").hexdigest()
        self.assertEqual(calculate_file_hash("dummy_path.txt"), expected_hash)
        mock_file_open.assert_called_with("dummy_path.txt", 'rb')

        # Test with non-existent file
        mock_isfile.return_value = False
        self.assertIsNone(calculate_file_hash("non_existent.txt"))

    # Mock rationale: os.path.isdir is a file system operation that needs to be controlled for deterministic tests.
    @patch('os.path.isdir')
    # Mock rationale: os.walk is a file system operation that needs to be controlled for deterministic tests.
    @patch('os.walk')
    # Mock rationale: os.path.join is a path manipulation function, mocking it ensures consistent paths in tests.
    @patch('os.path.join', side_effect=os.path.join) # Use real join for path construction
    # Mock rationale: calculate_file_hash is an internal dependency, mocking it allows controlling hash values directly.
    @patch('src.deduplicator.calculate_file_hash')
    def test_find_duplicate_files(self, mock_calculate_hash, mock_join, mock_walk, mock_isdir):
        mock_isdir.return_value = True
        
        # Mock a directory structure with duplicates
        mock_walk.return_value = [
            ('/tmp/test_dir', [], ['fileA.txt', 'fileB.txt', 'fileC.txt', 'fileD.txt']),
            ('/tmp/test_dir/subdir', [], ['fileE.txt'])
        ]
        
        # Mock hash values
        mock_calculate_hash.side_effect = {
            '/tmp/test_dir/fileA.txt': 'hash1',
            '/tmp/test_dir/fileB.txt': 'hash2',
            '/tmp/test_dir/fileC.txt': 'hash1', # Duplicate of fileA
            '/tmp/test_dir/fileD.txt': 'hash3',
            '/tmp/test_dir/subdir/fileE.txt': 'hash2', # Duplicate of fileB
        }.get

        expected_duplicates = {
            'hash1': ['/tmp/test_dir/fileA.txt', '/tmp/test_dir/fileC.txt'],
            'hash2': ['/tmp/test_dir/fileB.txt', '/tmp/test_dir/subdir/fileE.txt']
        }
        
        result = find_duplicate_files('/tmp/test_dir')
        self.assertEqual(result, expected_duplicates)

        # Test with no duplicates
        mock_calculate_hash.side_effect = {
            '/tmp/test_dir/fileA.txt': 'hash1',
            '/tmp/test_dir/fileB.txt': 'hash2',
        }.get
        mock_walk.return_value = [('/tmp/test_dir', [], ['fileA.txt', 'fileB.txt'])]
        self.assertEqual(find_duplicate_files('/tmp/test_dir'), {})

        # Test with non-existent directory
        mock_isdir.return_value = False
        with self.assertRaises(FileNotFoundError):
            find_duplicate_files('/non_existent_dir')

    # Mock rationale: os.remove is a file system operation that needs to be controlled for deterministic tests.
    @patch('os.remove')
    def test_remove_duplicate_files_dry_run(self, mock_os_remove):
        duplicates_map = {
            'hash1': ['/tmp/test_dir/fileA.txt', '/tmp/test_dir/fileC.txt'],
            'hash2': ['/tmp/test_dir/fileB.txt', '/tmp/test_dir/subdir/fileE.txt']
        }
        
        removed = remove_duplicate_files(duplicates_map, dry_run=True)
        self.assertEqual(set(removed), set(['/tmp/test_dir/fileC.txt', '/tmp/test_dir/subdir/fileE.txt']))
        mock_os_remove.assert_not_called() # Should not call remove in dry run

    # Mock rationale: os.remove is a file system operation that needs to be controlled for deterministic tests.
    @patch('os.remove')
    def test_remove_duplicate_files_live_run(self, mock_os_remove):
        duplicates_map = {
            'hash1': ['/tmp/test_dir/fileA.txt', '/tmp/test_dir/fileC.txt'],
            'hash2': ['/tmp/test_dir/fileB.txt', '/tmp/test_dir/subdir/fileE.txt']
        }
        
        removed = remove_duplicate_files(duplicates_map, dry_run=False)
        self.assertEqual(set(removed), set(['/tmp/test_dir/fileC.txt', '/tmp/test_dir/subdir/fileE.txt']))
        
        # Ensure os.remove was called for the correct files
        mock_os_remove.assert_any_call('/tmp/test_dir/fileC.txt')
        mock_os_remove.assert_any_call('/tmp/test_dir/subdir/fileE.txt')
        self.assertEqual(mock_os_remove.call_count, 2)

    # Mock rationale: sys.argv is used to pass command-line arguments, mocking it allows testing CLI behavior.
    @patch('sys.argv', ['deduplicator.py', '/tmp/test_dir', '--remove'])
    # Mock rationale: print is used for output, mocking it allows capturing and asserting on console output.
    @patch('builtins.print')
    # Mock rationale: find_duplicate_files is an internal dependency, mocking it allows controlling the input to main.
    @patch('src.deduplicator.find_duplicate_files')
    # Mock rationale: remove_duplicate_files is an internal dependency, mocking it allows controlling the output of main.
    @patch('src.deduplicator.remove_duplicate_files')
    def test_main_remove_verbose(self, mock_remove_duplicates, mock_find_duplicates, mock_print):
        mock_find_duplicates.return_value = {
            'hash1': ['/tmp/test_dir/fileA.txt', '/tmp/test_dir/fileC.txt'],
        }
        mock_remove_duplicates.return_value = ['/tmp/test_dir/fileC.txt']

        # Add --verbose to sys.argv for this test
        with patch('sys.argv', ['deduplicator.py', '/tmp/test_dir', '--remove', '--verbose']):
            main()
            mock_find_duplicates.assert_called_with('/tmp/test_dir')
            mock_remove_duplicates.assert_called_with(
                {'hash1': ['/tmp/test_dir/fileA.txt', '/tmp/test_dir/fileC.txt']},
                dry_run=False
            )
            # Check for specific print calls indicating removal and verbose output
            mock_print.assert_any_call("Successfully removed 1 duplicate files.")
            mock_print.assert_any_call("Removed files:")
            mock_print.assert_any_call("  - /tmp/test_dir/fileC.txt")

    # Mock rationale: sys.argv is used to pass command-line arguments, mocking it allows testing CLI behavior.
    @patch('sys.argv', ['deduplicator.py', '/tmp/test_dir']) # No --remove, so dry run
    # Mock rationale: print is used for output, mocking it allows capturing and asserting on console output.
    @patch('builtins.print')
    # Mock rationale: find_duplicate_files is an internal dependency, mocking it allows controlling the input to main.
    @patch('src.deduplicator.find_duplicate_files')
    # Mock rationale: remove_duplicate_files is an internal dependency, mocking it allows controlling the output of main.
    @patch('src.deduplicator.remove_duplicate_files')
    def test_main_dry_run(self, mock_remove_duplicates, mock_find_duplicates, mock_print):
        mock_find_duplicates.return_value = {
            'hash1': ['/tmp/test_dir/fileA.txt', '/tmp/test_dir/fileC.txt'],
        }
        mock_remove_duplicates.return_value = ['/tmp/test_dir/fileC.txt']

        main()
        mock_find_duplicates.assert_called_with('/tmp/test_dir')
        mock_remove_duplicates.assert_called_with(
            {'hash1': ['/tmp/test_dir/fileA.txt', '/tmp/test_dir/fileC.txt']},
            dry_run=True
        )
        # Check for specific print calls indicating dry run
        mock_print.assert_any_call("Would remove 1 duplicate files.")
        mock_print.assert_any_call("\n--- Dry Run: Duplicates would be removed with --remove ---")

    # Mock rationale: sys.argv is used to pass command-line arguments, mocking it allows testing CLI behavior.
    @patch('sys.argv', ['deduplicator.py', '/tmp/test_dir'])
    # Mock rationale: print is used for output, mocking it allows capturing and asserting on console output.
    @patch('builtins.print')
    # Mock rationale: find_duplicate_files is an internal dependency, mocking it allows controlling the input to main.
    @patch('src.deduplicator.find_duplicate_files')
    def test_main_no_duplicates(self, mock_find_duplicates, mock_print):
        mock_find_duplicates.return_value = {} # No duplicates found

        main()
        mock_find_duplicates.assert_called_with('/tmp/test_dir')
        mock_print.assert_any_call("No duplicate files found across all scanned directories.")

    # Mock rationale: sys.argv is used to pass command-line arguments, mocking it allows testing CLI behavior.
    @patch('sys.argv', ['deduplicator.py', '/non_existent_dir'])
    # Mock rationale: print is used for output, mocking it allows capturing and asserting on console output.
    @patch('builtins.print')
    # Mock rationale: find_duplicate_files is an internal dependency, mocking it allows controlling the input to main.
    @patch('src.deduplicator.find_duplicate_files', side_effect=FileNotFoundError("Directory not found: /non_existent_dir"))
    def test_main_directory_not_found(self, mock_find_duplicates, mock_print):
        main()
        mock_print.assert_any_call("Error: Directory not found: /non_existent_dir")

    # Mock rationale: sys.argv is used to pass command-line arguments, mocking it allows testing CLI behavior.
    @patch('sys.argv', ['deduplicator.py'])
    # Mock rationale: print is used for output, mocking it allows capturing and asserting on console output.
    @patch('builtins.print')
    # Mock rationale: argparse.ArgumentParser.print_help is called when no directories are provided, mocking it allows asserting on this behavior.
    @patch('argparse.ArgumentParser.print_help')
    def test_main_no_directories_provided(self, mock_print_help, mock_print):
        main()
        mock_print.assert_any_call("Error: No directories provided. Please specify one or more directories to scan.")
        mock_print_help.assert_called_once()


if __name__ == '__main__':
    unittest.main()
