import unittest
import os
import datetime
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Assume detector.py is in src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from detector import scan_for_anomalies, main

class TestTemporalAnomalyDetector(unittest.TestCase):

    @patch('detector.datetime')
    @patch('detector.os.walk')
    @patch('detector.os.path.isdir')
    @patch('detector.os.path.getmtime')
    def test_no_anomalies(self, mock_getmtime, mock_isdir, mock_os_walk, mock_datetime):
        # Mock rationale: Simulate current time for deterministic age calculations.
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 26, 12, 0, 0)
        # Mock rationale: Simulate file modification times.
        # All files are within the normal range (e.g., 10 days old, 100 seconds old).
        mock_getmtime.side_effect = [
            (datetime.datetime(2023, 10, 16, 12, 0, 0)).timestamp(), # file1.txt (10 days old)
            (datetime.datetime(2023, 10, 26, 11, 58, 20)).timestamp() # file2.txt (100 seconds old)
        ]
        # Mock rationale: Simulate directory existence.
        mock_isdir.return_value = True
        # Mock rationale: Simulate directory contents.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.txt'])
        ]

        # Max age: 30 days, Min age: 5 seconds
        anomalies = scan_for_anomalies('/test_dir', max_age_days=30, min_age_seconds=5)

        self.assertEqual(len(anomalies["too_old"]), 0)
        self.assertEqual(len(anomalies["too_new"]), 0)

    @patch('detector.datetime')
    @patch('detector.os.walk')
    @patch('detector.os.path.isdir')
    @patch('detector.os.path.getmtime')
    def test_too_old_anomaly(self, mock_getmtime, mock_isdir, mock_os_walk, mock_datetime):
        # Mock rationale: Simulate current time.
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 26, 12, 0, 0)
        # Mock rationale: Simulate file modification times.
        # file1.txt is 40 days old (too old for max_age_days=30).
        mock_getmtime.side_effect = [
            (datetime.datetime(2023, 9, 16, 12, 0, 0)).timestamp(), # file1.txt (40 days old)
            (datetime.datetime(2023, 10, 26, 11, 58, 20)).timestamp() # file2.txt (100 seconds old, normal)
        ]
        # Mock rationale: Simulate directory existence.
        mock_isdir.return_value = True
        # Mock rationale: Simulate directory contents.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.txt'])
        ]

        anomalies = scan_for_anomalies('/test_dir', max_age_days=30, min_age_seconds=5)

        self.assertEqual(len(anomalies["too_old"]), 1)
        self.assertIn('/test_dir/file1.txt', anomalies["too_old"][0])
        self.assertEqual(len(anomalies["too_new"]), 0)

    @patch('detector.datetime')
    @patch('detector.os.walk')
    @patch('detector.os.path.isdir')
    @patch('detector.os.path.getmtime')
    def test_too_new_anomaly(self, mock_getmtime, mock_isdir, mock_os_walk, mock_datetime):
        # Mock rationale: Simulate current time.
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 26, 12, 0, 0)
        # Mock rationale: Simulate file modification times.
        # file1.txt is 10 days old (normal).
        # file2.txt is 3 seconds old (too new for min_age_seconds=5).
        mock_getmtime.side_effect = [
            (datetime.datetime(2023, 10, 16, 12, 0, 0)).timestamp(), # file1.txt (10 days old, normal)
            (datetime.datetime(2023, 10, 26, 11, 59, 57)).timestamp() # file2.txt (3 seconds old)
        ]
        # Mock rationale: Simulate directory existence.
        mock_isdir.return_value = True
        # Mock rationale: Simulate directory contents.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.txt'])
        ]

        anomalies = scan_for_anomalies('/test_dir', max_age_days=30, min_age_seconds=5)

        self.assertEqual(len(anomalies["too_old"]), 0)
        self.assertEqual(len(anomalies["too_new"]), 1)
        self.assertIn('/test_dir/file2.txt', anomalies["too_new"][0])

    @patch('detector.datetime')
    @patch('detector.os.walk')
    @patch('detector.os.path.isdir')
    @patch('detector.os.path.getmtime')
    def test_both_anomalies(self, mock_getmtime, mock_isdir, mock_os_walk, mock_datetime):
        # Mock rationale: Simulate current time.
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 26, 12, 0, 0)
        # Mock rationale: Simulate file modification times.
        # file_old.txt is 40 days old.
        # file_new.txt is 3 seconds old.
        # file_normal.txt is 10 days old.
        mock_getmtime.side_effect = [
            (datetime.datetime(2023, 9, 16, 12, 0, 0)).timestamp(), # file_old.txt (40 days old)
            (datetime.datetime(2023, 10, 26, 11, 59, 57)).timestamp(), # file_new.txt (3 seconds old)
            (datetime.datetime(2023, 10, 16, 12, 0, 0)).timestamp() # file_normal.txt (10 days old)
        ]
        # Mock rationale: Simulate directory existence.
        mock_isdir.return_value = True
        # Mock rationale: Simulate directory contents.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['file_old.txt', 'file_new.txt', 'file_normal.txt'])
        ]

        anomalies = scan_for_anomalies('/test_dir', max_age_days=30, min_age_seconds=5)

        self.assertEqual(len(anomalies["too_old"]), 1)
        self.assertIn('/test_dir/file_old.txt', anomalies["too_old"][0])
        self.assertEqual(len(anomalies["too_new"]), 1)
        self.assertIn('/test_dir/file_new.txt', anomalies["too_new"][0])

    @patch('detector.os.path.isdir')
    def test_directory_not_found(self, mock_isdir):
        # Mock rationale: Simulate a non-existent directory.
        mock_isdir.return_value = False
        
        anomalies = scan_for_anomalies('/non_existent_dir', max_age_days=30, min_age_seconds=5)
        self.assertEqual(len(anomalies["too_old"]), 0)
        self.assertEqual(len(anomalies["too_new"]), 0)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    @patch('detector.scan_for_anomalies')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_anomalies_exit_0(self, mock_parse_args, mock_scan, mock_exit, mock_stdout):
        # Mock rationale: Simulate command-line arguments.
        mock_parse_args.return_value = MagicMock(
            directory='/test_dir',
            max_age_days=30,
            min_age_seconds=5
        )
        # Mock rationale: Simulate scan_for_anomalies returning no anomalies.
        mock_scan.return_value = {"too_old": [], "too_new": []}

        main()
        mock_exit.assert_called_once_with(0)
        self.assertIn("No temporal anomalies detected. All clear!", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    @patch('detector.scan_for_anomalies')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_anomalies_exit_1(self, mock_parse_args, mock_scan, mock_exit, mock_stdout):
        # Mock rationale: Simulate command-line arguments.
        mock_parse_args.return_value = MagicMock(
            directory='/test_dir',
            max_age_days=30,
            min_age_seconds=5
        )
        # Mock rationale: Simulate scan_for_anomalies returning anomalies.
        mock_scan.return_value = {
            "too_old": ["/test_dir/old_file.txt (Modified: 2023-09-16T12:00:00)"],
            "too_new": []
        }

        main()
        mock_exit.assert_called_once_with(1)
        self.assertIn("Temporal Anomalies Detected!", mock_stdout.getvalue())
        self.assertIn("Files that are suspiciously old:", mock_stdout.getvalue())
        self.assertIn("- /test_dir/old_file.txt", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
