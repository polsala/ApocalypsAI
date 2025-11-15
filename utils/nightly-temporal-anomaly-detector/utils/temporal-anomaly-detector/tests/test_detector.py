import unittest
from unittest.mock import patch, MagicMock
import datetime
import time
import os
import json

# Assuming detector.py is in src/
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from detector import find_temporal_anomalies

class TestTemporalAnomalyDetector(unittest.TestCase):

    def setUp(self):
        self.base_path = "/mock/scan/path"
        self.current_time = time.time()
        self.current_datetime = datetime.datetime.fromtimestamp(self.current_time)

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getctime')
    def test_no_anomalies(self, mock_getctime, mock_getmtime, mock_walk):
        # Mock rationale: Simulate a directory with normal files.
        # No anomalies should be detected.
        mock_walk.return_value = [
            (self.base_path, [], ["file1.txt", "file2.log"])
        ]
        
        # All files have modification and creation times in the recent past
        mock_getmtime.side_effect = [
            self.current_time - (1 * 24 * 3600), # file1.txt modified 1 day ago
            self.current_time - (2 * 24 * 3600)  # file2.log modified 2 days ago
        ]
        mock_getctime.side_effect = [
            self.current_time - (10 * 24 * 3600), # file1.txt created 10 days ago
            self.current_time - (20 * 24 * 3600)  # file2.log created 20 days ago
        ]

        results = find_temporal_anomalies(self.base_path)
        self.assertEqual(len(results["future_anomalies"]), 0)
        self.assertEqual(len(results["past_modified_anomalies"]), 0)

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getctime')
    def test_future_anomaly(self, mock_getctime, mock_getmtime, mock_walk):
        # Mock rationale: Simulate a file with a modification time in the future.
        # This should be detected as a future anomaly.
        mock_walk.return_value = [
            (self.base_path, [], ["future_file.txt"])
        ]
        
        future_mtime = self.current_time + (2 * 24 * 3600) # 2 days in the future
        mock_getmtime.return_value = future_mtime
        mock_getctime.return_value = self.current_time - (10 * 24 * 3600) # Normal creation time

        results = find_temporal_anomalies(self.base_path, future_threshold_days=1)
        self.assertEqual(len(results["future_anomalies"]), 1)
        self.assertEqual(results["future_anomalies"][0]["path"], os.path.join(self.base_path, "future_file.txt"))
        self.assertIn("days in the future", results["future_anomalies"][0]["reason"])
        self.assertEqual(len(results["past_modified_anomalies"]), 0)

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getctime')
    def test_past_modified_anomaly(self, mock_getctime, mock_getmtime, mock_walk):
        # Mock rationale: Simulate an old file (created long ago) that was recently modified.
        # This should be detected as a past_modified anomaly.
        mock_walk.return_value = [
            (self.base_path, [], ["old_but_new.log"])
        ]
        
        old_ctime = self.current_time - (400 * 24 * 3600) # Created 400 days ago
        recent_mtime = self.current_time - (3 * 24 * 3600) # Modified 3 days ago
        
        mock_getmtime.return_value = recent_mtime
        mock_getctime.return_value = old_ctime

        results = find_temporal_anomalies(
            self.base_path,
            past_modified_threshold_days=365, # Files older than 365 days by ctime
            recent_modification_window_days=7 # Modified within last 7 days
        )
        self.assertEqual(len(results["future_anomalies"]), 0)
        self.assertEqual(len(results["past_modified_anomalies"]), 1)
        self.assertEqual(results["past_modified_anomalies"][0]["path"], os.path.join(self.base_path, "old_but_new.log"))
        self.assertIn("File created over 365 days ago, but modified within the last 7 days.", results["past_modified_anomalies"][0]["reason"])

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getctime')
    def test_multiple_anomalies(self, mock_getctime, mock_getmtime, mock_walk):
        # Mock rationale: Simulate a scenario with both future and past_modified anomalies.
        # Both types should be detected.
        mock_walk.return_value = [
            (self.base_path, [], ["future.txt", "old_recent.log", "normal.py"])
        ]

        # Define times for each file
        future_mtime = self.current_time + (2 * 24 * 3600)
        old_ctime = self.current_time - (500 * 24 * 3600)
        recent_mtime_for_old = self.current_time - (5 * 24 * 3600)
        normal_mtime = self.current_time - (10 * 24 * 3600)
        normal_ctime = self.current_time - (20 * 24 * 3600)

        mock_getmtime.side_effect = [
            future_mtime,         # future.txt
            recent_mtime_for_old, # old_recent.log
            normal_mtime          # normal.py
        ]
        mock_getctime.side_effect = [
            self.current_time - (10 * 24 * 3600), # future.txt ctime
            old_ctime,                            # old_recent.log ctime
            normal_ctime                          # normal.py ctime
        ]

        results = find_temporal_anomalies(
            self.base_path,
            future_threshold_days=1,
            past_modified_threshold_days=365,
            recent_modification_window_days=7
        )

        self.assertEqual(len(results["future_anomalies"]), 1)
        self.assertEqual(results["future_anomalies"][0]["path"], os.path.join(self.base_path, "future.txt"))
        
        self.assertEqual(len(results["past_modified_anomalies"]), 1)
        self.assertEqual(results["past_modified_anomalies"][0]["path"], os.path.join(self.base_path, "old_recent.log"))

    @patch('os.walk')
    @patch('os.path.getmtime')
    @patch('os.path.getctime')
    def test_os_error_handling(self, mock_getctime, mock_getmtime, mock_walk):
        # Mock rationale: Simulate an OSError (e.g., permission denied, file deleted) during file access.
        # The detector should handle it gracefully and continue, not crash.
        mock_walk.return_value = [
            (self.base_path, [], ["accessible.txt", "inaccessible.txt"])
        ]

        # accessible.txt is normal
        # inaccessible.txt raises OSError
        mock_getmtime.side_effect = [
            self.current_time - (1 * 24 * 3600), # accessible.txt
            OSError("Permission denied")          # inaccessible.txt
        ]
        mock_getctime.side_effect = [
            self.current_time - (10 * 24 * 3600), # accessible.txt
            OSError("Permission denied")          # inaccessible.txt
        ]

        # Redirect stdout to capture the warning message
        with patch('sys.stdout', new_callable=MagicMock) as mock_stdout:
            results = find_temporal_anomalies(self.base_path)
            self.assertEqual(len(results["future_anomalies"]), 0)
            self.assertEqual(len(results["past_modified_anomalies"]), 0)
            mock_stdout.write.assert_called_with(f"Warning: Could not access {os.path.join(self.base_path, 'inaccessible.txt')}: Permission denied\n")
