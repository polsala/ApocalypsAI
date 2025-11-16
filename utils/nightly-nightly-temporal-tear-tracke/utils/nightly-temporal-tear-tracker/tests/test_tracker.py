import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the function to be tested
from src.tracker import scan_directory

class TestTemporalTearTracker(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.current_mock_time = datetime(2023, 10, 26, 10, 0, 0) # Fixed time for deterministic tests

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('datetime.datetime')
    def test_no_stale_files(self, mock_datetime, mock_walk, mock_getmtime):
        # Mock rationale: Fix current time for deterministic age calculation.
        mock_datetime.now.return_value = self.current_mock_time
        mock_datetime.fromtimestamp = datetime.fromtimestamp # Use real fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow datetime.datetime(Y,M,D) calls

        # Mock rationale: Simulate a directory structure without actual filesystem interaction.
        mock_walk.return_value = [
            (self.test_dir, [], ['file1.txt', 'file2.log'])
        ]

        # Mock rationale: Simulate recent modification times for all files.
        mock_getmtime.side_effect = {
            os.path.join(self.test_dir, 'file1.txt'): (self.current_mock_time - timedelta(days=10)).timestamp(),
            os.path.join(self.test_dir, 'file2.log'): (self.current_mock_time - timedelta(days=50)).timestamp(),
        }.get

        stale_files = scan_directory(self.test_dir, threshold_days=90)
        self.assertEqual(len(stale_files), 0, "Should find no stale files when all are recent.")

    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('datetime.datetime')
    def test_some_stale_files(self, mock_datetime, mock_walk, mock_getmtime):
        # Mock rationale: Fix current time for deterministic age calculation.
        mock_datetime.now.return_value = self.current_mock_time
        mock_datetime.fromtimestamp = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        # Mock rationale: Simulate a directory structure with mixed file ages.
        mock_walk.return_value = [
            (self.test_dir, ['subdir'], ['recent.txt', 'stale1.log']),
            (os.path.join(self.test_dir, 'subdir'), [], ['stale2.json', 'very_recent.py'])
        ]

        # Mock rationale: Simulate various modification times, some older than threshold.
        mock_getmtime.side_effect = {
            os.path.join(self.test_dir, 'recent.txt'): (self.current_mock_time - timedelta(days=30)).timestamp(),
            os.path.join(self.test_dir, 'stale1.log'): (self.current_mock_time - timedelta(days=100)).timestamp(),
            os.path.join(self.test_dir, 'subdir', 'stale2.json'): (self.current_mock_time - timedelta(days=120)).timestamp(),
            os.path.join(self.test_dir, 'subdir', 'very_recent.py'): (self.current_mock_time - timedelta(days=5)).timestamp(),
        }.get

        stale_files = scan_directory(self.test_dir, threshold_days=90)
        self.assertEqual(len(stale_files), 2, "Should find exactly two stale files.")

        # Check details of the first stale file
        stale1 = next(f for f in stale_files if 'stale1.log' in f['path'])
        self.assertEqual(stale1['path'], os.path.join(self.test_dir, 'stale1.log'))
        self.assertEqual(stale1['age_days'], 100)

        # Check details of the second stale file
        stale2 = next(f for f in stale_files if 'stale2.json' in f['path'])
        self.assertEqual(stale2['path'], os.path.join(self.test_dir, 'subdir', 'stale2.json'))
        self.assertEqual(stale2['age_days'], 120)

    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('datetime.datetime')
    def test_different_threshold(self, mock_datetime, mock_walk, mock_getmtime):
        # Mock rationale: Fix current time for deterministic age calculation.
        mock_datetime.now.return_value = self.current_mock_time
        mock_datetime.fromtimestamp = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        # Mock rationale: Simulate a directory structure.
        mock_walk.return_value = [
            (self.test_dir, [], ['file_60d.txt', 'file_120d.log'])
        ]

        # Mock rationale: Simulate modification times.
        mock_getmtime.side_effect = {
            os.path.join(self.test_dir, 'file_60d.txt'): (self.current_mock_time - timedelta(days=60)).timestamp(),
            os.path.join(self.test_dir, 'file_120d.log'): (self.current_mock_time - timedelta(days=120)).timestamp(),
        }.get

        # Test with threshold 70 days (only file_120d.log should be stale)
        stale_files_70 = scan_directory(self.test_dir, threshold_days=70)
        self.assertEqual(len(stale_files_70), 1, "Should find one stale file with 70-day threshold.")
        self.assertIn('file_120d.log', stale_files_70[0]['path'])

        # Test with threshold 130 days (no files should be stale)
        stale_files_130 = scan_directory(self.test_dir, threshold_days=130)
        self.assertEqual(len(stale_files_130), 0, "Should find no stale files with 130-day threshold.")

    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('datetime.datetime')
    def test_empty_directory(self, mock_datetime, mock_walk, mock_getmtime):
        # Mock rationale: Fix current time for deterministic age calculation.
        mock_datetime.now.return_value = self.current_mock_time
        mock_datetime.fromtimestamp = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        # Mock rationale: Simulate an empty directory.
        mock_walk.return_value = [
            (self.test_dir, [], [])
        ]

        stale_files = scan_directory(self.test_dir, threshold_days=90)
        self.assertEqual(len(stale_files), 0, "Should find no stale files in an empty directory.")

    @patch('os.path.isdir')
    def test_non_existent_directory(self, mock_isdir):
        # Mock rationale: Simulate a non-existent directory without actual filesystem interaction.
        mock_isdir.return_value = False

        with self.assertRaises(FileNotFoundError, msg="Should raise FileNotFoundError for non-existent path."):
            scan_directory('/non/existent/path', threshold_days=90)

    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('datetime.datetime')
    def test_file_inaccessibility(self, mock_datetime, mock_walk, mock_getmtime):
        # Mock rationale: Fix current time for deterministic age calculation.
        mock_datetime.now.return_value = self.current_mock_time
        mock_datetime.fromtimestamp = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        # Mock rationale: Simulate a directory structure.
        mock_walk.return_value = [
            (self.test_dir, [], ['accessible.txt', 'inaccessible.txt'])
        ]

        # Mock rationale: Simulate an OSError for one file, and a stale time for another.
        def mock_getmtime_side_effect(path):
            if 'inaccessible.txt' in path:
                raise OSError("Permission denied")
            return (self.current_mock_time - timedelta(days=100)).timestamp()

        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Mock rationale: Capture print output to check for warning messages.
        with patch('builtins.print') as mock_print:
            stale_files = scan_directory(self.test_dir, threshold_days=90)
            self.assertEqual(len(stale_files), 1, "Should find one stale file, skipping the inaccessible one.")
            self.assertIn('accessible.txt', stale_files[0]['path'])
            mock_print.assert_called_with(unittest.mock.ANY) # Check if print was called
            self.assertIn("Warning: Could not access file", mock_print.call_args[0][0])

if __name__ == '__main__':
    unittest.main()
