import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import time
from datetime import datetime, timedelta

# Add the src directory to the path to import detector
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import detector

class TestTemporalAnomalyDetector(unittest.TestCase):

    def setUp(self):
        # Set a fixed current time for deterministic tests
        self.mock_current_time = datetime(2023, 10, 27, 10, 0, 0)
        self.mock_current_time_epoch = self.mock_current_time.timestamp()

        # Patch the time-related functions in the detector module
        self.patcher_get_current_time = patch('detector.get_current_time_epoch', return_value=self.mock_current_time_epoch)
        self.mock_get_current_time = self.patcher_get_current_time.start()

        self.patcher_get_file_mtime = patch('detector.get_file_mtime_epoch')
        self.mock_get_file_mtime = self.patcher_get_file_mtime.start()

        self.patcher_path_exists = patch('detector.path_exists')
        self.mock_path_exists = self.patcher_path_exists.start()

        self.patcher_is_directory = patch('detector.is_directory')
        self.mock_is_directory = self.patcher_is_directory.start()

        self.patcher_list_directory_contents = patch('detector.list_directory_contents')
        self.mock_list_directory_contents = self.patcher_list_directory_contents.start()

    def tearDown(self):
        self.patcher_get_current_time.stop()
        self.patcher_get_file_mtime.stop()
        self.patcher_path_exists.stop()
        self.patcher_is_directory.stop()
        self.patcher_list_directory_contents.stop()

    # --- Test Cases for File Monitoring ---

    def test_file_vanished(self):
        self.mock_path_exists.return_value = False
        anomalies = detector.detect_anomalies("/nonexistent/file.log")
        self.assertIn("Path '/nonexistent/file.log' has vanished from existence!", anomalies[0])
        self.assertEqual(len(anomalies), 1)

    def test_file_too_old(self):
        self.mock_path_exists.return_value = True
        self.mock_is_directory.return_value = False
        # File modified 2 days ago
        old_mtime = (self.mock_current_time - timedelta(days=2)).timestamp()
        self.mock_get_file_mtime.return_value = old_mtime

        # Max age 1 day
        anomalies = detector.detect_anomalies("/path/to/old_file.log", max_age_seconds=timedelta(days=1).total_seconds())
        self.assertIn("File '/path/to/old_file.log' is", anomalies[0])
        self.assertIn("seconds old (>86400s). It's ancient!", anomalies[0])
        self.assertEqual(len(anomalies), 1)

    def test_file_recent_no_anomaly(self):
        self.mock_path_exists.return_value = True
        self.mock_is_directory.return_value = False
        # File modified 12 hours ago
        recent_mtime = (self.mock_current_time - timedelta(hours=12)).timestamp()
        self.mock_get_file_mtime.return_value = recent_mtime

        # Max age 1 day
        anomalies = detector.detect_anomalies("/path/to/recent_file.log", max_age_seconds=timedelta(days=1).total_seconds())
        self.assertEqual(len(anomalies), 0)

    def test_file_no_age_check(self):
        self.mock_path_exists.return_value = True
        self.mock_is_directory.return_value = False
        # File modified 10 days ago, but no max_age_seconds specified
        old_mtime = (self.mock_current_time - timedelta(days=10)).timestamp()
        self.mock_get_file_mtime.return_value = old_mtime

        anomalies = detector.detect_anomalies("/path/to/any_file.log")
        self.assertEqual(len(anomalies), 0)

    # --- Test Cases for Directory Monitoring ---

    def test_directory_vanished(self):
        self.mock_path_exists.return_value = False
        self.mock_is_directory.return_value = False # Not a directory if it doesn't exist
        anomalies = detector.detect_anomalies("/nonexistent/dir")
        self.assertIn("Path '/nonexistent/dir' has vanished from existence!", anomalies[0])
        self.assertEqual(len(anomalies), 1)

    def test_directory_contains_old_file(self):
        self.mock_path_exists.return_value = True
        self.mock_is_directory.side_effect = lambda p: p == "/data/logs"
        self.mock_list_directory_contents.return_value = ["app.log", "metrics.txt"]

        # app.log is old (2 days), metrics.txt is recent (1 hour)
        old_mtime = (self.mock_current_time - timedelta(days=2)).timestamp()
        recent_mtime = (self.mock_current_time - timedelta(hours=1)).timestamp()

        def mock_get_mtime_side_effect(path):
            if path == "/data/logs/app.log":
                return old_mtime
            elif path == "/data/logs/metrics.txt":
                return recent_mtime
            return self.mock_current_time_epoch # Default for other paths

        self.mock_get_file_mtime.side_effect = mock_get_mtime_side_effect

        # Max age 1 day
        anomalies = detector.detect_anomalies("/data/logs", max_age_seconds=timedelta(days=1).total_seconds())
        self.assertEqual(len(anomalies), 1)
        self.assertIn("File '/data/logs/app.log' is", anomalies[0])
        self.assertIn("seconds old (>86400s). It's ancient!", anomalies[0])

    def test_directory_contains_unexpected_file(self):
        self.mock_path_exists.return_value = True
        self.mock_is_directory.side_effect = lambda p: p == "/data/uploads"
        self.mock_list_directory_contents.return_value = ["report_2023.csv", "temp_file.bak", "image.jpg"]

        # All files are recent
        self.mock_get_file_mtime.return_value = (self.mock_current_time - timedelta(hours=1)).timestamp()

        # Expecting only CSV files
        anomalies = detector.detect_anomalies("/data/uploads", expected_patterns=[r".*\.csv$"])
        self.assertEqual(len(anomalies), 2)
        self.assertIn("File '/data/uploads/temp_file.bak' does not match any expected pattern.", anomalies[0])
        self.assertIn("File '/data/uploads/image.jpg' does not match any expected pattern.", anomalies[1])

    def test_directory_contains_expected_files_no_anomaly(self):
        self.mock_path_exists.return_value = True
        self.mock_is_directory.side_effect = lambda p: p == "/data/uploads"
        self.mock_list_directory_contents.return_value = ["report_2023.csv", "data_archive.csv"]

        # All files are recent
        self.mock_get_file_mtime.return_value = (self.mock_current_time - timedelta(hours=1)).timestamp()

        # Expecting only CSV files
        anomalies = detector.detect_anomalies("/data/uploads", expected_patterns=[r".*\.csv$"])
        self.assertEqual(len(anomalies), 0)

    def test_directory_contains_both_old_and_unexpected_files(self):
        self.mock_path_exists.return_value = True
        self.mock_is_directory.side_effect = lambda p: p == "/staging"
        self.mock_list_directory_contents.return_value = ["good_file.txt", "old_file.log", "rogue.exe"]

        # good_file.txt: recent, matches pattern
        # old_file.log: old, matches pattern
        # rogue.exe: recent, does not match pattern
        good_mtime = (self.mock_current_time - timedelta(hours=1)).timestamp()
        old_mtime = (self.mock_current_time - timedelta(days=3)).timestamp()
        rogue_mtime = (self.mock_current_time - timedelta(hours=2)).timestamp()

        def mock_get_mtime_side_effect(path):
            if path == "/staging/good_file.txt": return good_mtime
            if path == "/staging/old_file.log": return old_mtime
            if path == "/staging/rogue.exe": return rogue_mtime
            return self.mock_current_time_epoch

        self.mock_get_file_mtime.side_effect = mock_get_mtime_side_effect

        # Max age 1 day, expecting only .txt or .log files
        anomalies = detector.detect_anomalies(
            "/staging",
            max_age_seconds=timedelta(days=1).total_seconds(),
            expected_patterns=[r".*\.txt$", r".*\.log$"]
        )

        self.assertEqual(len(anomalies), 2)
        # Check for old file anomaly
        self.assertIn("File '/staging/old_file.log' is", anomalies[0])
        self.assertIn("seconds old (>86400s). It's ancient!", anomalies[0])
        # Check for unexpected file anomaly
        self.assertIn("File '/staging/rogue.exe' does not match any expected pattern.", anomalies[1])

    def test_directory_with_subdir_skipped(self):
        self.mock_path_exists.return_value = True
        self.mock_is_directory.side_effect = lambda p: p == "/root_dir" or p == "/root_dir/subdir"
        self.mock_list_directory_contents.return_value = ["file.txt", "subdir"]

        # file.txt is recent
        self.mock_get_file_mtime.return_value = (self.mock_current_time - timedelta(hours=1)).timestamp()

        anomalies = detector.detect_anomalies("/root_dir", max_age_seconds=timedelta(days=1).total_seconds())
        self.assertEqual(len(anomalies), 0) # No anomalies, subdir is skipped

    def test_empty_directory_no_anomaly(self):
        self.mock_path_exists.return_value = True
        self.mock_is_directory.return_value = True
        self.mock_list_directory_contents.return_value = []

        anomalies = detector.detect_anomalies("/empty/dir", max_age_seconds=timedelta(days=1).total_seconds())
        self.assertEqual(len(anomalies), 0)

    def test_main_function_no_anomalies(self):
        # Mock argparse to simulate CLI arguments
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path="/path/to/recent_file.log",
            max_age_days=1.0,
            expect_pattern=None,
            verbose=False
        )):
            # Mock detect_anomalies to return no anomalies
            with patch('detector.detect_anomalies', return_value=[]):
                with patch('sys.exit') as mock_exit:
                    with patch('builtins.print') as mock_print:
                        detector.main()
                        mock_exit.assert_called_once_with(0)
                        mock_print.assert_called_once_with("No temporal anomalies detected.")

    def test_main_function_with_anomalies(self):
        # Mock argparse to simulate CLI arguments
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path="/path/to/old_file.log",
            max_age_days=1.0,
            expect_pattern=None,
            verbose=False
        )):
            # Mock detect_anomalies to return anomalies
            mock_anomalies = ["Temporal Anomaly: File '/path/to/old_file.log' is too old!"]
            with patch('detector.detect_anomalies', return_value=mock_anomalies):
                with patch('sys.exit') as mock_exit:
                    with patch('builtins.print') as mock_print:
                        detector.main()
                        mock_exit.assert_called_once_with(1)
                        # Check that print was called with the anomaly message
                        mock_print.assert_any_call("\n--- Temporal Anomalies Detected! ---")
                        mock_print.assert_any_call("- Temporal Anomaly: File '/path/to/old_file.log' is too old!")

    def test_main_function_verbose_no_anomalies(self):
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            path="/path/to/recent_file.log",
            max_age_days=1.0,
            expect_pattern=None,
            verbose=True
        )):
            with patch('detector.detect_anomalies', return_value=[]):
                with patch('sys.exit') as mock_exit:
                    with patch('builtins.print') as mock_print:
                        detector.main()
                        mock_exit.assert_called_once_with(0)
                        mock_print.assert_any_call("\n--- All clear. Spacetime continuum stable. ---")


if __name__ == '__main__':
    unittest.main()
