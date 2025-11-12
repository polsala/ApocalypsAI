import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Import the functions from the utility script
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from dust_bunny_sweeper import is_dust_bunny, find_dust_bunnies, remove_dust_bunny, main, DUST_BUNNY_PATTERNS

class TestDustBunnySweeper(unittest.TestCase):

    def test_is_dust_bunny_file_patterns(self):
        self.assertTrue(is_dust_bunny('/path/to/file.tmp', DUST_BUNNY_PATTERNS))
        self.assertTrue(is_dust_bunny('/path/to/log.txt.log', DUST_BUNNY_PATTERNS))
        self.assertTrue(is_dust_bunny('/path/to/backup.bak', DUST_BUNNY_PATTERNS))
        self.assertTrue(is_dust_bunny('/path/to/vim.swp', DUST_BUNNY_PATTERNS))
        self.assertTrue(is_dust_bunny('/path/to/.DS_Store', DUST_BUNNY_PATTERNS))
        self.assertFalse(is_dust_bunny('/path/to/important.txt', DUST_BUNNY_PATTERNS))
        self.assertFalse(is_dust_bunny('/path/to/image.jpg', DUST_BUNNY_PATTERNS))

    @patch('os.path.isdir', return_value=True)
    def test_is_dust_bunny_directory_patterns(self, mock_isdir):
        # Mock rationale: os.path.isdir is called to differentiate between file and directory patterns.
        self.assertTrue(is_dust_bunny('/path/to/cache', DUST_BUNNY_PATTERNS))
        self.assertTrue(is_dust_bunny('/path/to/__pycache__', DUST_BUNNY_PATTERNS))
        self.assertTrue(is_dust_bunny('/path/to/node_modules', DUST_BUNNY_PATTERNS))
        self.assertFalse(is_dust_bunny('/path/to/my_project', DUST_BUNNY_PATTERNS))

    @patch('os.walk')
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isdir', side_effect=lambda p: 'dir' in p) # Mock for find_dust_bunnies to distinguish dirs
    def test_find_dust_bunnies_dry_run(self, mock_isdir, mock_exists, mock_walk):
        # Mock rationale: os.walk simulates the file system traversal without actual disk I/O.
        # Mock rationale: os.path.exists ensures the root path is considered valid.
        # Mock rationale: os.path.isdir helps distinguish files from directories for pattern matching.
        mock_walk.return_value = [
            ('/root', ['dir_cache', 'dir_project'], ['file.tmp', 'file.log', 'important.txt']),
            ('/root/dir_project', [], ['subfile.bak'])
        ]
        
        # Test with default patterns
        bunnies = find_dust_bunnies(['/root'], DUST_BUNNY_PATTERNS)
        expected_bunnies = [
            '/root/dir_cache', # Directory pattern
            '/root/file.tmp',
            '/root/file.log',
            '/root/dir_project/subfile.bak' # File pattern in sub-directory
        ]
        self.assertCountEqual(bunnies, expected_bunnies)

        # Test with a custom pattern
        custom_patterns = ['.custom']
        mock_walk.return_value = [
            ('/root', [], ['file.custom', 'other.txt'])
        ]
        bunnies = find_dust_bunnies(['/root'], custom_patterns)
        self.assertCountEqual(bunnies, ['/root/file.custom'])

    @patch('os.walk')
    @patch('os.path.exists', return_value=False)
    @patch('sys.stderr', new_callable=MagicMock)
    def test_find_dust_bunnies_non_existent_path(self, mock_stderr, mock_exists, mock_walk):
        # Mock rationale: os.path.exists simulates a non-existent path.
        # Mock rationale: sys.stderr captures error output without printing to console.
        bunnies = find_dust_bunnies(['/non/existent/path'], DUST_BUNNY_PATTERNS)
        self.assertEqual(bunnies, [])
        mock_stderr.write.assert_called_with("Warning: Path '/non/existent/path' does not exist. Skipping.\n")
        mock_walk.assert_not_called()

    @patch('shutil.rmtree')
    @patch('os.remove')
    @patch('os.path.isdir', side_effect=[True, False]) # First call isdir for dir, second for file
    def test_remove_dust_bunny(self, mock_isdir, mock_remove, mock_rmtree):
        # Mock rationale: shutil.rmtree and os.remove simulate file/directory deletion without actual disk I/O.
        # Mock rationale: os.path.isdir helps determine which deletion function to call.
        remove_dust_bunny('/path/to/dir_cache')
        mock_rmtree.assert_called_once_with('/path/to/dir_cache')
        mock_remove.assert_not_called()

        mock_rmtree.reset_mock()
        mock_remove.reset_mock()

        remove_dust_bunny('/path/to/file.tmp')
        mock_remove.assert_called_once_with('/path/to/file.tmp')
        mock_rmtree.assert_not_called()

    @patch('argparse.ArgumentParser.parse_args')
    @patch('dust_bunny_sweeper.find_dust_bunnies', return_value=[])
    @patch('builtins.print')
    def test_main_no_bunnies_found(self, mock_print, mock_find_bunnies, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args simulates command-line arguments.
        # Mock rationale: find_dust_bunnies simulates the core logic of finding files.
        # Mock rationale: builtins.print captures output without printing to console.
        mock_parse_args.return_value = MagicMock(paths=['.'], dry_run=False, force=False, verbose=False)
        main()
        mock_find_bunnies.assert_called_once_with(['.'], DUST_BUNNY_PATTERNS, False)
        mock_print.assert_any_call("\n🎉 Hooray! No digital dust bunnies found. Your system is sparkling clean!")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('dust_bunny_sweeper.find_dust_bunnies', return_value=['/path/to/file.tmp', '/path/to/dir_cache'])
    @patch('builtins.print')
    @patch('builtins.input', return_value='y')
    @patch('dust_bunny_sweeper.remove_dust_bunny')
    def test_main_with_deletion_confirmation(self, mock_remove_bunny, mock_input, mock_print, mock_find_bunnies, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args simulates command-line arguments.
        # Mock rationale: find_dust_bunnies simulates the core logic of finding files.
        # Mock rationale: builtins.print captures output without printing to console.
        # Mock rationale: builtins.input simulates user confirmation.
        # Mock rationale: remove_dust_bunny simulates the actual deletion process.
        mock_parse_args.return_value = MagicMock(paths=['.'], dry_run=False, force=False, verbose=False)
        main()
        mock_find_bunnies.assert_called_once()
        mock_input.assert_called_once()
        self.assertEqual(mock_remove_bunny.call_count, 2)
        mock_remove_bunny.assert_any_call('/path/to/file.tmp')
        mock_remove_bunny.assert_any_call('/path/to/dir_cache')
        mock_print.assert_any_call("\n🚀 Your system feels lighter already! (2 items swept away)!\n")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('dust_bunny_sweeper.find_dust_bunnies', return_value=['/path/to/file.tmp'])
    @patch('builtins.print')
    @patch('builtins.input', return_value='n')
    @patch('dust_bunny_sweeper.remove_dust_bunny')
    def test_main_with_deletion_cancellation(self, mock_remove_bunny, mock_input, mock_print, mock_find_bunnies, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args simulates command-line arguments.
        # Mock rationale: find_dust_bunnies simulates the core logic of finding files.
        # Mock rationale: builtins.print captures output without printing to console.
        # Mock rationale: builtins.input simulates user cancellation.
        # Mock rationale: remove_dust_bunny ensures no deletion occurs.
        mock_parse_args.return_value = MagicMock(paths=['.'], dry_run=False, force=False, verbose=False)
        main()
        mock_find_bunnies.assert_called_once()
        mock_input.assert_called_once()
        mock_remove_bunny.assert_not_called()
        mock_print.assert_any_call("\n🧹 Cleanup cancelled. Your dust bunnies live to see another day.")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('dust_bunny_sweeper.find_dust_bunnies', return_value=['/path/to/file.tmp'])
    @patch('builtins.print')
    @patch('dust_bunny_sweeper.remove_dust_bunny')
    def test_main_dry_run_mode(self, mock_remove_bunny, mock_print, mock_find_bunnies, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args simulates command-line arguments.
        # Mock rationale: find_dust_bunnies simulates the core logic of finding files.
        # Mock rationale: builtins.print captures output without printing to console.
        # Mock rationale: remove_dust_bunny ensures no deletion occurs in dry-run.
        mock_parse_args.return_value = MagicMock(paths=['.'], dry_run=True, force=False, verbose=False)
        main()
        mock_find_bunnies.assert_called_once()
        mock_remove_bunny.assert_not_called()
        mock_print.assert_any_call("\n--- DRY RUN MODE --- No files will be deleted. --- ")
        mock_print.assert_any_call("\n--- DRY RUN COMPLETE --- No changes were made. --- ")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('dust_bunny_sweeper.find_dust_bunnies', return_value=['/path/to/file.tmp'])
    @patch('builtins.print')
    @patch('dust_bunny_sweeper.remove_dust_bunny', side_effect=OSError("Permission denied"))
    @patch('sys.stderr', new_callable=MagicMock)
    def test_main_deletion_error_handling(self, mock_stderr, mock_remove_bunny, mock_print, mock_find_bunnies, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args simulates command-line arguments.
        # Mock rationale: find_dust_bunnies simulates the core logic of finding files.
        # Mock rationale: builtins.print captures output without printing to console.
        # Mock rationale: remove_dust_bunny simulates a deletion failure.
        # Mock rationale: sys.stderr captures error output without printing to console.
        mock_parse_args.return_value = MagicMock(paths=['.'], dry_run=False, force=True, verbose=False)
        main()
        mock_find_bunnies.assert_called_once()
        mock_remove_bunny.assert_called_once_with('/path/to/file.tmp')
        mock_stderr.write.assert_any_call("  [ERROR] Could not delete /path/to/file.tmp: Permission denied\n")
        mock_print.assert_any_call("\n🚀 Your system feels lighter already! (0 items swept away)!\n") # 0 because deletion failed

    @patch('argparse.ArgumentParser.parse_args')
    @patch('dust_bunny_sweeper.find_dust_bunnies', return_value=['/path/to/file.tmp'])
    @patch('builtins.print')
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    @patch('dust_bunny_sweeper.remove_dust_bunny')
    def test_main_keyboard_interrupt_cancellation(self, mock_remove_bunny, mock_input, mock_print, mock_find_bunnies, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args simulates command-line arguments.
        # Mock rationale: find_dust_bunnies simulates the core logic of finding files.
        # Mock rationale: builtins.print captures output without printing to console.
        # Mock rationale: builtins.input simulates a KeyboardInterrupt during confirmation.
        # Mock rationale: remove_dust_bunny ensures no deletion occurs.
        mock_parse_args.return_value = MagicMock(paths=['.'], dry_run=False, force=False, verbose=False)
        main()
        mock_find_bunnies.assert_called_once()
        mock_input.assert_called_once()
        mock_remove_bunny.assert_not_called()
        mock_print.assert_any_call("\n🧹 Cleanup interrupted. Your dust bunnies live to see another day.")
