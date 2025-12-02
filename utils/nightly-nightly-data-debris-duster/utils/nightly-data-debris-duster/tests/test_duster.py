import os
import shutil
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the src directory to the path for importing duster
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from duster import find_data_debris, report_debris, quarantine_debris, dust_debris, get_file_age_days

class TestDataDebrisDuster(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_dir = "test_temp_dir"
        self.quarantine_dir = "test_quarantine_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(self.quarantine_dir, exist_ok=True)

        # Mock datetime.now() to control file ages
        self.mock_now = datetime(2023, 10, 26, 10, 0, 0) # A fixed "current" time
        self.patcher_datetime_now = patch('duster.datetime')
        self.mock_datetime = self.patcher_datetime_now.start()
        self.mock_datetime.now.return_value = self.mock_now
        # Mock rationale: Keep original datetime.fromtimestamp and timedelta for correct internal calculations.
        # Also, allow datetime() constructor calls to pass through to the real datetime for objects created by fromtimestamp.
        self.mock_datetime.fromtimestamp = datetime.fromtimestamp
        self.mock_datetime.timedelta = timedelta
        self.mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

    def tearDown(self):
        # Clean up temporary directories
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(self.quarantine_dir):
            shutil.rmtree(self.quarantine_dir)
        self.patcher_datetime_now.stop()

    @patch('duster.os.path.getmtime')
    @patch('duster.os.walk')
    @patch('duster.os.path.isdir')
    def test_find_data_debris_no_files(self, mock_isdir, mock_os_walk, mock_getmtime):
        # Mock rationale: Simulate an empty directory structure to ensure no debris is found.
        mock_isdir.return_value = True
        mock_os_walk.return_value = [
            (os.path.join(self.test_dir, 'subdir'), [], [])
        ]
        debris = find_data_debris([self.test_dir], 90)
        self.assertEqual(len(debris), 0)

    @patch('duster.os.path.getmtime')
    @patch('duster.os.walk')
    @patch('duster.os.path.isdir')
    def test_find_data_debris_recent_files(self, mock_isdir, mock_os_walk, mock_getmtime):
        # Mock rationale: Simulate files that are too new to be considered debris.
        mock_isdir.return_value = True
        mock_os_walk.return_value = [
            (self.test_dir, [], ['recent_file.txt'])
        ]
        # Set mtime to be recent (e.g., 10 days ago)
        recent_timestamp = (self.mock_now - timedelta(days=10)).timestamp()
        mock_getmtime.return_value = recent_timestamp

        debris = find_data_debris([self.test_dir], 90)
        self.assertEqual(len(debris), 0)

    @patch('duster.os.path.getmtime')
    @patch('duster.os.walk')
    @patch('duster.os.path.isdir')
    def test_find_data_debris_old_files(self, mock_isdir, mock_os_walk, mock_getmtime):
        # Mock rationale: Simulate files that are old enough to be considered debris.
        mock_isdir.return_value = True
        mock_os_walk.return_value = [
            (self.test_dir, [], ['old_file_1.txt', 'old_file_2.log'])
        ]
        # Set mtime to be old (e.g., 100 days ago)
        old_timestamp = (self.mock_now - timedelta(days=100)).timestamp()
        mock_getmtime.return_value = old_timestamp

        debris = find_data_debris([self.test_dir], 90)
        self.assertEqual(len(debris), 2)
        self.assertIn(os.path.join(self.test_dir, 'old_file_1.txt'), debris)
        self.assertIn(os.path.join(self.test_dir, 'old_file_2.log'), debris)

    @patch('duster.os.path.getmtime')
    @patch('duster.os.walk')
    @patch('duster.os.path.isdir')
    def test_find_data_debris_mixed_files(self, mock_isdir, mock_os_walk, mock_getmtime):
        # Mock rationale: Simulate a mix of old and recent files to ensure correct filtering.
        mock_isdir.return_value = True
        
        # Define specific mtimes for each file
        file_mtimes = {
            os.path.join(self.test_dir, 'old_file.txt'): (self.mock_now - timedelta(days=100)).timestamp(),
            os.path.join(self.test_dir, 'recent_file.txt'): (self.mock_now - timedelta(days=10)).timestamp(),
            os.path.join(self.test_dir, 'another_old.log'): (self.mock_now - timedelta(days=120)).timestamp(),
        }

        def mock_getmtime_side_effect(filepath):
            return file_mtimes.get(filepath, (self.mock_now - timedelta(days=1)).timestamp()) # Default to recent if not specified

        mock_getmtime.side_effect = mock_getmtime_side_effect
        mock_os_walk.return_value = [
            (self.test_dir, [], ['old_file.txt', 'recent_file.txt', 'another_old.log'])
        ]

        debris = find_data_debris([self.test_dir], 90)
        self.assertEqual(len(debris), 2)
        self.assertIn(os.path.join(self.test_dir, 'old_file.txt'), debris)
        self.assertIn(os.path.join(self.test_dir, 'another_old.log'), debris)
        self.assertNotIn(os.path.join(self.test_dir, 'recent_file.txt'), debris)

    @patch('builtins.print')
    def test_report_debris_empty(self, mock_print):
        # Mock rationale: Capture print output to verify the "no debris" message is displayed.
        report_debris([])
        mock_print.assert_called_with("\n✨ All clear! No significant data debris detected. Your digital wasteland is surprisingly tidy.")

    @patch('builtins.print')
    @patch('duster.get_file_age_days')
    def test_report_debris_with_files(self, mock_get_file_age_days, mock_print):
        # Mock rationale: Capture print output and mock file age for consistent reporting messages.
        mock_get_file_age_days.side_effect = [100, 120] # For the two files
        debris = ['/path/to/old_file.txt', '/path/to/another_old.log']
        report_debris(debris)
        mock_print.assert_any_call("\n🚨 Attention, Scavenger! 2 pieces of data debris detected:")
        mock_print.assert_any_call("  - /path/to/old_file.txt (Age: 100 days)")
        mock_print.assert_any_call("  - /path/to/another_old.log (Age: 120 days)")

    @patch('duster.shutil.move')
    @patch('duster.os.makedirs')
    @patch('builtins.print')
    @patch('duster.os.path.commonpath')
    @patch('duster.os.path.relpath')
    def test_quarantine_debris(self, mock_relpath, mock_commonpath, mock_print, mock_makedirs, mock_move):
        # Mock rationale: Simulate file system operations (move, makedirs) without actual disk changes.
        # Mock commonpath and relpath to control the destination path construction deterministically.
        mock_commonpath.return_value = self.test_dir # Assume test_dir is the common root for mock
        mock_relpath.side_effect = lambda path, start: os.path.basename(path) # Simplify relative path for mock

        debris = [os.path.join(self.test_dir, 'old_file.txt'), os.path.join(self.test_dir, 'another_old.log')]
        quarantine_debris(debris, self.quarantine_dir)

        mock_makedirs.assert_any_call(self.quarantine_dir, exist_ok=True)
        mock_move.assert_any_call(os.path.join(self.test_dir, 'old_file.txt'), os.path.join(self.quarantine_dir, 'old_file.txt'))
        mock_move.assert_any_call(os.path.join(self.test_dir, 'another_old.log'), os.path.join(self.quarantine_dir, 'another_old.log'))
        mock_print.assert_any_call(f"\n📦 Initiating Quarantine Protocol for 2 items to '{self.quarantine_dir}'...")
        mock_print.assert_any_call("\n✅ Quarantine complete. 2 items safely contained. Review them at your leisure.")

    @patch('duster.os.remove')
    @patch('builtins.print')
    def test_dust_debris(self, mock_print, mock_remove):
        # Mock rationale: Simulate file deletion without actual disk changes.
        debris = ['/path/to/old_file.txt', '/path/to/another_old.log']
        dust_debris(debris)

        mock_remove.assert_any_call('/path/to/old_file.txt')
        mock_remove.assert_any_call('/path/to/another_old.log')
        mock_print.assert_any_call("\n🔥 Activating Dusting Protocol for 2 items. This is irreversible!")
        mock_print.assert_any_call("\n💀 Dusting complete. 2 items permanently removed. May they rest in digital peace.")

    @patch('duster.os.path.getmtime')
    def test_get_file_age_days(self, mock_getmtime):
        # Mock rationale: Control the file modification time to test age calculation deterministically.
        # File modified 100 days ago
        old_timestamp = (self.mock_now - timedelta(days=100)).timestamp()
        mock_getmtime.return_value = old_timestamp
        age = get_file_age_days('/fake/path/file.txt')
        self.assertEqual(age, 100)

        # File modified 5 days ago
        recent_timestamp = (self.mock_now - timedelta(days=5)).timestamp()
        mock_getmtime.return_value = recent_timestamp
        age = get_file_age_days('/fake/path/file.txt')
        self.assertEqual(age, 5)

    @patch('duster.os.path.getmtime')
    def test_get_file_age_days_error(self, mock_getmtime):
        # Mock rationale: Simulate an OSError during mtime retrieval (e.g., file not found) to test error handling.
        mock_getmtime.side_effect = OSError("File not found")
        age = get_file_age_days('/nonexistent/file.txt')
        self.assertEqual(age, -1) # Expect -1 for error

    @patch('duster.os.path.isdir')
    @patch('builtins.print')
    def test_find_data_debris_invalid_path(self, mock_print, mock_isdir):
        # Mock rationale: Simulate an invalid directory path being passed to ensure it's skipped with a warning.
        mock_isdir.return_value = False # First path is invalid
        debris = find_data_debris(['/invalid/path'], 90)
        self.assertEqual(len(debris), 0)
        mock_print.assert_any_call("⚠️ Warning: Path '/invalid/path' is not a valid directory. Skipping.")
