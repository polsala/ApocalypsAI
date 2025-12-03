import unittest
from unittest.mock import patch, MagicMock, call
import os
import shutil
import sys
from io import StringIO

# Add the src directory to the Python path for direct import in tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import dust_collector
sys.path.pop(0) # Clean up sys.path after import

class TestDustCollector(unittest.TestCase):

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile', return_value=True)
    def test_find_dust_files_by_size(self, mock_isfile, mock_getsize, mock_walk):
        # Mock rationale: Simulate a file system structure and file sizes without actual disk I/O.
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log', 'subdir/file3.tmp']),
            ('/test_dir/subdir', [], ['file3.tmp'])
        ]
        mock_getsize.side_effect = lambda x: {
            '/test_dir/file1.txt': 50,
            '/test_dir/file2.log': 1500,
            '/test_dir/subdir/file3.tmp': 80
        }.get(x, 0)

        dust_files = dust_collector.find_dust_files('/test_dir', max_size=100, empty_only=False)
        self.assertEqual(len(dust_files), 2)
        self.assertIn(('/test_dir/file1.txt', 50), dust_files)
        self.assertIn(('/test_dir/subdir/file3.tmp', 80), dust_files)
        self.assertNotIn(('/test_dir/file2.log', 1500), dust_files)

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile', return_value=True)
    def test_find_dust_files_empty_only(self, mock_isfile, mock_getsize, mock_walk):
        # Mock rationale: Simulate files with various sizes, specifically testing the empty_only flag.
        mock_walk.return_value = [
            ('/test_dir', [], ['empty.txt', 'small.log', 'large.dat'])
        ]
        mock_getsize.side_effect = lambda x: {
            '/test_dir/empty.txt': 0,
            '/test_dir/small.log': 50,
            '/test_dir/large.dat': 2000
        }.get(x, 0)

        dust_files = dust_collector.find_dust_files('/test_dir', max_size=100, empty_only=True)
        self.assertEqual(len(dust_files), 1)
        self.assertIn(('/test_dir/empty.txt', 0), dust_files)
        self.assertNotIn(('/test_dir/small.log', 50), dust_files)

    @patch('builtins.print')
    def test_list_dust_files(self, mock_print):
        # Mock rationale: Capture stdout to verify correct output without actual printing.
        dust_files = [('/path/to/dust1.txt', 10), ('/path/to/dust2.log', 50)]
        dust_collector.list_dust_files(dust_files)
        mock_print.assert_any_call("\n--- Cosmic Dust Report ---")
        mock_print.assert_any_call("- /path/to/dust1.txt (10 bytes)")
        mock_print.assert_any_call("- /path/to/dust2.log (50 bytes)")

    @patch('builtins.print')
    def test_list_dust_files_no_dust(self, mock_print):
        # Mock rationale: Capture stdout to verify correct output when no dust is found.
        dust_collector.list_dust_files([])
        mock_print.assert_called_once_with("No cosmic dust found. Your repository is sparkling clean!")

    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.relpath', side_effect=lambda path, start: path.replace(start + os.sep, '')) # Mock rationale: Simulate relative path calculation.
    @patch('builtins.print')
    def test_archive_dust_files(self, mock_print, mock_relpath, mock_move, mock_makedirs):
        # Mock rationale: Prevent actual file system changes (makedirs, move) and capture stdout.
        base_path = '/test_repo'
        archive_dir_name = '.archive'
        dust_files = [
            ('/test_repo/file1.txt', 10),
            ('/test_repo/subdir/file2.log', 50)
        ]

        dust_collector.archive_dust_files(dust_files, base_path, archive_dir_name, dry_run=False)

        mock_makedirs.assert_any_call(os.path.join(base_path, archive_dir_name), exist_ok=True)
        mock_makedirs.assert_any_call(os.path.join(base_path, archive_dir_name, 'subdir'), exist_ok=True)

        mock_move.assert_any_call('/test_repo/file1.txt', os.path.join(base_path, archive_dir_name, 'file1.txt'))
        mock_move.assert_any_call('/test_repo/subdir/file2.log', os.path.join(base_path, archive_dir_name, 'subdir', 'file2.log'))
        self.assertEqual(mock_move.call_count, 2)
        mock_print.assert_any_call(f"Archived: /test_repo/file1.txt -> {os.path.join(base_path, archive_dir_name, 'file1.txt')}")

    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.relpath', side_effect=lambda path, start: path.replace(start + os.sep, ''))
    @patch('builtins.print')
    def test_archive_dust_files_dry_run(self, mock_print, mock_relpath, mock_move, mock_makedirs):
        # Mock rationale: Verify dry-run output without performing actual file system operations.
        base_path = '/test_repo'
        archive_dir_name = '.archive'
        dust_files = [
            ('/test_repo/file1.txt', 10),
            ('/test_repo/subdir/file2.log', 50)
        ]

        dust_collector.archive_dust_files(dust_files, base_path, archive_dir_name, dry_run=True)

        mock_makedirs.assert_not_called()
        mock_move.assert_not_called()
        mock_print.assert_any_call(f"Dry run: Would create archive directory: {os.path.join(base_path, archive_dir_name)}")
        mock_print.assert_any_call("Dry run: Would move the following files to archive:")
        mock_print.assert_any_call("  - /test_repo/file1.txt")
        mock_print.assert_any_call("  - /test_repo/subdir/file2.log")

    @patch('os.remove')
    @patch('builtins.print')
    def test_delete_dust_files(self, mock_print, mock_remove):
        # Mock rationale: Prevent actual file deletion and capture stdout.
        dust_files = [('/path/to/dust1.txt', 10), ('/path/to/dust2.log', 50)]
        dust_collector.delete_dust_files(dust_files, dry_run=False)

        mock_remove.assert_any_call('/path/to/dust1.txt')
        mock_remove.assert_any_call('/path/to/dust2.log')
        self.assertEqual(mock_remove.call_count, 2)
        mock_print.assert_any_call("Deleted: /path/to/dust1.txt")
        mock_print.assert_any_call("Deleted: /path/to/dust2.log")

    @patch('os.remove')
    @patch('builtins.print')
    def test_delete_dust_files_dry_run(self, mock_print, mock_remove):
        # Mock rationale: Verify dry-run output without performing actual file deletion.
        dust_files = [('/path/to/dust1.txt', 10), ('/path/to/dust2.log', 50)]
        dust_collector.delete_dust_files(dust_files, dry_run=True)

        mock_remove.assert_not_called()
        mock_print.assert_any_call("Dry run: Would delete the following files:")
        mock_print.assert_any_call("  - /path/to/dust1.txt")
        mock_print.assert_any_call("  - /path/to/dust2.log")

    @patch('os.path.isdir', return_value=True)
    @patch('dust_collector.find_dust_files', return_value=[('/path/to/dust.txt', 10)])
    @patch('dust_collector.list_dust_files')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_list_mode(self, mock_print, mock_exit, mock_list_dust_files, mock_find_dust_files, mock_isdir):
        # Mock rationale: Simulate CLI arguments, file system checks, and function calls without actual execution.
        test_args = ['script_name', '/test_path', '--mode', 'list']
        with patch('sys.argv', test_args):
            dust_collector.main()
            mock_find_dust_files.assert_called_once_with('/test_path', 1024, False)
            mock_list_dust_files.assert_called_once_with([('/path/to/dust.txt', 10)])
            mock_exit.assert_called_once_with(0)

    @patch('os.path.isdir', return_value=True)
    @patch('dust_collector.find_dust_files', return_value=[('/path/to/dust.txt', 10)])
    @patch('dust_collector.archive_dust_files')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_archive_mode(self, mock_print, mock_exit, mock_archive_dust_files, mock_find_dust_files, mock_isdir):
        # Mock rationale: Simulate CLI arguments, file system checks, and function calls without actual execution.
        test_args = ['script_name', '/test_path', '--mode', 'archive']
        with patch('sys.argv', test_args):
            dust_collector.main()
            mock_find_dust_files.assert_called_once_with('/test_path', 1024, False)
            mock_archive_dust_files.assert_called_once_with([('/path/to/dust.txt', 10)], '/test_path', '.dust_archive', False)
            mock_exit.assert_called_once_with(0)

    @patch('os.path.isdir', return_value=True)
    @patch('dust_collector.find_dust_files', return_value=[])
    @patch('dust_collector.list_dust_files')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_no_dust_exit_code(self, mock_print, mock_exit, mock_list_dust_files, mock_find_dust_files, mock_isdir):
        # Mock rationale: Verify the correct exit code (2 for no-op) when no dust is found for archive/delete modes.
        test_args = ['script_name', '/test_path', '--mode', 'archive']
        with patch('sys.argv', test_args):
            dust_collector.main()
            mock_find_dust_files.assert_called_once_with('/test_path', 1024, False)
            mock_exit.assert_called_once_with(2) # No-op exit code

    @patch('os.path.isdir', return_value=False)
    @patch('sys.exit')
    @patch('sys.stderr', new_callable=StringIO)
    @patch('builtins.print')
    def test_main_invalid_path(self, mock_print, mock_stderr, mock_exit, mock_isdir):
        # Mock rationale: Simulate an invalid path argument and verify error output and exit code.
        test_args = ['script_name', '/invalid_path']
        with patch('sys.argv', test_args):
            dust_collector.main()
            mock_isdir.assert_called_once_with('/invalid_path')
            self.assertIn("Error: Path '/invalid_path' is not a valid directory.", mock_stderr.getvalue())
            mock_exit.assert_called_once_with(1)

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.print')
    def test_find_dust_files_os_error_handling(self, mock_print, mock_isfile, mock_getsize, mock_walk):
        # Mock rationale: Simulate an OSError during file access to ensure robust error handling.
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log'])
        ]
        # Simulate an OSError for file1.txt
        mock_getsize.side_effect = lambda x: 10 if x == '/test_dir/file2.log' else OSError("Permission denied")

        dust_files = dust_collector.find_dust_files('/test_dir', max_size=100, empty_only=False)
        self.assertEqual(len(dust_files), 1)
        self.assertIn(('/test_dir/file2.log', 10), dust_files)
        mock_print.assert_any_call(unittest.mock.ANY, file=sys.stderr) # Check if warning was printed to stderr
        self.assertIn("Warning: Could not access file /test_dir/file1.txt: Permission denied", mock_print.call_args_list[0].args[0])

if __name__ == '__main__':
    unittest.main()
