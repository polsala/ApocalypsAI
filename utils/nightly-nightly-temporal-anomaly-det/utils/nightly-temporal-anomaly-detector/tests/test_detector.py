import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone

# Add the src directory to the path to allow importing detector.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from detector import find_temporal_anomalies, main

class TestTemporalAnomalyDetector(unittest.TestCase):

    def setUp(self):
        # Mock current time for deterministic tests
        self.mock_now = datetime(2024, 7, 20, 10, 0, 0, tzinfo=timezone.utc)
        self.patcher_now = patch('detector.datetime', wraps=datetime)
        self.mock_datetime = self.patcher_now.start()
        # Ensure datetime.now() returns the mocked time, especially when called with tz=timezone.utc
        self.mock_datetime.now.side_effect = lambda tz=None: self.mock_now if tz == timezone.utc else datetime.now(tz)

    def tearDown(self):
        self.patcher_now.stop()

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_no_anomalies(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with normal files to ensure no anomalies are reported.
        # os.path.isdir: To confirm the target directory exists.
        # os.walk: To simulate directory structure and files.
        # os.path.getmtime: To provide modification times for files.
        
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log'])
        ]
        
        # Files modified slightly in the past, well within normal limits
        normal_mtime_1 = (self.mock_now - timedelta(days=10)).timestamp()
        normal_mtime_2 = (self.mock_now - timedelta(hours=5)).timestamp()
        mock_getmtime.side_effect = [normal_mtime_1, normal_mtime_2]

        anomalies = find_temporal_anomalies('/test_dir')
        self.assertEqual(len(anomalies), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_future_modification_time(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a file with a modification time in the future.
        # os.path.isdir, os.walk, os.path.getmtime: As above.
        
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['future_file.txt'])
        ]
        
        future_mtime = (self.mock_now + timedelta(minutes=10)).timestamp()
        mock_getmtime.return_value = future_mtime

        anomalies = find_temporal_anomalies('/test_dir', future_threshold_seconds=5)
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['type'], 'FUTURE_MODIFICATION_TIME')
        self.assertEqual(anomalies[0]['file'], '/test_dir/future_file.txt')
        self.assertIn('future', anomalies[0]['details'])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_ancient_modification_time(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a file with a modification time significantly in the past.
        # os.path.isdir, os.walk, os.path.getmtime: As above.
        
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['ancient_file.doc'])
        ]
        
        ancient_mtime = datetime(1975, 1, 1, tzinfo=timezone.utc).timestamp()
        mock_getmtime.return_value = ancient_mtime

        anomalies = find_temporal_anomalies('/test_dir', ancient_year=1980)
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['type'], 'ANCIENT_MODIFICATION_TIME')
        self.assertEqual(anomalies[0]['file'], '/test_dir/ancient_file.doc')
        self.assertIn('before 1980', anomalies[0]['details'])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_mixed_anomalies(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with both future and ancient files.
        # os.path.isdir, os.walk, os.path.getmtime: As above.
        
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['future.txt', 'normal.log', 'ancient.bak'])
        ]
        
        future_mtime = (self.mock_now + timedelta(days=1)).timestamp()
        normal_mtime = (self.mock_now - timedelta(days=5)).timestamp()
        ancient_mtime = datetime(1960, 1, 1, tzinfo=timezone.utc).timestamp()
        
        mock_getmtime.side_effect = [future_mtime, normal_mtime, ancient_mtime]

        anomalies = find_temporal_anomalies('/test_dir', ancient_year=1980)
        self.assertEqual(len(anomalies), 2)
        anomaly_types = sorted([a['type'] for a in anomalies])
        self.assertEqual(anomaly_types, ['ANCIENT_MODIFICATION_TIME', 'FUTURE_MODIFICATION_TIME'])

    @patch('os.path.isdir')
    def test_directory_not_found(self, mock_isdir):
        # Mock rationale: Simulate a non-existent directory.
        # os.path.isdir: To return False, indicating the directory doesn't exist.
        
        mock_isdir.return_value = False
        anomalies = find_temporal_anomalies('/non_existent_dir')
        self.assertEqual(len(anomalies), 0) 

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_os_error_on_getmtime(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate an OSError when trying to get a file's modification time.
        # os.path.isdir, os.walk: As above.
        # os.path.getmtime: To raise an OSError.
        
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', [], ['unreadable_file.txt'])
        ]
        mock_getmtime.side_effect = OSError("Permission denied")

        anomalies = find_temporal_anomalies('/test_dir')
        self.assertEqual(len(anomalies), 1)
        self.assertEqual(anomalies[0]['type'], 'ACCESS_ERROR')
        self.assertIn('Permission denied', anomalies[0]['details'])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_recursive_scan(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Test that the utility correctly scans subdirectories by mocking os.walk.
        # os.path.isdir, os.walk, os.path.getmtime: As above.
        
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', ['subdir1'], ['file_root.txt']),
            ('/test_dir/subdir1', [], ['file_subdir.txt'])
        ]
        
        future_mtime = (self.mock_now + timedelta(days=1)).timestamp()
        ancient_mtime = datetime(1970, 1, 1, tzinfo=timezone.utc).timestamp()
        
        mock_getmtime.side_effect = [future_mtime, ancient_mtime] # Order matters for side_effect

        anomalies = find_temporal_anomalies('/test_dir', recursive=True)
        self.assertEqual(len(anomalies), 2)
        self.assertIn('/test_dir/file_root.txt', [a['file'] for a in anomalies])
        self.assertIn('/test_dir/subdir1/file_subdir.txt', [a['file'] for a in anomalies])
        
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_non_recursive_scan(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Test that the utility only scans the top-level directory when recursive=False.
        # os.path.isdir, os.walk, os.path.getmtime: As above.
        
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/test_dir', ['subdir1'], ['file_root.txt']),
            ('/test_dir/subdir1', [], ['file_subdir.txt'])
        ]
        
        future_mtime = (self.mock_now + timedelta(days=1)).timestamp()
        # ancient_mtime = datetime(1970, 1, 1, tzinfo=timezone.utc).timestamp()
        
        mock_getmtime.side_effect = [future_mtime] # Only root file will be checked

        anomalies = find_temporal_anomalies('/test_dir', recursive=False)
        self.assertEqual(len(anomalies), 1)
        self.assertIn('/test_dir/file_root.txt', [a['file'] for a in anomalies])
        self.assertNotIn('/test_dir/subdir1/file_subdir.txt', [a['file'] for a in anomalies])

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('detector.find_temporal_anomalies')
    def test_main_no_anomalies(self, mock_find_anomalies, mock_exit, mock_stdout):
        # Mock rationale: Test the main function's behavior when no anomalies are found.
        # sys.stdout: To capture printed output.
        # sys.exit: To prevent actual program exit and check exit code.
        # detector.find_temporal_anomalies: To control the return value of the core logic.
        
        mock_find_anomalies.return_value = []
        
        # Mock argparse to simulate command line arguments
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            directory_path='/test_dir',
            future_threshold=5,
            ancient_year=1980,
            no_recursive=False
        )):
            main()
            mock_find_anomalies.assert_called_once_with('/test_dir', 5, 1980, True)
            mock_exit.assert_called_once_with(0)
            mock_stdout.write.assert_any_call("No temporal anomalies detected in '/test_dir'. All clear!\n")

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('detector.find_temporal_anomalies')
    def test_main_with_anomalies(self, mock_find_anomalies, mock_exit, mock_stdout):
        # Mock rationale: Test the main function's behavior when anomalies are found.
        # sys.stdout, sys.exit, detector.find_temporal_anomalies: As above.
        
        mock_find_anomalies.return_value = [
            {
                "file": "/test_dir/future.txt",
                "type": "FUTURE_MODIFICATION_TIME",
                "mtime": "2024-07-21T10:00:00+00:00",
                "current_time": "2024-07-20T10:00:00+00:00",
                "details": "Modified 2024-07-21T10:00:00+00:00 (future)"
            }
        ]
        
        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(
            directory_path='/test_dir',
            future_threshold=5,
            ancient_year=1980,
            no_recursive=False
        )):
            main()
            mock_find_anomalies.assert_called_once_with('/test_dir', 5, 1980, True)
            mock_exit.assert_called_once_with(1)
            mock_stdout.write.assert_any_call("Temporal Anomalies Detected:\n")
            mock_stdout.write.assert_any_call("- File: /test_dir/future.txt\n")

if __name__ == '__main__':
    unittest.main()
