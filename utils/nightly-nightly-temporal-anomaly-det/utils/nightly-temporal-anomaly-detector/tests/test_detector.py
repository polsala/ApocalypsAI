import unittest
import os
import time
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Import the function to be tested
from src.detector import find_temporal_anomalies

class TestTemporalAnomalyDetector(unittest.TestCase):

    @patch('src.detector.datetime')
    @patch('src.detector.os.path.getmtime')
    @patch('src.detector.os.walk')
    def test_no_anomalies(self, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Simulate current time for consistent testing.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow datetime constructor

        # Mock rationale: Simulate a directory with normal files.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log'])
        ]

        # Mock rationale: Simulate modification times within normal range.
        # file1.txt: 1 year ago
        # file2.log: 2 years ago
        normal_timestamp_1 = (datetime(2022, 10, 26, 12, 0, 0)).timestamp()
        normal_timestamp_2 = (datetime(2021, 10, 26, 12, 0, 0)).timestamp()
        mock_getmtime.side_effect = [normal_timestamp_1, normal_timestamp_2]

        anomalies = find_temporal_anomalies('/test_dir', max_age_years=5, future_tolerance_seconds=60)

        self.assertEqual(len(anomalies["future_files"]), 0)
        self.assertEqual(len(anomalies["ancient_files"]), 0)

    @patch('src.detector.datetime')
    @patch('src.detector.os.path.getmtime')
    @patch('src.detector.os.walk')
    def test_future_files_detected(self, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Simulate current time for consistent testing.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        # Mock rationale: Simulate a directory with a future file.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['future_file.txt'])
        ]

        # Mock rationale: Simulate a modification time in the future (e.g., 2 minutes from now).
        future_timestamp = (datetime(2023, 10, 26, 12, 2, 0)).timestamp()
        mock_getmtime.return_value = future_timestamp

        anomalies = find_temporal_anomalies('/test_dir', max_age_years=5, future_tolerance_seconds=60)

        self.assertEqual(len(anomalies["future_files"]), 1)
        self.assertEqual(anomalies["future_files"][0]["path"], os.path.join('/test_dir', 'future_file.txt'))
        self.assertIn("minutes in the future", anomalies["future_files"][0]["reason"])
        self.assertEqual(len(anomalies["ancient_files"]), 0)

    @patch('src.detector.datetime')
    @patch('src.detector.os.path.getmtime')
    @patch('src.detector.os.walk')
    def test_ancient_files_detected(self, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Simulate current time for consistent testing.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        # Mock rationale: Simulate a directory with an ancient file.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['ancient_report.pdf'])
        ]

        # Mock rationale: Simulate a modification time far in the past (e.g., 10 years ago).
        ancient_timestamp = (datetime(2013, 10, 26, 12, 0, 0)).timestamp()
        mock_getmtime.return_value = ancient_timestamp

        anomalies = find_temporal_anomalies('/test_dir', max_age_years=5, future_tolerance_seconds=60)

        self.assertEqual(len(anomalies["ancient_files"]), 1)
        self.assertEqual(anomalies["ancient_files"][0]["path"], os.path.join('/test_dir', 'ancient_report.pdf'))
        self.assertIn("5 years ago or more", anomalies["ancient_files"][0]["reason"])
        self.assertEqual(len(anomalies["future_files"]), 0)

    @patch('src.detector.datetime')
    @patch('src.detector.os.path.getmtime')
    @patch('src.detector.os.walk')
    def test_mixed_anomalies(self, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Simulate current time for consistent testing.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        # Mock rationale: Simulate a directory with mixed files.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['future.txt', 'normal.log', 'ancient.pdf'])
        ]

        # Mock rationale: Simulate modification times for mixed files.
        future_timestamp = (datetime(2023, 10, 26, 12, 3, 0)).timestamp() # 3 mins in future
        normal_timestamp = (datetime(2023, 1, 1, 0, 0, 0)).timestamp()    # Recent past
        ancient_timestamp = (datetime(2010, 5, 1, 0, 0, 0)).timestamp()   # Very old
        mock_getmtime.side_effect = [future_timestamp, normal_timestamp, ancient_timestamp]

        anomalies = find_temporal_anomalies('/test_dir', max_age_years=5, future_tolerance_seconds=60)

        self.assertEqual(len(anomalies["future_files"]), 1)
        self.assertEqual(anomalies["future_files"][0]["path"], os.path.join('/test_dir', 'future.txt'))
        self.assertEqual(len(anomalies["ancient_files"]), 1)
        self.assertEqual(anomalies["ancient_files"][0]["path"], os.path.join('/test_dir', 'ancient.pdf'))

    @patch('src.detector.datetime')
    @patch('src.detector.os.path.getmtime')
    @patch('src.detector.os.walk')
    def test_empty_directory(self, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Simulate current time for consistent testing.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        # Mock rationale: Simulate an empty directory.
        mock_os_walk.return_value = [
            ('/empty_dir', [], [])
        ]
        mock_getmtime.side_effect = [] # No files, so getmtime won't be called

        anomalies = find_temporal_anomalies('/empty_dir', max_age_years=5, future_tolerance_seconds=60)

        self.assertEqual(len(anomalies["future_files"]), 0)
        self.assertEqual(len(anomalies["ancient_files"]), 0)

    @patch('src.detector.datetime')
    @patch('src.detector.os.path.getmtime')
    @patch('src.detector.os.walk')
    def test_os_error_handling(self, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Simulate current time for consistent testing.
        mock_datetime.now.return_value = datetime(2023, 10, 26, 12, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        # Mock rationale: Simulate a directory with one inaccessible file.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['inaccessible.txt', 'normal.txt'])
        ]

        # Mock rationale: getmtime raises OSError for 'inaccessible.txt', then returns normal for 'normal.txt'.
        normal_timestamp = (datetime(2023, 1, 1, 0, 0, 0)).timestamp()
        mock_getmtime.side_effect = [OSError("Permission denied"), normal_timestamp]

        # Mock rationale: Capture print output to ensure warning is printed.
        with patch('builtins.print') as mock_print:
            anomalies = find_temporal_anomalies('/test_dir', max_age_years=5, future_tolerance_seconds=60)
            mock_print.assert_called_with(unittest.mock.ANY) # Check if print was called
            self.assertIn("Warning: Could not access", mock_print.call_args_list[0].args[0])

        self.assertEqual(len(anomalies["future_files"]), 0)
        self.assertEqual(len(anomalies["ancient_files"]), 0)


if __name__ == '__main__':
    unittest.main()
