import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
import sys
from io import StringIO

# Adjust path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from duster import find_irradiated_data, decontaminate_data, format_size, main
sys.path.pop(0)

class TestDuster(unittest.TestCase):

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    @patch('os.path.getsize')
    @patch('os.walk')
    def test_find_irradiated_data(self, mock_walk, mock_getsize, mock_isdir, mock_isfile, mock_exists):
        # Mock rationale: Simulate file system state without actual files.
        mock_exists.side_effect = lambda p: p in ['/tmp/old_log.txt', '/tmp/cache_dir', '/tmp/empty_dir', '/tmp/permission_denied_file']
        mock_isfile.side_effect = lambda p: p == '/tmp/old_log.txt' or p == '/tmp/permission_denied_file'
        mock_isdir.side_effect = lambda p: p in ['/tmp/cache_dir', '/tmp/empty_dir']

        # Mock rationale: Simulate file sizes.
        mock_getsize.side_effect = lambda p: {
            '/tmp/old_log.txt': 1024,
            '/tmp/cache_dir/file1.tmp': 500,
            '/tmp/cache_dir/file2.tmp': 200,
            '/tmp/cache_dir/subdir/subfile.log': 200,
            '/tmp/permission_denied_file': 300
        }.get(p, 0)

        # Mock rationale: Simulate directory contents for os.walk.
        mock_walk.side_effect = [
            [ # For /tmp/cache_dir
                ('/tmp/cache_dir', [], ['file1.tmp', 'file2.tmp']),
                ('/tmp/cache_dir/subdir', [], ['subfile.log'])
            ],
            [] # For /tmp/empty_dir
        ]

        # Test case 1: Single file
        result = find_irradiated_data(['/tmp/old_log.txt'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ('/tmp/old_log.txt', 1024))

        # Test case 2: Directory with files
        result = find_irradiated_data(['/tmp/cache_dir'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ('/tmp/cache_dir', 900)) # 500 + 200 + 200

        # Test case 3: Non-existent path
        result = find_irradiated_data(['/tmp/non_existent.txt'])
        self.assertEqual(len(result), 0)

        # Test case 4: Empty directory
        result = find_irradiated_data(['/tmp/empty_dir'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ('/tmp/empty_dir', 0))

        # Test case 5: File with permission error (getsize raises OSError)
        mock_getsize.side_effect = lambda p: {
            '/tmp/permission_denied_file': 300
        }.get(p, os.error('Permission denied')) if p == '/tmp/permission_denied_file' else 0
        result = find_irradiated_data(['/tmp/permission_denied_file'])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ('/tmp/permission_denied_file', 0)) # Size should be 0 if error occurs

    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('builtins.print')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    def test_decontaminate_data(self, mock_isdir, mock_isfile, mock_print, mock_rmtree, mock_remove):
        # Mock rationale: Prevent actual file system modifications during tests.
        mock_isfile.side_effect = lambda p: p == '/tmp/file_to_delete.txt'
        mock_isdir.side_effect = lambda p: p == '/tmp/dir_to_delete'

        # Test dry run
        removed = decontaminate_data(['/tmp/file_to_delete.txt', '/tmp/dir_to_delete'], dry_run=True)
        self.assertEqual(len(removed), 2)
        mock_remove.assert_not_called()
        mock_rmtree.assert_not_called()
        mock_print.assert_any_call("[DRY RUN] Would decontaminate: /tmp/file_to_delete.txt")
        mock_print.assert_any_call("[DRY RUN] Would decontaminate: /tmp/dir_to_delete")

        # Test actual cleanse
        mock_remove.reset_mock()
        mock_rmtree.reset_mock()
        mock_print.reset_mock()
        removed = decontaminate_data(['/tmp/file_to_delete.txt', '/tmp/dir_to_delete'], dry_run=False)
        self.assertEqual(len(removed), 2)
        mock_remove.assert_called_once_with('/tmp/file_to_delete.txt')
        mock_rmtree.assert_called_once_with('/tmp/dir_to_delete')
        mock_print.assert_not_called() # No dry run prints

        # Test error handling for file removal
        mock_remove.reset_mock()
        mock_rmtree.reset_mock()
        mock_print.reset_mock()
        mock_remove.side_effect = OSError("Permission denied")
        removed = decontaminate_data(['/tmp/file_to_delete.txt'], dry_run=False)
        self.assertEqual(len(removed), 0)
        mock_print.assert_called_once_with("Error decontaminating /tmp/file_to_delete.txt: Permission denied")

        # Test error handling for directory removal
        mock_remove.reset_mock()
        mock_rmtree.reset_mock()
        mock_print.reset_mock()
        mock_remove.side_effect = None # Reset file error
        mock_rmtree.side_effect = OSError("Directory not empty")
        removed = decontaminate_data(['/tmp/dir_to_delete'], dry_run=False)
        self.assertEqual(len(removed), 0)
        mock_print.assert_called_once_with("Error decontaminating /tmp/dir_to_delete: Directory not empty")

        # Test neither file nor directory
        mock_remove.reset_mock()
        mock_rmtree.reset_mock()
        mock_print.reset_mock()
        mock_isfile.side_effect = lambda p: False
        mock_isdir.side_effect = lambda p: False
        removed = decontaminate_data(['/tmp/unknown_path'], dry_run=False)
        self.assertEqual(len(removed), 0)
        mock_print.assert_called_once_with("Warning: /tmp/unknown_path is neither a file nor a directory. Skipping.")

    def test_format_size(self):
        self.assertEqual(format_size(0), "0.00 B")
        self.assertEqual(format_size(500), "500.00 B")
        self.assertEqual(format_size(1023), "1023.00 B")
        self.assertEqual(format_size(1024), "1.00 KB")
        self.assertEqual(format_size(1024 * 1024), "1.00 MB")
        self.assertEqual(format_size(1.5 * 1024 * 1024), "1.50 MB")
        self.assertEqual(format_size(1.5 * 1024 * 1024 * 1024), "1.50 GB")
        self.assertEqual(format_size(1.5 * (1024**4)), "1.50 TB")
        self.assertEqual(format_size(1.5 * (1024**5)), "1.50 PB")

    @patch('src.duster.find_irradiated_data')
    @patch('src.duster.decontaminate_data')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_dry_run(self, mock_exit, mock_parse_args, mock_print, mock_decontaminate_data, mock_find_irradiated_data):
        # Mock rationale: Control CLI arguments and internal function calls for main execution.
        mock_parse_args.return_value = MagicMock(paths=['/tmp/test_path'], cleanse=False)
        mock_find_irradiated_data.return_value = [('/tmp/test_path', 1024)]
        mock_decontaminate_data.return_value = ['/tmp/test_path']

        main()

        mock_find_irradiated_data.assert_called_once_with(['/tmp/test_path'])
        mock_print.assert_any_call("Detected 1 irradiated data clusters, totaling 1.00 KB:")
        mock_print.assert_any_call("  - /tmp/test_path (1.00 KB)")
        mock_print.assert_any_call("\nDry run complete. To perform actual decontamination, run with --cleanse.")
        mock_decontaminate_data.assert_called_once_with(['/tmp/test_path'], dry_run=True)
        mock_exit.assert_not_called()

    @patch('src.duster.find_irradiated_data')
    @patch('src.duster.decontaminate_data')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_cleanse(self, mock_exit, mock_parse_args, mock_print, mock_decontaminate_data, mock_find_irradiated_data):
        # Mock rationale: Control CLI arguments and internal function calls for main execution.
        mock_parse_args.return_value = MagicMock(paths=['/tmp/test_path'], cleanse=True)
        mock_find_irradiated_data.return_value = [('/tmp/test_path', 2048)]
        mock_decontaminate_data.return_value = ['/tmp/test_path']

        main()

        mock_find_irradiated_data.assert_called_once_with(['/tmp/test_path'])
        mock_print.assert_any_call("Initiating decontamination sequence...")
        mock_print.assert_any_call("Decontamination complete. 1 clusters purged, reclaiming 2.00 KB of digital wasteland.")
        mock_decontaminate_data.assert_called_once_with(['/tmp/test_path'], dry_run=False)
        mock_exit.assert_not_called()

    @patch('src.duster.find_irradiated_data')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_no_data_found(self, mock_exit, mock_parse_args, mock_print, mock_find_irradiated_data):
        # Mock rationale: Control CLI arguments and internal function calls for main execution.
        mock_parse_args.return_value = MagicMock(paths=['/tmp/test_path'], cleanse=False)
        mock_find_irradiated_data.return_value = []

        main()

        mock_find_irradiated_data.assert_called_once_with(['/tmp/test_path'])
        mock_print.assert_any_call("No irradiated data detected. Your system is pristine... for now.")
        mock_exit.assert_not_called()

    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_no_paths_provided(self, mock_exit, mock_parse_args, mock_print):
        # Mock rationale: Test the case where no paths are given to the CLI.
        mock_parse_args.return_value = MagicMock(paths=[], cleanse=False)
        mock_exit.side_effect = SystemExit # Prevent actual exit during test

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_any_call("Error: Please provide at least one path to scan. Use `python src/duster.py --help` for usage.")
