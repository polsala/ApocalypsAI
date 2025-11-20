import unittest
import os
import sys
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from pathlib import Path

# Add the src directory to the path for importing sweeper.py
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
import sweeper

class TestSweeper(unittest.TestCase):

    # Mock rationale: time.time() is non-deterministic. Fixing it allows consistent age calculations.
    @patch('time.time', return_value=datetime(2023, 10, 26, 12, 0, 0).timestamp())
    def test_get_file_age_days(self, mock_time):
        mock_path = MagicMock(spec=Path)
        
        # Test with st_birthtime
        mock_stat_birth = MagicMock()
        mock_stat_birth.st_birthtime = (datetime(2023, 10, 25, 12, 0, 0) - timedelta(days=5)).timestamp() # 5 days old
        mock_stat_birth.st_mtime = (datetime(2023, 10, 25, 12, 0, 0) - timedelta(days=10)).timestamp() # 10 days old
        mock_path.stat.return_value = mock_stat_birth
        self.assertAlmostEqual(sweeper.get_file_age_days(mock_path), 5.0, places=2)

        # Test with st_mtime (no st_birthtime)
        mock_stat_mtime = MagicMock()
        del mock_stat_mtime.st_birthtime # Simulate no birthtime
        mock_stat_mtime.st_mtime = (datetime(2023, 10, 25, 12, 0, 0) - timedelta(days=7)).timestamp() # 7 days old
        mock_path.stat.return_value = mock_stat_mtime
        self.assertAlmostEqual(sweeper.get_file_age_days(mock_path), 7.0, places=2)

        # Test file not found
        mock_path.stat.side_effect = FileNotFoundError
        self.assertEqual(sweeper.get_file_age_days(mock_path), -1)

        # Test OSError
        mock_path.stat.side_effect = OSError
        self.assertEqual(sweeper.get_file_age_days(mock_path), -1)

    # Mock rationale: Path.is_dir and Path.glob are file system operations.
    # Mocking them allows simulating directory existence and contents without actual file system interaction.
    @patch('pathlib.Path.is_dir', return_value=True)
    @patch('pathlib.Path.glob')
    # Mock rationale: time.time() is non-deterministic. Fixing it allows consistent age calculations.
    @patch('time.time', return_value=datetime(2023, 10, 26, 12, 0, 0).timestamp())
    @patch('sweeper.get_file_age_days') # Mock rationale: Isolate find_dust_bunnies from get_file_age_days's internal logic.
    def test_find_dust_bunnies(self, mock_get_age, mock_time, mock_glob, mock_is_dir):
        mock_dir = Path("/mock/dir")
        patterns = ["*.tmp", "*.log.old"]
        age_days = 10

        # Simulate files
        file1 = MagicMock(spec=Path, name="file1.tmp")
        file1.is_file.return_value = True
        file2 = MagicMock(spec=Path, name="old.log.old")
        file2.is_file.return_value = True
        file3 = MagicMock(spec=Path, name="recent.tmp")
        file3.is_file.return_value = True
        file4 = MagicMock(spec=Path, name="not_matching.txt")
        file4.is_file.return_value = True
        subdir_file = MagicMock(spec=Path, name="subdir/another.tmp")
        subdir_file.is_file.return_value = True
        
        # Mock glob to return files for each pattern
        mock_glob.side_effect = [
            [file1, file3, subdir_file], # For "*.tmp"
            [file2]                      # For "*.log.old"
        ]

        # Mock get_file_age_days for each file
        mock_get_age.side_effect = {
            file1: 15,  # Older than 10 days
            file2: 20,  # Older than 10 days
            file3: 5,   # Not older than 10 days
            subdir_file: 12 # Older than 10 days
        }.get

        found_files = sweeper.find_dust_bunnies(mock_dir, patterns, age_days)
        
        # Ensure glob was called for each pattern
        mock_glob.assert_any_call("**/*.tmp")
        mock_glob.assert_any_call("**/*.log.old")
        
        # Only file1, file2, and subdir_file should be found
        self.assertIn(file1, found_files)
        self.assertIn(file2, found_files)
        self.assertIn(subdir_file, found_files)
        self.assertNotIn(file3, found_files)
        self.assertNotIn(file4, found_files)
        self.assertEqual(len(found_files), 3)

        # Test directory not found
        mock_is_dir.return_value = False
        with patch('sys.stderr', new_callable=MagicMock) as mock_stderr:
            found_files_no_dir = sweeper.find_dust_bunnies(mock_dir, patterns, age_days)
            self.assertEqual(found_files_no_dir, [])
            mock_stderr.write.assert_called_with(f"Error: Directory '{mock_dir}' not found or is not a directory.\n")

    # Mock rationale: os.remove is a file system operation. Mocking it prevents actual deletion.
    # input() is interactive. Mocking it allows providing predefined responses.
    # print() is for output. Mocking it allows capturing and asserting printed messages.
    @patch('os.remove')
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('sweeper.get_file_age_days', return_value=15) # Mock rationale: get_file_age_days is called for printing age.
    def test_sweep_dust_bunnies(self, mock_get_age, mock_print, mock_input, mock_remove):
        file1 = MagicMock(spec=Path, name="file1.tmp")
        file2 = MagicMock(spec=Path, name="file2.log.old")
        files_to_delete = [file1, file2]

        # Test dry run
        mock_print.reset_mock()
        sweeper.sweep_dust_bunnies(files_to_delete, dry_run=True, force=False)
        mock_print.assert_any_call("\nThis was a DRY RUN. No files were actually deleted.")
        mock_remove.assert_not_called()

        # Test deletion with confirmation (yes)
        mock_print.reset_mock()
        mock_input.return_value = 'y'
        sweeper.sweep_dust_bunnies(files_to_delete, dry_run=False, force=False)
        mock_input.assert_called_once_with("\nProceed with deletion? (y/N): ")
        mock_remove.assert_any_call(file1)
        mock_remove.assert_any_call(file2)
        mock_print.assert_any_call(f"  ✅ Deleted: {file1}")
        mock_print.assert_any_call(f"  ✅ Deleted: {file2}")
        mock_print.assert_any_call("\nSweeping complete. 2 files deleted.")
        mock_input.reset_mock() # Reset for next test

        # Test deletion with confirmation (no)
        mock_print.reset_mock()
        mock_remove.reset_mock()
        mock_input.return_value = 'n'
        sweeper.sweep_dust_bunnies(files_to_delete, dry_run=False, force=False)
        mock_input.assert_called_once_with("\nProceed with deletion? (y/N): ")
        mock_remove.assert_not_called()
        mock_print.assert_any_call("Deletion cancelled.")
        mock_input.reset_mock()

        # Test forced deletion
        mock_print.reset_mock()
        mock_remove.reset_mock()
        sweeper.sweep_dust_bunnies(files_to_delete, dry_run=False, force=True)
        mock_input.assert_not_called() # input should be skipped
        mock_remove.assert_any_call(file1)
        mock_remove.assert_any_call(file2)
        mock_print.assert_any_call("\nSweeping complete. 2 files deleted.")

        # Test deletion with OSError
        mock_print.reset_mock()
        mock_remove.reset_mock()
        mock_remove.side_effect = [None, OSError("Permission denied")] # First file deletes, second fails
        sweeper.sweep_dust_bunnies(files_to_delete, dry_run=False, force=True)
        mock_print.assert_any_call(f"  ✅ Deleted: {file1}")
        mock_print.assert_any_call(f"  ❌ Failed to delete {file2}: Permission denied")
        mock_print.assert_any_call("\nSweeping complete. 1 files deleted.")

        # Test no files to delete
        mock_print.reset_mock()
        sweeper.sweep_dust_bunnies([], dry_run=False, force=True)
        mock_print.assert_any_call("No digital dust bunnies found to sweep. Your system is sparkling clean!")
        mock_remove.assert_not_called()

    # Mock rationale: sys.exit is a program termination. Mocking it prevents actual exit during tests.
    # argparse.ArgumentParser.parse_args() is CLI interaction. Mocking it allows providing arguments programmatically.
    # print() and sys.stderr are for output. Mocking them allows capturing and asserting messages.
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sweeper.find_dust_bunnies', return_value=[Path("/mock/file.tmp")])
    @patch('sweeper.sweep_dust_bunnies')
    @patch('sys.exit')
    @patch('builtins.print')
    @patch('sys.stderr', new_callable=MagicMock)
    def test_main(self, mock_stderr, mock_print, mock_sys_exit, mock_sweep, mock_find, mock_parse_args):
        # Test successful run
        mock_parse_args.return_value = MagicMock(
            directory=".",
            pattern=["*.tmp"],
            age_days=30,
            dry_run=False,
            force=False
        )
        sweeper.main()
        mock_find.assert_called_once()
        mock_sweep.assert_called_once()
        mock_sys_exit.assert_not_called()
        mock_find.reset_mock()
        mock_sweep.reset_mock()

        # Test no pattern specified
        mock_parse_args.return_value = MagicMock(
            directory=".",
            pattern=[], # No pattern
            age_days=30,
            dry_run=False,
            force=False
        )
        sweeper.main()
        mock_print.assert_any_call("Error: At least one --pattern must be specified.", file=mock_stderr)
        mock_sys_exit.assert_called_once_with(1)
        mock_find.assert_not_called()
        mock_sweep.assert_not_called()

if __name__ == '__main__':
    unittest.main()
