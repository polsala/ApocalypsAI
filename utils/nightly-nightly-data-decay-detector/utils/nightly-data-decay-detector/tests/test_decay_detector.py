import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the function to be tested
from src.decay_detector import find_decayed_files

class TestDecayDetector(unittest.TestCase):

    # Define a fixed current time for deterministic testing
    TEST_CURRENT_TIME = datetime(2024, 1, 1, 12, 0, 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getatime')
    def test_no_decayed_files(self, mock_getatime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a valid directory path.
        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory with files.
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log'])
        ]

        # Mock rationale: Simulate files that are very recent (not decayed).
        # current_time - 1 day, well within a 90-day threshold.
        recent_timestamp = (self.TEST_CURRENT_TIME - timedelta(days=1)).timestamp()
        mock_getmtime.return_value = recent_timestamp
        mock_getatime.return_value = recent_timestamp

        result = find_decayed_files('/test_dir', 90, current_time=self.TEST_CURRENT_TIME)
        self.assertEqual(len(result), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getatime')
    def test_decayed_files_both_old(self, mock_getatime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a valid directory path.
        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory with files.
        mock_walk.return_value = [
            ('/test_dir', [], ['old_file.txt'])
        ]

        # Mock rationale: Simulate both modification and access times being old (beyond 90 days).
        old_timestamp = (self.TEST_CURRENT_TIME - timedelta(days=100)).timestamp()

        mock_getmtime.return_value = old_timestamp
        mock_getatime.return_value = old_timestamp

        result = find_decayed_files('/test_dir', 90, current_time=self.TEST_CURRENT_TIME)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['file'], os.path.join('/test_dir', 'old_file.txt'))
        self.assertGreaterEqual(result[0]['age_days'], 90)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getatime')
    def test_not_decayed_if_one_is_recent(self, mock_getatime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a valid directory path.
        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory with files.
        mock_walk.return_value = [
            ('/test_dir', [], ['mixed_file.txt'])
        ]

        # Mock rationale: Simulate an old modification time.
        old_timestamp = (self.TEST_CURRENT_TIME - timedelta(days=100)).timestamp()
        # Mock rationale: Simulate a recent access time.
        recent_timestamp = (self.TEST_CURRENT_TIME - timedelta(days=5)).timestamp()

        # Case 1: mtime old, atime recent -> should NOT be decayed
        def get_mtime_side_effect_1(path):
            return old_timestamp
        def get_atime_side_effect_1(path):
            return recent_timestamp
        mock_getmtime.side_effect = get_mtime_side_effect_1
        mock_getatime.side_effect = get_atime_side_effect_1
        result = find_decayed_files('/test_dir', 90, current_time=self.TEST_CURRENT_TIME)
        self.assertEqual(len(result), 0, "File should not be decayed if accessed recently.")

        # Case 2: mtime recent, atime old -> should NOT be decayed
        def get_mtime_side_effect_2(path):
            return recent_timestamp
        def get_atime_side_effect_2(path):
            return old_timestamp
        mock_getmtime.side_effect = get_mtime_side_effect_2
        mock_getatime.side_effect = get_atime_side_effect_2
        result = find_decayed_files('/test_dir', 90, current_time=self.TEST_CURRENT_TIME)
        self.assertEqual(len(result), 0, "File should not be decayed if modified recently.")

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getatime')
    def test_empty_directory(self, mock_getatime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a valid directory path.
        mock_isdir.return_value = True

        # Mock rationale: Simulate an empty directory.
        mock_walk.return_value = [
            ('/empty_dir', [], [])
        ]

        result = find_decayed_files('/empty_dir', 90, current_time=self.TEST_CURRENT_TIME)
        self.assertEqual(len(result), 0)

    @patch('os.path.isdir')
    def test_invalid_directory(self, mock_isdir):
        # Mock rationale: Simulate an invalid directory path.
        mock_isdir.return_value = False

        result = find_decayed_files('/non_existent_dir', 90, current_time=self.TEST_CURRENT_TIME)
        self.assertEqual(len(result), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getatime')
    def test_threshold_zero_days(self, mock_getatime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a valid directory path.
        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory with files.
        mock_walk.return_value = [
            ('/test_dir', [], ['file_zero.txt'])
        ]

        # Mock rationale: Simulate a file modified/accessed just a second before the current_time.
        just_old_timestamp = (self.TEST_CURRENT_TIME - timedelta(seconds=1)).timestamp()
        mock_getmtime.return_value = just_old_timestamp
        mock_getatime.return_value = just_old_timestamp

        result = find_decayed_files('/test_dir', 0, current_time=self.TEST_CURRENT_TIME)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['file'], os.path.join('/test_dir', 'file_zero.txt'))
        self.assertGreaterEqual(result[0]['age_days'], 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getatime')
    def test_os_error_handling(self, mock_getatime, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a valid directory path.
        mock_isdir.return_value = True

        # Mock rationale: Simulate a directory with a file.
        mock_walk.return_value = [
            ('/test_dir', [], ['inaccessible_file.txt'])
        ]

        # Mock rationale: Simulate an OSError when trying to get file times.
        mock_getmtime.side_effect = OSError("Permission denied")
        mock_getatime.side_effect = OSError("Permission denied")

        # We expect no files to be returned, as errors are suppressed.
        result = find_decayed_files('/test_dir', 90, current_time=self.TEST_CURRENT_TIME)
        self.assertEqual(len(result), 0)
