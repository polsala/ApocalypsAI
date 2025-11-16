import unittest
import os
import shutil
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Add the src directory to sys.path to allow direct import of sweeper.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from sweeper import find_dust_bunnies, sweep_dust_bunnies, main, DEFAULT_PATTERNS

class TestDustBunnySweeper(unittest.TestCase):

    @patch('os.walk')
    def test_find_dust_bunnies_basic(self, mock_os_walk):
        # Mock rationale: os.walk is a file system operation. Mocking it allows
        # us to simulate various directory structures and file types without
        # actually creating files on disk, ensuring deterministic and fast tests.
        mock_os_walk.return_value = [
            ('/root', ['dir1', '__pycache__', 'node_modules'], ['file.txt', 'test.pyc']),
            ('/root/dir1', [], ['another.log']),
            ('/root/__pycache__', [], ['cache.pyc']),
            ('/root/node_modules', ['package'], ['index.js']),
            ('/root/node_modules/package', [], ['dep.js']),
        ]

        files, dirs = find_dust_bunnies('/root', DEFAULT_PATTERNS)

        expected_files = [
            '/root/test.pyc',
            '/root/dir1/another.log',
        ]
        expected_dirs = [
            '/root/__pycache__',
            '/root/node_modules',
        ]

        self.assertCountEqual(files, expected_files)
        self.assertCountEqual(dirs, expected_dirs)

    @patch('os.walk')
    def test_find_dust_bunnies_custom_patterns(self, mock_os_walk):
        # Mock rationale: Same as above, simulating file system for custom patterns.
        mock_os_walk.return_value = [
            ('/project', ['build', 'src'], ['config.yaml', 'temp.tmp']),
            ('/project/build', [], ['output.exe']),
            ('/project/src', [], ['main.c']),
        ]
        custom_patterns = ['build', '*.tmp']

        files, dirs = find_dust_bunnies('/project', custom_patterns)

        expected_files = ['/project/temp.tmp']
        expected_dirs = ['/project/build']

        self.assertCountEqual(files, expected_files)
        self.assertCountEqual(dirs, expected_dirs)

    @patch('os.walk')
    def test_find_dust_bunnies_nested_deletion(self, mock_os_walk):
        # Mock rationale: Simulating a scenario where a file is inside a directory
        # that is itself marked for deletion. The utility should only mark the parent dir.
        mock_os_walk.return_value = [
            ('/repo', ['__pycache__'], ['main.py']),
            ('/repo/__pycache__', [], ['foo.pyc']),
        ]

        files, dirs = find_dust_bunnies('/repo', DEFAULT_PATTERNS)

        self.assertCountEqual(files, []) # foo.pyc should not be in files, as __pycache__ is deleted
        self.assertCountEqual(dirs, ['/repo/__pycache__'])

    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('builtins.print')
    def test_sweep_dust_bunnies_dry_run(self, mock_print, mock_rmtree, mock_os_remove):
        # Mock rationale: os.remove and shutil.rmtree perform actual file system
        # deletions. Mocking them prevents unintended data loss and allows us to
        # verify that the correct calls *would* have been made.
        # builtins.print is mocked to capture output for verification without
        # polluting test console.
        files = ['/tmp/file1.pyc', '/tmp/file2.log']
        dirs = ['/tmp/__pycache__', '/tmp/node_modules']

        sweep_dust_bunnies(files, dirs, dry_run=True)

        mock_os_remove.assert_not_called()
        mock_rmtree.assert_not_called()
        mock_print.assert_any_call("\n--- Dry Run: Would delete the following dust bunnies ---")
        # Check for specific prints, order of files/dirs might vary due to set/sort
        self.assertIn("  [FILE] /tmp/file1.pyc", [call.args[0] for call in mock_print.call_args_list])
        self.assertIn("  [DIR] /tmp/__pycache__", [call.args[0] for call in mock_print.call_args_list])
        self.assertIn("Dry run identified 4 dust bunnies.", [call.args[0] for call in mock_print.call_args_list])

    @patch('os.remove')
    @patch('shutil.rmtree')
    @patch('builtins.print')
    def test_sweep_dust_bunnies_actual_sweep(self, mock_print, mock_rmtree, mock_os_remove):
        # Mock rationale: Same as above, verifying actual deletion calls.
        files = ['/tmp/file1.pyc', '/tmp/file2.log']
        dirs = ['/tmp/__pycache__', '/tmp/node_modules']

        sweep_dust_bunnies(files, dirs, dry_run=False)

        self.assertEqual(mock_os_remove.call_count, len(files))
        mock_os_remove.assert_any_call('/tmp/file1.pyc')
        mock_os_remove.assert_any_call('/tmp/file2.log')

        self.assertEqual(mock_rmtree.call_count, len(dirs))
        mock_rmtree.assert_any_call('/tmp/__pycache__')
        mock_rmtree.assert_any_call('/tmp/node_modules')

        # Check for specific prints
        self.assertIn("\n--- Sweeping dust bunnies ---", [call.args[0] for call in mock_print.call_args_list])
        self.assertIn("  [DELETED FILE] /tmp/file1.pyc", [call.args[0] for call in mock_print.call_args_list])
        self.assertIn("  [DELETED DIR] /tmp/__pycache__", [call.args[0] for call in mock_print.call_args_list])
        self.assertIn("Successfully swept 4 dust bunnies.", [call.args[0] for call in mock_print.call_args_list])

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.abspath', side_effect=lambda x: f'/abs/{x}')
    @patch('sweeper.find_dust_bunnies', return_value=(['f1'], ['d1']))
    @patch('sweeper.sweep_dust_bunnies')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_dry_run_mode(self, mock_parse_args, mock_print, mock_sweep, mock_find, mock_abspath, mock_isdir):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to control
        # command-line arguments programmatically. os.path.isdir and os.path.abspath
        # are mocked to control path validation without actual file system checks.
        # find_dust_bunnies and sweep_dust_bunnies are mocked to isolate the main
        # function's logic and prevent side effects. builtins.print is mocked to
        # capture output.
        mock_parse_args.return_value = MagicMock(
            path='.', dry_run=True, patterns=DEFAULT_PATTERNS
        )
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            main()
            output = fake_stdout.getvalue()

        mock_find.assert_called_once_with('/abs/.', DEFAULT_PATTERNS)
        mock_sweep.assert_called_once_with(['f1'], ['d1'], True)
        self.assertIn("Dry run identified 2 dust bunnies.", output)
        self.assertIn("Dry run complete. To actually sweep, run without --dry-run.", output)

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.abspath', side_effect=lambda x: f'/abs/{x}')
    @patch('sweeper.find_dust_bunnies', return_value=([], []))
    @patch('sweeper.sweep_dust_bunnies')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_dust_bunnies(self, mock_parse_args, mock_print, mock_sweep, mock_find, mock_abspath, mock_isdir):
        # Mock rationale: Same as above, testing the scenario where no dust bunnies are found.
        mock_parse_args.return_value = MagicMock(
            path='.', dry_run=False, patterns=DEFAULT_PATTERNS
        )
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            with self.assertRaises(SystemExit) as cm: # main() calls exit(0)
                main()
            self.assertEqual(cm.exception.code, 0)
            output = fake_stdout.getvalue()

        mock_find.assert_called_once_with('/abs/.', DEFAULT_PATTERNS)
        mock_sweep.assert_not_called()
        self.assertIn("No dust bunnies found. Your workspace is sparkling clean!", output)

    @patch('os.path.isdir', return_value=False)
    @patch('os.path.abspath', side_effect=lambda x: f'/abs/{x}')
    @patch('builtins.print')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_invalid_path(self, mock_parse_args, mock_print, mock_abspath, mock_isdir):
        # Mock rationale: Testing error handling for an invalid path.
        mock_parse_args.return_value = MagicMock(
            path='/nonexistent', dry_run=False, patterns=DEFAULT_PATTERNS
        )
        
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            with self.assertRaises(SystemExit) as cm: # main() calls exit(1)
                main()
            self.assertEqual(cm.exception.code, 1)
            output = fake_stdout.getvalue()

        self.assertIn("Error: Path '/abs//nonexistent' is not a valid directory.", output)


if __name__ == '__main__':
    unittest.main()
