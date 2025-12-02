import unittest
from unittest.mock import patch, mock_open, call
import os
import sys
import io
import shutil

# Import the function to be tested
from src.dust_collector import collect_dust, _is_dust, _perform_action

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        self.mock_stdout = io.StringIO()
        sys.stdout = self.mock_stdout

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('os.path.getsize')
    def test_is_dust(self, mock_getsize):
        # Mock rationale: os.path.getsize is a file system operation that needs to be controlled for deterministic tests.
        mock_getsize.return_value = 500 # bytes
        self.assertTrue(_is_dust('/path/to/small_file.txt', 1024))

        mock_getsize.return_value = 1024
        self.assertTrue(_is_dust('/path/to/exact_size_file.txt', 1024))

        mock_getsize.return_value = 1025
        self.assertFalse(_is_dust('/path/to/large_file.txt', 1024))

        mock_getsize.return_value = 0 # Empty file
        self.assertTrue(_is_dust('/path/to/empty_file.txt', 1024))

        # Test OSError handling (e.g., file disappeared)
        mock_getsize.side_effect = OSError
        self.assertFalse(_is_dust('/path/to/missing_file.txt', 1024))

    @patch('os.remove')
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    def test_perform_action_delete(self, mock_exists, mock_makedirs, mock_move, mock_remove):
        # Mock rationale: os.remove, shutil.move, os.makedirs, os.path.exists are file system operations.
        # We need to prevent actual file deletion/movement and control directory creation/existence for tests.
        _perform_action('/path/to/file.txt', 'delete')
        mock_remove.assert_called_once_with('/path/to/file.txt')
        self.assertIn('Deleting: /path/to/file.txt', self.mock_stdout.getvalue())
        mock_move.assert_not_called()
        mock_makedirs.assert_not_called()

    @patch('os.remove')
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('os.path.exists', side_effect=[False, True, False]) # First move is new, second move has collision, third is new
    def test_perform_action_archive(self, mock_exists, mock_makedirs, mock_move, mock_remove):
        # Mock rationale: os.remove, shutil.move, os.makedirs, os.path.exists are file system operations.
        # We need to prevent actual file deletion/movement and control directory creation/existence for tests.
        archive_dir = '/archive'
        filepath1 = '/path/to/file1.txt'
        filepath2 = '/path/to/file2.txt'

        # Test first archive (no collision)
        _perform_action(filepath1, 'archive', archive_dir)
        mock_makedirs.assert_called_once_with(archive_dir, exist_ok=True)
        mock_move.assert_called_once_with(filepath1, os.path.join(archive_dir, 'file1.txt'))
        self.assertIn(f'Archiving: {filepath1} -> {os.path.join(archive_dir, 'file1.txt')}', self.mock_stdout.getvalue())
        mock_remove.assert_not_called()
        mock_makedirs.reset_mock()
        mock_move.reset_mock()
        self.mock_stdout.truncate(0)
        self.mock_stdout.seek(0)

        # Test second archive (with collision, should rename)
        _perform_action(filepath2, 'archive', archive_dir)
        mock_makedirs.assert_called_once_with(archive_dir, exist_ok=True)
        mock_move.assert_called_once_with(filepath2, os.path.join(archive_dir, 'file2_1.txt'))
        self.assertIn(f'Archiving: {filepath2} -> {os.path.join(archive_dir, 'file2_1.txt')}', self.mock_stdout.getvalue())
        mock_remove.assert_not_called()

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.remove')
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    def test_collect_dust_list_dry_run(self, mock_exists, mock_makedirs, mock_move, mock_remove, mock_getsize, mock_walk):
        # Mock rationale: os.walk simulates directory structure, os.path.getsize controls file sizes.
        # os.remove, shutil.move, os.makedirs, os.path.exists are file system operations that should not occur in dry-run/list mode.
        mock_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.log']),
            ('/root/subdir', [], ['file3.tmp', 'large_file.txt'])
        ]
        # file1.txt: 500 bytes (dust)
        # file2.log: 100 bytes (dust)
        # file3.tmp: 2000 bytes (dust)
        # large_file.txt: 5000 bytes (not dust)
        mock_getsize.side_effect = {
            '/root/file1.txt': 500,
            '/root/file2.log': 100,
            '/root/subdir/file3.tmp': 2000,
            '/root/subdir/large_file.txt': 5000
        }.get

        # Test list action
        dust_count = collect_dust('.', max_size_kb=2.0, action='list', dry_run=False)
        self.assertEqual(dust_count, 3)
        output = self.mock_stdout.getvalue()
        self.assertIn('Found dust: /root/file1.txt (500 bytes)', output)
        self.assertIn('Found dust: /root/file2.log (100 bytes)', output)
        self.assertIn('Found dust: /root/subdir/file3.tmp (2000 bytes)', output)
        self.assertNotIn('large_file.txt', output)
        mock_remove.assert_not_called()
        mock_move.assert_not_called()

        self.mock_stdout.truncate(0)
        self.mock_stdout.seek(0)
        mock_remove.reset_mock()
        mock_move.reset_mock()

        # Test delete action with dry_run
        dust_count = collect_dust('.', max_size_kb=2.0, action='delete', dry_run=True)
        self.assertEqual(dust_count, 3)
        output = self.mock_stdout.getvalue()
        self.assertIn('Identified dust: /root/file1.txt (500 bytes)', output)
        self.assertIn('(Dry run: would delete /root/file1.txt)', output)
        self.assertIn('No changes were made due to --dry-run.', output)
        mock_remove.assert_not_called()
        mock_move.assert_not_called()

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.remove')
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    def test_collect_dust_delete_action(self, mock_exists, mock_makedirs, mock_move, mock_remove, mock_getsize, mock_walk):
        # Mock rationale: os.walk simulates directory structure, os.path.getsize controls file sizes.
        # os.remove is the target action to be mocked and asserted.
        mock_walk.return_value = [
            ('/root', [], ['dusty_file.txt', 'clean_file.txt'])
        ]
        mock_getsize.side_effect = {
            '/root/dusty_file.txt': 100,
            '/root/clean_file.txt': 2000
        }.get

        dust_count = collect_dust('.', max_size_kb=1.0, action='delete', dry_run=False)
        self.assertEqual(dust_count, 1)
        mock_remove.assert_called_once_with('/root/dusty_file.txt')
        self.assertIn('Deleting: /root/dusty_file.txt', self.mock_stdout.getvalue())
        mock_move.assert_not_called()

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.remove')
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    def test_collect_dust_archive_action(self, mock_exists, mock_makedirs, mock_move, mock_remove, mock_getsize, mock_walk):
        # Mock rationale: os.walk simulates directory structure, os.path.getsize controls file sizes.
        # shutil.move, os.makedirs are the target actions to be mocked and asserted.
        mock_walk.return_value = [
            ('/root', [], ['dusty_file.txt', 'clean_file.txt'])
        ]
        mock_getsize.side_effect = {
            '/root/dusty_file.txt': 100,
            '/root/clean_file.txt': 2000
        }.get
        archive_dir = '/my_archive'

        dust_count = collect_dust('.', max_size_kb=1.0, action='archive', dry_run=False, archive_dir=archive_dir)
        self.assertEqual(dust_count, 1)
        mock_makedirs.assert_called_once_with(archive_dir, exist_ok=True)
        mock_move.assert_called_once_with('/root/dusty_file.txt', os.path.join(archive_dir, 'dusty_file.txt'))
        self.assertIn(f'Archiving: /root/dusty_file.txt -> {os.path.join(archive_dir, 'dusty_file.txt')}', self.mock_stdout.getvalue())
        mock_remove.assert_not_called()

    @patch('os.walk')
    @patch('os.path.getsize')
    @patch('os.remove')
    @patch('shutil.move')
    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    def test_collect_dust_no_dust_found(self, mock_exists, mock_makedirs, mock_move, mock_remove, mock_getsize, mock_walk):
        # Mock rationale: os.walk simulates directory structure, os.path.getsize controls file sizes.
        # No file system changes should occur if no dust is found.
        mock_walk.return_value = [
            ('/root', [], ['large_file1.txt', 'large_file2.log'])
        ]
        mock_getsize.side_effect = {
            '/root/large_file1.txt': 5000,
            '/root/large_file2.log': 3000
        }.get

        dust_count = collect_dust('.', max_size_kb=1.0, action='list', dry_run=False)
        self.assertEqual(dust_count, 0)
        output = self.mock_stdout.getvalue()
        self.assertIn('Scan complete. Found 0 \'cosmic dust\' files.', output)
        self.assertNotIn('Found dust:', output)
        mock_remove.assert_not_called()
        mock_move.assert_not_called()

    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.dust_collector.collect_dust')
    def test_main_archive_no_dir_error(self, mock_collect_dust, mock_parse_args, mock_exit):
        # Mock rationale: sys.exit to prevent actual exit during test, argparse.ArgumentParser.parse_args to control CLI arguments,
        # collect_dust to ensure it's not called when an error occurs.
        mock_parse_args.return_value = type('obj', (object,), {
            'path': '.', 'max_size': 1.0, 'action': 'archive', 'dry_run': False, 'archive_dir': None
        })()
        
        from src.dust_collector import main
        main()
        mock_exit.assert_called_once_with(1)
        mock_collect_dust.assert_not_called()
        self.assertIn("Error: --archive-dir is required when --action is 'archive' and not in dry-run mode.", self.mock_stdout.getvalue())

    @patch('sys.exit')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.dust_collector.collect_dust')
    def test_main_archive_no_dir_dry_run_ok(self, mock_collect_dust, mock_parse_args, mock_exit):
        # Mock rationale: sys.exit to prevent actual exit during test, argparse.ArgumentParser.parse_args to control CLI arguments,
        # collect_dust to ensure it's called correctly.
        mock_parse_args.return_value = type('obj', (object,), {
            'path': '.', 'max_size': 1.0, 'action': 'archive', 'dry_run': True, 'archive_dir': None
        })()
        
        from src.dust_collector import main
        main()
        mock_exit.assert_not_called()
        mock_collect_dust.assert_called_once_with(
            path='.', max_size_kb=1.0, action='archive', dry_run=True, archive_dir=None
        )
