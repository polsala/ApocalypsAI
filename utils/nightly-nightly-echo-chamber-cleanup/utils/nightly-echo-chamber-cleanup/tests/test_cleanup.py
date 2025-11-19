import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys

# Add the src directory to the path to allow importing cleanup.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import cleanup

class TestCleanup(unittest.TestCase):

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.sha256')
    def test_find_duplicates_no_duplicates(self, mock_sha256, mock_open_file, mock_getsize, mock_walk):
        # Mock rationale: Simulate a directory with unique files to ensure no duplicates are found.
        mock_walk.return_value = [
            ('/tmp/test_dir', [], ['file1.txt', 'file2.txt'])
        ]
        mock_getsize.side_effect = [100, 200] # Different sizes
        mock_sha256.return_value.hexdigest.side_effect = ['hash1', 'hash2']

        duplicates, savings = cleanup.find_duplicates('/tmp/test_dir')
        self.assertEqual(duplicates, {})
        self.assertEqual(savings, 0)

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.sha256')
    def test_find_duplicates_with_duplicates(self, mock_sha256, mock_open_file, mock_getsize, mock_walk):
        # Mock rationale: Simulate a directory with duplicate files (same size, same hash) and unique files.
        mock_walk.return_value = [
            ('/tmp/test_dir', [], ['fileA.txt', 'fileB.txt', 'fileC.txt', 'unique.log'])
        ]
        # fileA.txt and fileB.txt are duplicates (same size, same hash)
        # fileC.txt has same size as A/B but different hash
        # unique.log is unique
        mock_getsize.side_effect = [100, 100, 100, 500]
        mock_sha256_instance = MagicMock()
        mock_sha256.return_value = mock_sha256_instance
        mock_sha256_instance.hexdigest.side_effect = ['hash_dup', 'hash_dup', 'hash_diff', 'hash_unique']

        duplicates, savings = cleanup.find_duplicates('/tmp/test_dir')

        expected_duplicates = {
            'hash_dup': [
                os.path.join('/tmp/test_dir', 'fileA.txt'),
                os.path.join('/tmp/test_dir', 'fileB.txt')
            ]
        }
        self.assertEqual(duplicates, expected_duplicates)
        self.assertEqual(savings, 100) # One duplicate of size 100

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.sha256')
    def test_find_duplicates_multiple_groups(self, mock_sha256, mock_open_file, mock_getsize, mock_walk):
        # Mock rationale: Simulate multiple groups of duplicates with different sizes and hashes.
        mock_walk.return_value = [
            ('/tmp/test_dir', [], ['f1.txt', 'f2.txt', 'g1.log', 'g2.log', 'g3.log'])
        ]
        # f1, f2 are duplicates (size 100, hash_A)
        # g1, g2, g3 are duplicates (size 200, hash_B)
        mock_getsize.side_effect = [100, 100, 200, 200, 200]
        mock_sha256_instance = MagicMock()
        mock_sha256.return_value = mock_sha256_instance
        mock_sha256_instance.hexdigest.side_effect = ['hash_A', 'hash_A', 'hash_B', 'hash_B', 'hash_B']

        duplicates, savings = cleanup.find_duplicates('/tmp/test_dir')

        expected_duplicates = {
            'hash_A': [
                os.path.join('/tmp/test_dir', 'f1.txt'),
                os.path.join('/tmp/test_dir', 'f2.txt')
            ],
            'hash_B': [
                os.path.join('/tmp/test_dir', 'g1.log'),
                os.path.join('/tmp/test_dir', 'g2.log'),
                os.path.join('/tmp/test_dir', 'g3.log')
            ]
        }
        self.assertEqual(duplicates, expected_duplicates)
        self.assertEqual(savings, 100 * 1 + 200 * 2) # (100 * (2-1)) + (200 * (3-1)) = 100 + 400 = 500

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.sha256')
    def test_find_duplicates_empty_directory(self, mock_sha256, mock_open_file, mock_getsize, mock_walk):
        # Mock rationale: Simulate an empty directory to ensure no files are processed.
        mock_walk.return_value = [
            ('/tmp/empty_dir', [], [])
        ]

        duplicates, savings = cleanup.find_duplicates('/tmp/empty_dir')
        self.assertEqual(duplicates, {})
        self.assertEqual(savings, 0)

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=mock_open)
    @patch('hashlib.sha256')
    def test_find_duplicates_inaccessible_file(self, mock_sha256, mock_open_file, mock_getsize, mock_walk):
        # Mock rationale: Simulate a file that becomes inaccessible during processing (e.g., deleted or permission error).
        mock_walk.return_value = [
            ('/tmp/test_dir', [], ['accessible.txt', 'inaccessible.txt'])
        ]
        mock_getsize.side_effect = [100, OSError("Permission denied")]
        mock_sha256.return_value.hexdigest.side_effect = ['hash_acc']

        duplicates, savings = cleanup.find_duplicates('/tmp/test_dir')
        self.assertEqual(duplicates, {})
        self.assertEqual(savings, 0)

    @patch('os.path.isdir', return_value=True)
    @patch('cleanup.find_duplicates', return_value=({}, 0))
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_duplicates_found(self, mock_exit, mock_print, mock_find_duplicates, mock_isdir):
        # Mock rationale: Test the main function's behavior when no duplicates are found.
        # Mock find_duplicates to return empty, print to capture output, sys.exit to prevent actual exit.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(directory='/tmp/test_dir', delete=False)):
            cleanup.main()
            mock_print.assert_any_call("No duplicate files found. Your echo chamber is pristine!")
            mock_exit.assert_called_once_with(0)

    @patch('os.path.isdir', return_value=True)
    @patch('cleanup.find_duplicates', return_value=(
        {'hash_dup': ['/tmp/test_dir/fileA.txt', '/tmp/test_dir/fileB.txt']},
        100
    ))
    @patch('builtins.print')
    @patch('sys.exit')
    @patch('builtins.input', return_value='no')
    def test_main_dry_run_report(self, mock_input, mock_exit, mock_print, mock_find_duplicates, mock_isdir):
        # Mock rationale: Test the main function's dry-run reporting behavior.
        # Mock find_duplicates to return some duplicates, print to capture output, sys.exit to prevent actual exit.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(directory='/tmp/test_dir', delete=False)):
            cleanup.main()
            mock_print.assert_any_call("\n--- Duplicate Files Found ---")
            mock_print.assert_any_call("\nThis was a dry run. No files were deleted. Use --delete to remove duplicates.")
            mock_exit.assert_called_once_with(0)

    @patch('os.path.isdir', return_value=True)
    @patch('cleanup.find_duplicates', return_value=(
        {'hash_dup': ['/tmp/test_dir/fileA.txt', '/tmp/test_dir/fileB.txt']},
        100
    ))
    @patch('builtins.print')
    @patch('sys.exit')
    @patch('builtins.input', return_value='yes')
    @patch('os.remove')
    @patch('os.path.getsize', return_value=100) # Mock getsize for deletion calculation
    def test_main_delete_confirmed(self, mock_getsize, mock_remove, mock_input, mock_exit, mock_print, mock_find_duplicates, mock_isdir):
        # Mock rationale: Test the main function's deletion behavior when confirmed.
        # Mock find_duplicates to return duplicates, input to simulate 'yes', os.remove to check calls.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(directory='/tmp/test_dir', delete=True)):
            cleanup.main()
            mock_input.assert_called_once_with("\nAre you sure you want to DELETE these duplicate files? (yes/no): ")
            mock_remove.assert_called_once_with('/tmp/test_dir/fileB.txt')
            mock_print.assert_any_call("  Deleted: /tmp/test_dir/fileB.txt")
            mock_print.assert_any_call("\nDeletion complete. Removed 1 files, saving 100.00 B.")
            mock_exit.assert_called_once_with(0)

    @patch('os.path.isdir', return_value=True)
    @patch('cleanup.find_duplicates', return_value=(
        {'hash_dup': ['/tmp/test_dir/fileA.txt', '/tmp/test_dir/fileB.txt']},
        100
    ))
    @patch('builtins.print')
    @patch('sys.exit')
    @patch('builtins.input', return_value='no')
    @patch('os.remove')
    def test_main_delete_cancelled(self, mock_remove, mock_input, mock_exit, mock_print, mock_find_duplicates, mock_isdir):
        # Mock rationale: Test the main function's deletion cancellation behavior.
        # Mock input to simulate 'no', ensure os.remove is NOT called.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(directory='/tmp/test_dir', delete=True)):
            cleanup.main()
            mock_input.assert_called_once_with("\nAre you sure you want to DELETE these duplicate files? (yes/no): ")
            mock_remove.assert_not_called()
            mock_print.assert_any_call("Deletion cancelled.")
            mock_exit.assert_called_once_with(2)

    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_invalid_directory(self, mock_exit, mock_print, mock_isdir):
        # Mock rationale: Test handling of an invalid directory path.
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(directory='/nonexistent', delete=False)):
            cleanup.main()
            mock_print.assert_any_call(unittest.mock.ANY, file=sys.stderr) # Check for error message to stderr
            mock_exit.assert_called_once_with(1)

    def test_format_bytes(self):
        # Mock rationale: This is a pure function, no mocks needed.
        self.assertEqual(cleanup.format_bytes(0), "0.00 B")
        self.assertEqual(cleanup.format_bytes(100), "100.00 B")
        self.assertEqual(cleanup.format_bytes(1024), "1.00 KB")
        self.assertEqual(cleanup.format_bytes(1024 * 1024), "1.00 MB")
        self.assertEqual(cleanup.format_bytes(1024 * 1024 * 1024), "1.00 GB")
        self.assertEqual(cleanup.format_bytes(1024 * 1024 * 1024 * 1024), "1.00 TB")
        self.assertEqual(cleanup.format_bytes(1536), "1.50 KB")
        self.assertEqual(cleanup.format_bytes(1024**5), "1.00 PB")
