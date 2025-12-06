import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import os
import sys

# Add the src directory to the Python path to allow importing detector.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import detector

class TestChronosDriftDetector(unittest.TestCase):

    @patch('detector.datetime')
    @patch('detector.os.stat')
    @patch('detector.os.walk')
    @patch('detector.os.path.exists')
    def test_future_mtime_drift_detection(self, mock_exists, mock_walk, mock_stat, mock_datetime):
        # Mock rationale: Simulate the current time for deterministic testing.
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        # Mock rationale: Allow datetime.fromtimestamp to function normally with mocked timestamps.
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        # Mock rationale: Allow timedelta to function normally for time calculations.
        mock_datetime.timedelta = timedelta

        # Mock rationale: Simulate a directory structure with a file.
        mock_exists.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['future_file.txt'])
        ]

        # Mock rationale: Simulate file stat information, specifically mtime 100 seconds in the future.
        mock_stat_obj = MagicMock()
        mock_stat_obj.st_mtime = (mock_datetime.now.return_value + timedelta(seconds=100)).timestamp()
        mock_stat_obj.st_ctime = (mock_datetime.now.return_value - timedelta(seconds=10)).timestamp() # Normal ctime
        mock_stat.return_value = mock_stat_obj

        # Mock rationale: Suppress print statements during test execution to avoid polluting test output.
        with patch('builtins.print') as mock_print:
            drifted_files = detector.detect_chronos_drift(
                paths=['/test_dir'],
                future_threshold_seconds=60, # Threshold is 60s, file is 100s in future
                past_threshold_seconds=0
            )

            self.assertEqual(len(drifted_files), 1)
            self.assertIn('/test_dir/future_file.txt', drifted_files)
            mock_print.assert_any_call(self.assertRegex(f".*DRIFTED.*Future MTime.*-> /test_dir/future_file.txt"))

    @patch('detector.datetime')
    @patch('detector.os.stat')
    @patch('detector.os.walk')
    @patch('detector.os.path.exists')
    def test_future_ctime_drift_detection(self, mock_exists, mock_walk, mock_stat, mock_datetime):
        # Mock rationale: Simulate the current time for deterministic testing.
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        # Mock rationale: Allow datetime.fromtimestamp to function normally with mocked timestamps.
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        # Mock rationale: Allow timedelta to function normally for time calculations.
        mock_datetime.timedelta = timedelta

        # Mock rationale: Simulate a directory structure with a file.
        mock_exists.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['future_ctime_file.txt'])
        ]

        # Mock rationale: Simulate file stat information, specifically ctime 100 seconds in the future.
        mock_stat_obj = MagicMock()
        mock_stat_obj.st_mtime = (mock_datetime.now.return_value - timedelta(seconds=10)).timestamp() # Normal mtime
        mock_stat_obj.st_ctime = (mock_datetime.now.return_value + timedelta(seconds=100)).timestamp()
        mock_stat.return_value = mock_stat_obj

        # Mock rationale: Suppress print statements during test execution.
        with patch('builtins.print') as mock_print:
            drifted_files = detector.detect_chronos_drift(
                paths=['/test_dir'],
                future_threshold_seconds=60, # Threshold is 60s, file is 100s in future
                past_threshold_seconds=0
            )

            self.assertEqual(len(drifted_files), 1)
            self.assertIn('/test_dir/future_ctime_file.txt', drifted_files)
            mock_print.assert_any_call(self.assertRegex(f".*DRIFTED.*Future CTime.*-> /test_dir/future_ctime_file.txt"))

    @patch('detector.datetime')
    @patch('detector.os.stat')
    @patch('detector.os.walk')
    @patch('detector.os.path.exists')
    def test_past_mtime_drift_detection(self, mock_exists, mock_walk, mock_stat, mock_datetime):
        # Mock rationale: Simulate the current time for deterministic testing.
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        # Mock rationale: Allow datetime.fromtimestamp to function normally with mocked timestamps.
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        # Mock rationale: Allow timedelta to function normally for time calculations.
        mock_datetime.timedelta = timedelta

        # Mock rationale: Simulate a directory structure with a file.
        mock_exists.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['past_file.txt'])
        ]

        # Mock rationale: Simulate file stat information, specifically mtime 100000 seconds in the past.
        mock_stat_obj = MagicMock()
        mock_stat_obj.st_mtime = (mock_datetime.now.return_value - timedelta(seconds=100000)).timestamp()
        mock_stat_obj.st_ctime = (mock_datetime.now.return_value - timedelta(seconds=100010)).timestamp()
        mock_stat.return_value = mock_stat_obj

        # Mock rationale: Suppress print statements during test execution.
        with patch('builtins.print') as mock_print:
            drifted_files = detector.detect_chronos_drift(
                paths=['/test_dir'],
                future_threshold_seconds=0,
                past_threshold_seconds=86400 # Threshold is 86400s (1 day), file is 100000s in past
            )

            self.assertEqual(len(drifted_files), 1)
            self.assertIn('/test_dir/past_file.txt', drifted_files)
            mock_print.assert_any_call(self.assertRegex(f".*DRIFTED.*Past MTime.*-> /test_dir/past_file.txt"))

    @patch('detector.datetime')
    @patch('detector.os.stat')
    @patch('detector.os.walk')
    @patch('detector.os.path.exists')
    def test_no_drift_detection(self, mock_exists, mock_walk, mock_stat, mock_datetime):
        # Mock rationale: Simulate the current time for deterministic testing.
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        # Mock rationale: Allow datetime.fromtimestamp to function normally with mocked timestamps.
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        # Mock rationale: Allow timedelta to function normally for time calculations.
        mock_datetime.timedelta = timedelta

        # Mock rationale: Simulate a directory structure with a file.
        mock_exists.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['normal_file.txt'])
        ]

        # Mock rationale: Simulate file stat information with normal timestamps.
        mock_stat_obj = MagicMock()
        mock_stat_obj.st_mtime = (mock_datetime.now.return_value - timedelta(seconds=10)).timestamp()
        mock_stat_obj.st_ctime = (mock_datetime.now.return_value - timedelta(seconds=20)).timestamp()
        mock_stat.return_value = mock_stat_obj

        # Mock rationale: Suppress print statements during test execution.
        with patch('builtins.print') as mock_print:
            drifted_files = detector.detect_chronos_drift(
                paths=['/test_dir'],
                future_threshold_seconds=60,
                past_threshold_seconds=86400
            )

            self.assertEqual(len(drifted_files), 0)
            mock_print.assert_any_call("\nNo chronos drift detected. All timestamps appear stable.")

    @patch('detector.datetime')
    @patch('detector.os.stat')
    @patch('detector.os.walk')
    @patch('detector.os.path.exists')
    def test_report_all_option(self, mock_exists, mock_walk, mock_stat, mock_datetime):
        # Mock rationale: Simulate the current time for deterministic testing.
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        # Mock rationale: Allow datetime.fromtimestamp to function normally with mocked timestamps.
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        # Mock rationale: Allow timedelta to function normally for time calculations.
        mock_datetime.timedelta = timedelta

        # Mock rationale: Simulate a directory structure with a file.
        mock_exists.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['normal_file.txt'])
        ]

        # Mock rationale: Simulate file stat information with normal timestamps.
        mock_stat_obj = MagicMock()
        mock_stat_obj.st_mtime = (mock_datetime.now.return_value - timedelta(seconds=10)).timestamp()
        mock_stat_obj.st_ctime = (mock_datetime.now.return_value - timedelta(seconds=20)).timestamp()
        mock_stat.return_value = mock_stat_obj

        # Mock rationale: Suppress print statements during test execution.
        with patch('builtins.print') as mock_print:
            drifted_files = detector.detect_chronos_drift(
                paths=['/test_dir'],
                future_threshold_seconds=60,
                past_threshold_seconds=86400,
                report_all=True
            )

            self.assertEqual(len(drifted_files), 0) # Still no *drifted* files
            mock_print.assert_any_call(self.assertRegex(f".*OK.*MTime:.*-> /test_dir/normal_file.txt"))

    @patch('detector.os.path.exists')
    @patch('builtins.print')
    def test_path_not_found(self, mock_print, mock_exists):
        # Mock rationale: Simulate a non-existent path.
        mock_exists.return_value = False

        drifted_files = detector.detect_chronos_drift(
            paths=['/non_existent_dir'],
            future_threshold_seconds=60,
            past_threshold_seconds=0
        )

        self.assertEqual(len(drifted_files), 0)
        mock_print.assert_any_call("Warning: Path not found: /non_existent_dir")

    @patch('detector.datetime')
    @patch('detector.os.stat')
    @patch('detector.os.walk')
    @patch('detector.os.path.exists')
    @patch('builtins.print')
    def test_os_error_on_stat(self, mock_print, mock_exists, mock_walk, mock_stat, mock_datetime):
        # Mock rationale: Simulate the current time for deterministic testing.
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        # Mock rationale: Allow datetime.fromtimestamp to function normally with mocked timestamps.
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        # Mock rationale: Allow timedelta to function normally for time calculations.
        mock_datetime.timedelta = timedelta

        # Mock rationale: Simulate a directory structure with a file.
        mock_exists.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['unreadable_file.txt'])
        ]

        # Mock rationale: Simulate an OSError when trying to stat a file.
        mock_stat.side_effect = OSError("Permission denied")

        drifted_files = detector.detect_chronos_drift(
            paths=['/test_dir'],
            future_threshold_seconds=60,
            past_threshold_seconds=0
        )

        self.assertEqual(len(drifted_files), 0)
        mock_print.assert_any_call("Could not get timestamps for /test_dir/unreadable_file.txt")


if __name__ == '__main__':
    unittest.main()
