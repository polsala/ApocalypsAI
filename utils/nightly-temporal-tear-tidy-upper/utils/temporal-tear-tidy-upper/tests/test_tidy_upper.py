import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from pathlib import Path
import sys
import io

# Import the main script
# Mock rationale: This import needs to happen after patching sys.path if the script
# were not directly runnable, but since it's a standalone script, we can import it
# directly and then mock its internal functions.
from src import tidy_upper

class TestTemporalTearTidyUpper(unittest.TestCase):

    def setUp(self):
        # Capture stdout/stderr for testing print statements
        self.held_stdout = sys.stdout
        self.held_stderr = sys.stderr
        self.mock_stdout = io.StringIO()
        self.mock_stderr = io.StringIO()
        sys.stdout = self.mock_stdout
        sys.stderr = self.mock_stderr

    def tearDown(self):
        # Restore stdout/stderr
        sys.stdout = self.held_stdout
        sys.stderr = self.held_stderr

    @patch('src.tidy_upper.datetime')
    def test_get_file_age_days(self, mock_datetime):
        # Mock rationale: Control the current time and file modification time
        # to ensure deterministic age calculation without relying on actual system time.
        mock_datetime.now.return_value = datetime(2023, 10, 26)
        
        mock_file = MagicMock(spec=Path)
        mock_stat = MagicMock()
        
        # File modified 30 days ago
        mock_stat.st_mtime = datetime(2023, 9, 26).timestamp()
        mock_file.stat.return_value = mock_stat
        self.assertEqual(tidy_upper.get_file_age_days(mock_file), 30)

        # File modified 10 days ago
        mock_stat.st_mtime = datetime(2023, 10, 16).timestamp()
        mock_file.stat.return_value = mock_stat
        self.assertEqual(tidy_upper.get_file_age_days(mock_file), 10)

        # File not found
        mock_file.stat.side_effect = FileNotFoundError
        self.assertEqual(tidy_upper.get_file_age_days(mock_file), -1)

    @patch('src.tidy_upper.get_file_age_days')
    @patch('pathlib.Path.is_dir', return_value=True)
    @patch('pathlib.Path.iterdir')
    def test_scan_directory(self, mock_iterdir, mock_is_dir, mock_get_file_age_days):
        # Mock rationale: Simulate a directory structure and file ages without creating
        # actual files, ensuring the scan logic is tested deterministically and offline.
        
        mock_dir = Path("/mock/dir")
        
        # Simulate files:
        # file_old_1: 40 days old (should be picked up by age_threshold=30)
        # file_old_2: 35 days old (should be picked up)
        # file_new_1: 20 days old (should NOT be picked up)
        # sub_dir: a directory (should be skipped by default)
        
        mock_file_old_1 = MagicMock(spec=Path, name="file_old_1")
        mock_file_old_1.is_file.return_value = True
        mock_file_old_1.__str__.return_value = "/mock/dir/file_old_1.log"

        mock_file_old_2 = MagicMock(spec=Path, name="file_old_2")
        mock_file_old_2.is_file.return_value = True
        mock_file_old_2.__str__.return_value = "/mock/dir/file_old_2.tmp"

        mock_file_new_1 = MagicMock(spec=Path, name="file_new_1")
        mock_file_new_1.is_file.return_value = True
        mock_file_new_1.__str__.return_value = "/mock/dir/file_new_1.txt"

        mock_sub_dir = MagicMock(spec=Path, name="sub_dir")
        mock_sub_dir.is_file.return_value = False
        mock_sub_dir.is_dir.return_value = True
        mock_sub_dir.__str__.return_value = "/mock/dir/sub_dir"

        mock_iterdir.return_value = [
            mock_file_old_1,
            mock_file_old_2,
            mock_file_new_1,
            mock_sub_dir
        ]

        # Configure get_file_age_days mock
        def get_age_side_effect(filepath):
            if filepath.name == "file_old_1": return 40
            if filepath.name == "file_old_2": return 35
            if filepath.name == "file_new_1": return 20
            return 0 # Default for others

        mock_get_file_age_days.side_effect = get_age_side_effect

        # Test with age threshold 30
        old_files = tidy_upper.scan_directory(mock_dir, 30)
        self.assertEqual(len(old_files), 2)
        self.assertIn(mock_file_old_1, old_files)
        self.assertIn(mock_file_old_2, old_files)
        self.assertNotIn(mock_file_new_1, old_files)
        self.assertNotIn(mock_sub_dir, old_files)

        # Test with age threshold 50 (should find nothing)
        old_files_none = tidy_upper.scan_directory(mock_dir, 50)
        self.assertEqual(len(old_files_none), 0)

        # Test with invalid directory
        mock_is_dir.return_value = False
        old_files_invalid = tidy_upper.scan_directory(Path("/invalid/dir"), 30)
        self.assertEqual(len(old_files_invalid), 0)
        self.assertIn("Warning: Rift detected at '/invalid/dir' - not a valid directory. Skipping.", self.mock_stderr.getvalue())

    @patch('src.tidy_upper.scan_directory')
    @patch('src.tidy_upper.get_file_age_days', return_value=35) # For printing age
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.input', return_value='y') # Mock user confirmation
    @patch('pathlib.Path.unlink') # Mock file deletion
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during tests
    def test_main_dry_run(self, mock_sys_exit, mock_unlink, mock_input, mock_parse_args, mock_scan_directory, mock_get_file_age_days_for_print):
        # Mock rationale: Simulate command-line arguments, directory scanning results,
        # and prevent actual file operations or program exit during a dry run test.
        
        # Configure mock arguments for dry run
        mock_parse_args.return_value = MagicMock(
            dirs=["/mock/dir1", "/mock/dir2"],
            age=30,
            dry_run=True,
            confirm=False
        )

        # Simulate files found by scan_directory
        mock_file1 = MagicMock(spec=Path, name="file1")
        mock_file1.__str__.return_value = "/mock/dir1/old_file1.log"
        mock_file2 = MagicMock(spec=Path, name="file2")
        mock_file2.__str__.return_value = "/mock/dir2/old_file2.tmp"
        
        mock_scan_directory.side_effect = [[mock_file1], [mock_file2]]

        tidy_upper.main()

        # Assertions for dry run
        self.assertIn("Identified 2 temporal tears", self.mock_stdout.getvalue())
        self.assertIn("/mock/dir1/old_file1.log", self.mock_stdout.getvalue())
        self.assertIn("/mock/dir2/old_file2.tmp", self.mock_stdout.getvalue())
        self.assertIn("This was a dry run. No files were actually deleted.", self.mock_stdout.getvalue())
        mock_unlink.assert_not_called() # Crucial for dry run
        mock_input.assert_not_called() # No confirmation needed for dry run
        mock_sys_exit.assert_called_once_with(0) # Should exit successfully

    @patch('src.tidy_upper.scan_directory')
    @patch('src.tidy_upper.get_file_age_days', return_value=35) # For printing age
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.input', return_value='y') # Mock user confirmation
    @patch('pathlib.Path.unlink') # Mock file deletion
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during tests
    def test_main_delete_confirmed(self, mock_sys_exit, mock_unlink, mock_input, mock_parse_args, mock_scan_directory, mock_get_file_age_days_for_print):
        # Mock rationale: Simulate command-line arguments, directory scanning results,
        # user confirmation, and prevent actual file deletion during a deletion test.
        
        # Configure mock arguments for deletion with confirmation
        mock_parse_args.return_value = MagicMock(
            dirs=["/mock/dir"],
            age=30,
            dry_run=False,
            confirm=False
        )

        mock_file1 = MagicMock(spec=Path, name="file1")
        mock_file1.__str__.return_value = "/mock/dir/old_file1.log"
        mock_file2 = MagicMock(spec=Path, name="file2")
        mock_file2.__str__.return_value = "/mock/dir/old_file2.tmp"
        
        mock_scan_directory.return_value = [mock_file1, mock_file2]

        tidy_upper.main()

        # Assertions for deletion
        self.assertIn("Identified 2 temporal tears", self.mock_stdout.getvalue())
        self.assertIn("Proceed with mending 2 temporal tears? (y/N):", self.mock_stdout.getvalue())
        mock_input.assert_called_once() # User confirmation should be requested
        mock_unlink.assert_any_call() # Both files should be attempted to be unlinked
        self.assertEqual(mock_unlink.call_count, 2)
        self.assertIn("Successfully mended 2 temporal tears.", self.mock_stdout.getvalue())
        mock_sys_exit.assert_called_once_with(0)

    @patch('src.tidy_upper.scan_directory')
    @patch('src.tidy_upper.get_file_age_days', return_value=35) # For printing age
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.input', return_value='n') # Mock user declining confirmation
    @patch('pathlib.Path.unlink') # Mock file deletion
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during tests
    def test_main_delete_declined(self, mock_sys_exit, mock_unlink, mock_input, mock_parse_args, mock_scan_directory, mock_get_file_age_days_for_print):
        # Mock rationale: Simulate user declining deletion, ensuring no files are deleted
        # and the program exits with the correct no-op code.
        
        mock_parse_args.return_value = MagicMock(
            dirs=["/mock/dir"],
            age=30,
            dry_run=False,
            confirm=False
        )

        mock_file1 = MagicMock(spec=Path, name="file1")
        mock_file1.__str__.return_value = "/mock/dir/old_file1.log"
        mock_scan_directory.return_value = [mock_file1]

        tidy_upper.main()

        self.assertIn("Mending aborted. The tears remain.", self.mock_stdout.getvalue())
        mock_unlink.assert_not_called() # No deletion should occur
        mock_sys_exit.assert_called_once_with(2) # Should exit with no-op code

    @patch('src.tidy_upper.scan_directory')
    @patch('src.tidy_upper.get_file_age_days', return_value=35) # For printing age
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.input', return_value='y') # Mock user confirmation (not used if --confirm)
    @patch('pathlib.Path.unlink') # Mock file deletion
    @patch('sys.exit') # Mock sys.exit to prevent actual exit during tests
    def test_main_delete_with_confirm_flag(self, mock_sys_exit, mock_unlink, mock_input, mock_parse_args, mock_scan_directory, mock_get_file_age_days_for_print):
        # Mock rationale: Test the --confirm flag bypasses user input, ensuring
        # direct deletion without interaction.
        
        mock_parse_args.return_value = MagicMock(
            dirs=["/mock/dir"],
            age=30,
            dry_run=False,
            confirm=True # This flag should bypass input()
        )

        mock_file1 = MagicMock(spec=Path, name="file1")
        mock_file1.__str__.return_value = "/mock/dir/old_file1.log"
        mock_scan_directory.return_value = [mock_file1]

        tidy_upper.main()

        self.assertIn("Mending temporal tears...", self.mock_stdout.getvalue())
        mock_input.assert_not_called() # Input should be bypassed
        mock_unlink.assert_called_once_with() # Deletion should proceed
        mock_sys_exit.assert_called_once_with(0)

    @patch('src.tidy_upper.scan_directory', return_value=[])
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_no_old_files(self, mock_sys_exit, mock_parse_args, mock_scan_directory):
        # Mock rationale: Test the scenario where no old files are found,
        # ensuring the correct message is printed and the program exits successfully.
        
        mock_parse_args.return_value = MagicMock(
            dirs=["/mock/dir"],
            age=30,
            dry_run=False,
            confirm=False
        )

        tidy_upper.main()

        self.assertIn("The temporal fabric is pristine! No tears older than 30 days found.", self.mock_stdout.getvalue())
        mock_scan_directory.assert_called_once()
        mock_sys_exit.assert_called_once_with(0)

    @patch('src.tidy_upper.scan_directory')
    @patch('src.tidy_upper.get_file_age_days', return_value=35)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.input', return_value='y')
    @patch('pathlib.Path.unlink', side_effect=OSEerver("Permission denied"))
    @patch('sys.exit')
    def test_main_deletion_failure(self, mock_sys_exit, mock_unlink, mock_input, mock_parse_args, mock_scan_directory, mock_get_file_age_days_for_print):
        # Mock rationale: Simulate a file deletion failure (e.g., permission denied),
        # ensuring the error is reported and the program still exits successfully
        # (as some files might have been deleted).
        
        mock_parse_args.return_value = MagicMock(
            dirs=["/mock/dir"],
            age=30,
            dry_run=False,
            confirm=True
        )

        mock_file1 = MagicMock(spec=Path, name="file1")
        mock_file1.__str__.return_value = "/mock/dir/old_file1.log"
        mock_scan_directory.return_value = [mock_file1]

        tidy_upper.main()

        self.assertIn("Failed to mend /mock/dir/old_file1.log: Permission denied", self.mock_stderr.getvalue())
        self.assertIn("Successfully mended 0 temporal tears.", self.mock_stdout.getvalue())
        self.assertIn("1 tears resisted mending.", self.mock_stdout.getvalue())
        mock_sys_exit.assert_called_once_with(0)


if __name__ == '__main__':
    unittest.main()
