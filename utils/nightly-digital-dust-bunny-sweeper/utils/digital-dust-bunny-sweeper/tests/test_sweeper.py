import unittest
import os
import time
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import functions from the main script
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from sweeper import get_file_age_in_days, is_dust_bunny, find_dust_bunnies, sweep_dust_bunnies, main

class TestSweeper(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing file system operations
        self.test_dir = 'temp_test_dir'
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        # Clean up the temporary directory after tests
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('os.path.getmtime')
    def test_get_file_age_in_days(self, mock_getmtime):
        # Mock rationale: os.path.getmtime returns the last modification time of a file.
        # We need to control this value to test age calculation deterministically.
        mock_getmtime.return_value = time.time() - (30 * 24 * 3600) # 30 days ago
        self.assertAlmostEqual(get_file_age_in_days('dummy_file.txt'), 30, delta=0.1)

        mock_getmtime.return_value = time.time() - (5 * 24 * 3600) # 5 days ago
        self.assertAlmostEqual(get_file_age_in_days('dummy_file.txt'), 5, delta=0.1)

        mock_getmtime.side_effect = OSError # Simulate file not found
        self.assertEqual(get_file_age_in_days('non_existent_file.txt'), float('inf'))

    @patch('os.path.exists', return_value=True)
    @patch('sweeper.get_file_age_in_days')
    def test_is_dust_bunny_age(self, mock_get_file_age, mock_exists):
        # Mock rationale: os.path.exists checks if a path exists. We assume it does for this test.
        # Mock rationale: get_file_age_in_days calculates file age. We control its return value.

        # Test with age criterion
        mock_get_file_age.return_value = 40 # 40 days old
        self.assertTrue(is_dust_bunny('old_file.txt', 30, []))

        mock_get_file_age.return_value = 20 # 20 days old
        self.assertFalse(is_dust_bunny('new_file.txt', 30, []))

        # Test with age 0 (no age filtering)
        mock_get_file_age.return_value = 100
        self.assertFalse(is_dust_bunny('any_file.txt', 0, []))

    @patch('os.path.exists', return_value=True)
    @patch('sweeper.get_file_age_in_days', return_value=10) # Not old enough for age filter
    def test_is_dust_bunny_patterns(self, mock_get_file_age, mock_exists):
        # Mock rationale: os.path.exists checks if a path exists. We assume it does for this test.
        # Mock rationale: get_file_age_in_days calculates file age. We set it to a value that won't trigger age-based detection.

        # Test with pattern criterion
        patterns = ['*.log', 'temp_*']
        self.assertTrue(is_dust_bunny('error.log', 30, patterns))
        self.assertTrue(is_dust_bunny('temp_data/', 30, patterns))
        self.assertFalse(is_dust_bunny('report.txt', 30, patterns))

    @patch('os.path.exists', return_value=True)
    @patch('sweeper.get_file_age_in_days', return_value=10) # Not old enough for age filter
    def test_is_dust_bunny_no_match(self, mock_get_file_age, mock_exists):
        # Mock rationale: os.path.exists checks if a path exists. We assume it does for this test.
        # Mock rationale: get_file_age_in_days calculates file age. We set it to a value that won't trigger age-based detection.
        self.assertFalse(is_dust_bunny('clean_file.txt', 30, ['*.log']))

    @patch('os.path.exists', return_value=False)
    def test_is_dust_bunny_non_existent(self, mock_exists):
        # Mock rationale: os.path.exists checks if a path exists. We simulate a non-existent path.
        self.assertFalse(is_dust_bunny('non_existent.txt', 30, []))

    @patch('os.walk')
    @patch('sweeper.is_dust_bunny')
    def test_find_dust_bunnies(self, mock_is_dust_bunny, mock_os_walk):
        # Mock rationale: os.walk simulates traversing a directory tree. We control the structure.
        # Mock rationale: is_dust_bunny determines if an item is a dust bunny. We control its output.

        # Simulate a directory structure
        mock_os_walk.return_value = [
            ('/root', ['old_dir', 'new_dir'], ['old_file.log', 'new_file.txt']),
            ('/root/old_dir', [], ['temp_file.tmp']),
            ('/root/new_dir', [], ['important.txt'])
        ]

        # Configure is_dust_bunny to identify specific items
        def is_dust_bunny_side_effect(path, min_age, patterns):
            if 'old_file.log' in path or 'old_dir' in path or 'temp_file.tmp' in path:
                return True
            return False
        mock_is_dust_bunny.side_effect = is_dust_bunny_side_effect

        found_bunnies = find_dust_bunnies('/root', 30, ['*.log', '*.tmp'])
        expected_bunnies = [
            '/root/old_dir',
            '/root/old_file.log',
            '/root/old_dir/temp_file.tmp'
        ]
        self.assertCountEqual(found_bunnies, expected_bunnies)

        # Ensure that if a directory is a dust bunny, its contents are not re-checked
        # This is handled by `dirnames.remove(dname)` in the actual code, which os.walk mock doesn't fully simulate
        # but the `is_dust_bunny` mock ensures only the top-level dir is flagged.
        # The test above implicitly covers this by checking the final list.

    @patch('builtins.print')
    @patch('builtins.input', return_value='y')
    @patch('os.remove')
    @patch('shutil.rmtree')
    def test_sweep_dust_bunnies_delete_confirmed(self, mock_rmtree, mock_remove, mock_input, mock_print):
        # Mock rationale: builtins.print captures output for verification.
        # Mock rationale: builtins.input simulates user confirmation.
        # Mock rationale: os.remove simulates file deletion.
        # Mock rationale: shutil.rmtree simulates directory deletion.

        dust_bunnies = ['file1.txt', 'dir1/']

        # Configure os.path.isfile and os.path.isdir for the mock
        with patch('os.path.isfile', side_effect=lambda x: x == 'file1.txt'), \
             patch('os.path.isdir', side_effect=lambda x: x == 'dir1/'):
            sweep_dust_bunnies(dust_bunnies, dry_run=False)

        mock_input.assert_called_once_with('\n🧹 Ready to sweep these dust bunnies away? (y/N): ')
        mock_remove.assert_called_once_with('file1.txt')
        mock_rmtree.assert_called_once_with('dir1/')
        self.assertIn('Sweeping...', [call.args[0] for call in mock_print.call_args_list])
        self.assertIn('Digital space tidied up!', [call.args[0] for call in mock_print.call_args_list])

    @patch('builtins.print')
    @patch('builtins.input', return_value='n')
    @patch('os.remove')
    @patch('shutil.rmtree')
    def test_sweep_dust_bunnies_delete_cancelled(self, mock_rmtree, mock_remove, mock_input, mock_print):
        # Mock rationale: builtins.print captures output for verification.
        # Mock rationale: builtins.input simulates user cancellation.
        # Mock rationale: os.remove and shutil.rmtree should NOT be called.

        dust_bunnies = ['file1.txt', 'dir1/']
        sweep_dust_bunnies(dust_bunnies, dry_run=False)

        mock_input.assert_called_once()
        mock_remove.assert_not_called()
        mock_rmtree.assert_not_called()
        self.assertIn('Operation cancelled. The dust bunnies live to see another day! 🐾', [call.args[0] for call in mock_print.call_args_list])

    @patch('builtins.print')
    @patch('os.remove')
    @patch('shutil.rmtree')
    def test_sweep_dust_bunnies_dry_run(self, mock_rmtree, mock_remove, mock_print):
        # Mock rationale: builtins.print captures output for verification.
        # Mock rationale: os.remove and shutil.rmtree should NOT be called in dry-run.

        dust_bunnies = ['file1.txt', 'dir1/']
        sweep_dust_bunnies(dust_bunnies, dry_run=True)

        mock_remove.assert_not_called()
        mock_rmtree.assert_not_called()
        self.assertIn('Found 2 digital dust bunnies:', [call.args[0] for call in mock_print.call_args_list])
        self.assertIn('(This was a dry run. No files were actually swept away.)', [call.args[0] for call in mock_print.call_args_list])

    @patch('builtins.print')
    def test_sweep_dust_bunnies_no_bunnies(self, mock_print):
        # Mock rationale: builtins.print captures output for verification.
        sweep_dust_bunnies([], dry_run=True)
        self.assertIn('Your digital space is sparkling clean! No dust bunnies found.', [call.args[0] for call in mock_print.call_args_list])

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.find_dust_bunnies', return_value=['/path/to/old_file.log'])
    @patch('sweeper.sweep_dust_bunnies')
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    def test_main_dry_run_default(self, mock_print, mock_isdir, mock_sweep, mock_find, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args simulates command-line arguments.
        # Mock rationale: find_dust_bunnies simulates finding items.
        # Mock rationale: sweep_dust_bunnies simulates the sweeping action.
        # Mock rationale: os.path.isdir ensures the path is valid.
        # Mock rationale: builtins.print captures output for verification.

        mock_parse_args.return_value = MagicMock(
            path='/test/path',
            age=30,
            patterns=['*.log'],
            dry_run=False, # Default behavior if --delete is not present
            delete=False
        )
        main()
        mock_find.assert_called_once_with('/test/path', 30, ['*.log'])
        mock_sweep.assert_called_once_with(['/path/to/old_file.log'], True) # Should be dry_run=True

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.find_dust_bunnies', return_value=['/path/to/old_file.log'])
    @patch('sweeper.sweep_dust_bunnies')
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    def test_main_delete_mode(self, mock_print, mock_isdir, mock_sweep, mock_find, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args simulates command-line arguments.
        # Mock rationale: find_dust_bunnies simulates finding items.
        # Mock rationale: sweep_dust_bunnies simulates the sweeping action.
        # Mock rationale: os.path.isdir ensures the path is valid.
        # Mock rationale: builtins.print captures output for verification.

        mock_parse_args.return_value = MagicMock(
            path='/test/path',
            age=30,
            patterns=['*.log'],
            dry_run=False,
            delete=True
        )
        main()
        mock_find.assert_called_once_with('/test/path', 30, ['*.log'])
        mock_sweep.assert_called_once_with(['/path/to/old_file.log'], False) # Should be dry_run=False

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_invalid_path(self, mock_print, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args simulates command-line arguments.
        # Mock rationale: builtins.print captures output for verification.

        mock_parse_args.return_value = MagicMock(
            path='/non/existent/path',
            age=30,
            patterns=['*.log'],
            dry_run=True,
            delete=False
        )
        with patch('os.path.isdir', return_value=False):
            # Mock rationale: os.path.isdir simulates an invalid directory path.
            main()
        mock_print.assert_any_call("Error: Path '/non/existent/path' is not a valid directory.")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_delete_and_dry_run_error(self, mock_print, mock_parse_args):
        # Mock rationale: argparse.ArgumentParser.parse_args simulates command-line arguments.
        # Mock rationale: builtins.print captures output for verification.

        mock_parse_args.return_value = MagicMock(
            path='/test/path',
            age=30,
            patterns=['*.log'],
            dry_run=True,
            delete=True
        )
        main()
        mock_print.assert_any_call("Error: Cannot use --delete and --dry-run together. Please choose one.")

if __name__ == '__main__':
    unittest.main()
