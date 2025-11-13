import unittest
import os
import tempfile
import shutil
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Import the functions to test
from src.dust_collector import find_dust, clean_dust, get_file_age_days

class TestCosmicDustCollector(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.current_time = datetime(2023, 10, 27, 10, 0, 0) # Fixed current time for deterministic tests

        # Create some test files and directories
        os.makedirs(os.path.join(self.test_dir, "sub_dir_a"))
        os.makedirs(os.path.join(self.test_dir, "sub_dir_b"))

        # Files for age testing
        self._create_file(os.path.join(self.test_dir, "old_log.log"), age_days=10)
        self._create_file(os.path.join(self.test_dir, "recent_log.log"), age_days=1)
        self._create_file(os.path.join(self.test_dir, "sub_dir_a", "very_old.tmp"), age_days=30)

        # Files for pattern testing
        self._create_file(os.path.join(self.test_dir, "temp_file.tmp"))
        self._create_file(os.path.join(self.test_dir, "backup.bak"))
        self._create_file(os.path.join(self.test_dir, "important.txt"))
        self._create_file(os.path.join(self.test_dir, "sub_dir_b", "another.log"))
        self._create_file(os.path.join(self.test_dir, "sub_dir_b", "config.ini.bak"))
        self._create_file(os.path.join(self.test_dir, "specific_file_to_delete.txt"))

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def _create_file(self, filepath, content="test", age_days=0):
        """Helper to create a file with specific content and modification time."""
        with open(filepath, "w") as f:
            f.write(content)
        # Set modification time relative to self.current_time
        mod_time = self.current_time - timedelta(days=age_days)
        os.utime(filepath, (mod_time.timestamp(), mod_time.timestamp()))

    @patch('src.dust_collector.datetime')
    def test_get_file_age_days(self, mock_datetime):
        # Mock rationale: We need to control the 'current' time to make age calculations deterministic.
        # By patching datetime.now(), we ensure that get_file_age_days always calculates age
        # relative to our fixed self.current_time.
        mock_datetime.now.return_value = self.current_time
        mock_datetime.fromtimestamp = datetime.fromtimestamp # Keep original fromtimestamp

        filepath = os.path.join(self.test_dir, "old_log.log")
        self.assertEqual(get_file_age_days(filepath), 10)

        filepath = os.path.join(self.test_dir, "recent_log.log")
        self.assertEqual(get_file_age_days(filepath), 1)

        filepath = os.path.join(self.test_dir, "sub_dir_a", "very_old.tmp")
        self.assertEqual(get_file_age_days(filepath), 30)

    @patch('src.dust_collector.datetime')
    def test_find_dust_by_age(self, mock_datetime):
        # Mock rationale: See test_get_file_age_days. Essential for deterministic age-based filtering.
        mock_datetime.now.return_value = self.current_time
        mock_datetime.fromtimestamp = datetime.fromtimestamp

        # Find files older than 5 days
        dust = find_dust(self.test_dir, age_days=5)
        expected_dust = [
            os.path.join(self.test_dir, "old_log.log"),
            os.path.join(self.test_dir, "sub_dir_a", "very_old.tmp")
        ]
        self.assertCountEqual(dust, expected_dust)

        # Find files older than 20 days
        dust = find_dust(self.test_dir, age_days=20)
        expected_dust = [
            os.path.join(self.test_dir, "sub_dir_a", "very_old.tmp")
        ]
        self.assertCountEqual(dust, expected_dust)

        # No files older than 40 days
        dust = find_dust(self.test_dir, age_days=40)
        self.assertEqual(len(dust), 0)

    @patch('src.dust_collector.datetime')
    def test_find_dust_by_patterns(self, mock_datetime):
        # Mock rationale: See test_get_file_age_days. Not strictly needed for pattern matching,
        # but good practice to keep consistent if age filtering is also involved.
        mock_datetime.now.return_value = self.current_time
        mock_datetime.fromtimestamp = datetime.fromtimestamp

        # Find .tmp and .bak files
        dust = find_dust(self.test_dir, patterns=['*.tmp', '*.bak'])
        expected_dust = [
            os.path.join(self.test_dir, "temp_file.tmp"),
            os.path.join(self.test_dir, "backup.bak"),
            os.path.join(self.test_dir, "sub_dir_a", "very_old.tmp"),
            os.path.join(self.test_dir, "sub_dir_b", "config.ini.bak")
        ]
        self.assertCountEqual(dust, expected_dust)

        # Find .log files
        dust = find_dust(self.test_dir, patterns=['*.log'])
        expected_dust = [
            os.path.join(self.test_dir, "old_log.log"),
            os.path.join(self.test_dir, "recent_log.log"),
            os.path.join(self.test_dir, "sub_dir_b", "another.log")
        ]
        self.assertCountEqual(dust, expected_dust)

        # Find specific file by exact name
        dust = find_dust(self.test_dir, patterns=['specific_file_to_delete.txt'])
        expected_dust = [
            os.path.join(self.test_dir, "specific_file_to_delete.txt")
        ]
        self.assertCountEqual(dust, expected_dust)

        # Find specific file by wildcard
        dust = find_dust(self.test_dir, patterns=['important.*'])
        expected_dust = [
            os.path.join(self.test_dir, "important.txt")
        ]
        self.assertCountEqual(dust, expected_dust)

    @patch('src.dust_collector.datetime')
    def test_find_dust_by_age_and_patterns(self, mock_datetime):
        # Mock rationale: See test_get_file_age_days. Essential for deterministic age-based filtering.
        mock_datetime.now.return_value = self.current_time
        mock_datetime.fromtimestamp = datetime.fromtimestamp

        # Find files that are either older than 5 days OR match '*.log' or '*.tmp'
        dust = find_dust(self.test_dir, age_days=5, patterns=['*.log', '*.tmp'])
        expected_dust = [
            os.path.join(self.test_dir, "old_log.log"), # Age > 5 days
            os.path.join(self.test_dir, "recent_log.log"), # Matches *.log
            os.path.join(self.test_dir, "sub_dir_a", "very_old.tmp"), # Age > 5 days
            os.path.join(self.test_dir, "temp_file.tmp"), # Matches *.tmp
            os.path.join(self.test_dir, "sub_dir_b", "another.log") # Matches *.log
        ]
        self.assertCountEqual(dust, expected_dust)

        # Find files that are either older than 1 day OR match 'backup.bak'
        dust = find_dust(self.test_dir, age_days=1, patterns=['backup.bak'])
        expected_dust = [
            os.path.join(self.test_dir, "old_log.log"), # Age > 1 day
            os.path.join(self.test_dir, "recent_log.log"), # Age > 1 day
            os.path.join(self.test_dir, "sub_dir_a", "very_old.tmp"), # Age > 1 day
            os.path.join(self.test_dir, "backup.bak") # Matches pattern
        ]
        self.assertCountEqual(dust, expected_dust)

    @patch('src.dust_collector.os.remove')
    @patch('builtins.print') # Mock print to capture output
    def test_clean_dust_dry_run(self, mock_print, mock_os_remove):
        # Mock rationale: We don't want to actually delete files during a dry run test.
        # Mocking os.remove ensures no file system changes.
        # Mocking print allows us to verify the output messages.
        files_to_clean = [
            os.path.join(self.test_dir, "old_log.log"),
            os.path.join(self.test_dir, "temp_file.tmp")
        ]
        clean_dust(files_to_clean, dry_run=True)

        mock_os_remove.assert_not_called()
        mock_print.assert_any_call("--- DRY RUN ---")
        mock_print.assert_any_call(f"Would delete: {files_to_clean[0]}")
        mock_print.assert_any_call(f"Would delete: {files_to_clean[1]}")
        mock_print.assert_any_call("--- COMPLETE ---")

    @patch('builtins.print') # Mock print to capture output
    def test_clean_dust_actual_run(self, mock_print):
        # Mock rationale: We want to verify actual deletion. We'll use real files in tempdir.
        # Mocking print allows us to verify the output messages.
        file1 = os.path.join(self.test_dir, "to_delete_1.txt")
        file2 = os.path.join(self.test_dir, "to_delete_2.txt")
        self._create_file(file1)
        self._create_file(file2)

        self.assertTrue(os.path.exists(file1))
        self.assertTrue(os.path.exists(file2))

        files_to_clean = [file1, file2]
        clean_dust(files_to_clean, dry_run=False)

        self.assertFalse(os.path.exists(file1))
        self.assertFalse(os.path.exists(file2))
        mock_print.assert_any_call("--- CLEANING ---")
        mock_print.assert_any_call(f"Deleted: {file1}")
        mock_print.assert_any_call(f"Deleted: {file2}")
        mock_print.assert_any_call("--- COMPLETE ---")

    @patch('builtins.print')
    def test_clean_dust_no_files(self, mock_print):
        # Mock rationale: Mocking print allows us to verify the output messages.
        clean_dust([], dry_run=False)
        mock_print.assert_any_call("No cosmic dust found to clean.")
        mock_print.assert_not_any_call("--- CLEANING ---") # Ensure it doesn't print header if no files

    @patch('src.dust_collector.os.remove')
    @patch('builtins.print')
    def test_clean_dust_error_on_delete(self, mock_print, mock_os_remove):
        # Mock rationale: Simulate an OSError during file deletion to test error handling.
        # Mocking os.remove to raise an exception.
        # Mocking print allows us to verify the output messages.
        mock_os_remove.side_effect = OSError("Permission denied")
        file_to_delete = os.path.join(self.test_dir, "error_file.txt")
        self._create_file(file_to_delete)

        files_to_clean = [file_to_delete]
        clean_dust(files_to_clean, dry_run=False)

        mock_os_remove.assert_called_once_with(file_to_delete)
        mock_print.assert_any_call(f"Error deleting {file_to_delete}: Permission denied")
