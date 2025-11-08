import unittest
import os
import time
from unittest.mock import patch, MagicMock
from src.detector import scan_directory_for_anomalies, format_timestamp, main

class TestTemporalAnomalyDetector(unittest.TestCase):

    def setUp(self):
        # Define some base timestamps for deterministic testing
        self.base_time = 1672531200.0  # Jan 1, 2023 00:00:00 UTC
        self.one_day = 86400
        self.one_hour = 3600

    @patch('os.walk')
    @patch('os.stat')
    def test_no_anomalies(self, mock_stat, mock_walk):
        # Mock rationale: Simulate a file system with no anomalies.
        # os.walk provides directory structure, os.stat provides file metadata.
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log']),
            ('/test_dir/subdir', [], ['subfile.json'])
        ]

        # Mock rationale: All files have mtime and ctime within the threshold.
        # mtime and ctime are close to each other.
        def stat_side_effect(path):
            mock_stat_obj = MagicMock()
            if 'file1.txt' in path:
                mock_stat_obj.st_mtime = self.base_time + 100
                mock_stat_obj.st_ctime = self.base_time + 105
            elif 'file2.log' in path:
                mock_stat_obj.st_mtime = self.base_time + 200
                mock_stat_obj.st_ctime = self.base_time + 200
            elif 'subfile.json' in path:
                mock_stat_obj.st_mtime = self.base_time + 300
                mock_stat_obj.st_ctime = self.base_time + 301
            else:
                raise FileNotFoundError
            return mock_stat_obj

        mock_stat.side_effect = stat_side_effect

        anomalies = scan_directory_for_anomalies('/test_dir', threshold_seconds=self.one_day)
        self.assertEqual(len(anomalies), 0)

    @patch('os.walk')
    @patch('os.stat')
    def test_large_positive_difference_anomaly(self, mock_stat, mock_walk):
        # Mock rationale: Simulate a file modified much later than its metadata.
        mock_walk.return_value = [
            ('/test_dir', [], ['anomaly_file.txt'])
        ]

        def stat_side_effect(path):
            mock_stat_obj = MagicMock()
            if 'anomaly_file.txt' in path:
                mock_stat_obj.st_mtime = self.base_time + self.one_day * 2 # 2 days later
                mock_stat_obj.st_ctime = self.base_time # Original ctime
            else:
                raise FileNotFoundError
            return mock_stat_obj

        mock_stat.side_effect = stat_side_effect

        anomalies = scan_directory_for_anomalies('/test_dir', threshold_seconds=self.one_day)
        self.assertEqual(len(anomalies), 1)
        self.assertIn('anomaly_file.txt', anomalies[0]['path'])
        self.assertAlmostEqual(anomalies[0]['diff'], self.one_day * 2)
        self.assertEqual(anomalies[0]['type'], 'mtime significantly newer than ctime')

    @patch('os.walk')
    @patch('os.stat')
    def test_mtime_older_than_ctime_anomaly(self, mock_stat, mock_walk):
        # Mock rationale: Simulate a file where mtime is significantly older than ctime.
        # This often indicates a file restored from an old backup.
        mock_walk.return_value = [
            ('/test_dir', [], ['old_mtime_file.txt'])
        ]

        def stat_side_effect(path):
            mock_stat_obj = MagicMock()
            if 'old_mtime_file.txt' in path:
                mock_stat_obj.st_mtime = self.base_time # Original mtime
                mock_stat_obj.st_ctime = self.base_time + self.one_day * 2 # ctime updated later
            else:
                raise FileNotFoundError
            return mock_stat_obj

        mock_stat.side_effect = stat_side_effect

        anomalies = scan_directory_for_anomalies('/test_dir', threshold_seconds=self.one_day)
        self.assertEqual(len(anomalies), 1)
        self.assertIn('old_mtime_file.txt', anomalies[0]['path'])
        self.assertAlmostEqual(anomalies[0]['diff'], -self.one_day * 2)
        self.assertEqual(anomalies[0]['type'], 'mtime significantly older than ctime')

    @patch('os.walk')
    @patch('os.stat')
    def test_mtime_older_than_ctime_within_threshold(self, mock_stat, mock_walk):
        # Mock rationale: Simulate a file where mtime is slightly older than ctime,
        # but the absolute difference is within the threshold. This should still be flagged
        # by the specific "mtime older than ctime" rule.
        mock_walk.return_value = [
            ('/test_dir', [], ['subtle_warp.txt'])
        ]

        def stat_side_effect(path):
            mock_stat_obj = MagicMock()
            if 'subtle_warp.txt' in path:
                mock_stat_obj.st_mtime = self.base_time + self.one_hour # mtime
                mock_stat_obj.st_ctime = self.base_time + self.one_hour + 1000 # ctime 1000s later
            else:
                raise FileNotFoundError
            return mock_stat_obj

        mock_stat.side_effect = stat_side_effect

        anomalies = scan_directory_for_anomalies('/test_dir', threshold_seconds=self.one_day) # Threshold is 24h
        self.assertEqual(len(anomalies), 1)
        self.assertIn('subtle_warp.txt', anomalies[0]['path'])
        self.assertAlmostEqual(anomalies[0]['diff'], -1000.0)
        self.assertEqual(anomalies[0]['type'], 'mtime older than ctime (potential time warp)')


    @patch('os.walk')
    @patch('os.stat')
    def test_empty_directory(self, mock_stat, mock_walk):
        # Mock rationale: Simulate an empty directory.
        mock_walk.return_value = [
            ('/empty_dir', [], [])
        ]
        anomalies = scan_directory_for_anomalies('/empty_dir')
        self.assertEqual(len(anomalies), 0)
        mock_stat.assert_not_called() # No files to stat

    @patch('os.walk')
    @patch('os.stat')
    def test_permission_error_file(self, mock_stat, mock_walk):
        # Mock rationale: Simulate a file that cannot be stat'd due to permissions.
        mock_walk.return_value = [
            ('/test_dir', [], ['unreadable.txt', 'readable.txt'])
        ]

        def stat_side_effect(path):
            if 'unreadable.txt' in path:
                raise OSError("Permission denied")
            elif 'readable.txt' in path:
                mock_stat_obj = MagicMock()
                mock_stat_obj.st_mtime = self.base_time + 100
                mock_stat_obj.st_ctime = self.base_time + 100
                return mock_stat_obj
            else:
                raise FileNotFoundError
        mock_stat.side_effect = stat_side_effect

        anomalies = scan_directory_for_anomalies('/test_dir')
        self.assertEqual(len(anomalies), 0) # Unreadable file is skipped, readable is fine.

    def test_format_timestamp(self):
        # Mock rationale: Test timestamp formatting.
        self.assertEqual(format_timestamp(self.base_time), '2023-01-01 00:00:00')
        self.assertEqual(format_timestamp(None), 'N/A')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.detector.scan_directory_for_anomalies')
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_no_anomalies(self, mock_exit, mock_print, mock_isdir, mock_scan_dir, mock_parse_args):
        # Mock rationale: Test main function when no anomalies are found.
        mock_parse_args.return_value = MagicMock(path='/test_dir', threshold_seconds=self.one_day)
        mock_scan_dir.return_value = [] # No anomalies

        main()

        mock_print.assert_any_call("Scanning '/test_dir' for temporal anomalies with a threshold of 86400 seconds...")
        mock_print.assert_any_call("\nNo temporal anomalies detected. All clear!")
        mock_exit.assert_called_once_with(2) # Exit code 2 for no-op

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.detector.scan_directory_for_anomalies')
    @patch('os.path.isdir', return_value=True)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_with_anomalies(self, mock_exit, mock_print, mock_isdir, mock_scan_dir, mock_parse_args):
        # Mock rationale: Test main function when anomalies are found.
        mock_parse_args.return_value = MagicMock(path='/test_dir', threshold_seconds=self.one_day)
        mock_scan_dir.return_value = [{
            "path": "/test_dir/anomaly.txt",
            "mtime": self.base_time,
            "ctime": self.base_time + self.one_day * 2,
            "diff": -self.one_day * 2,
            "type": "mtime significantly older than ctime"
        }]

        main()

        mock_print.assert_any_call("\n--- Detected Temporal Anomalies ---")
        mock_print.assert_any_call(f"[ANOMALY] /test_dir/anomaly.txt: mtime=2023-01-01 00:00:00, ctime=2023-01-03 00:00:00, Diff={-self.one_day * 2:.1f}s (mtime significantly older than ctime)")
        mock_exit.assert_called_once_with(0) # Exit code 0 for success (anomalies found)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_exit, mock_print, mock_isdir, mock_parse_args):
        # Mock rationale: Test main function with an invalid path.
        mock_parse_args.return_value = MagicMock(path='/non_existent_dir', threshold_seconds=self.one_day)

        main()

        mock_print.assert_any_call("Error: Path '/non_existent_dir' is not a valid directory.")
        mock_exit.assert_called_once_with(1) # Exit code 1 for failure

if __name__ == '__main__':
    unittest.main()
