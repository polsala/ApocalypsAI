import unittest
import os
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import time # For simulating file modification times

# Mock rationale: We don't want tests to actually create/delete/move files on the filesystem.
# Mocking os.walk, os.path.isdir, os.path.getmtime, os.makedirs, and shutil.move
# allows us to simulate file system interactions deterministically and offline.

# Import the class to be tested
from src.sweeper import DigitalDebrisSweeper

class TestDigitalDebrisSweeper(unittest.TestCase):

    def setUp(self):
        # Common patterns for tests
        self.patterns = ["*.log", "*.tmp", "*~"]
        self.quarantine_dir = "/mock/quarantine"

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_debris_no_debris(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with no debris files.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/project', [], ['main.py', 'config.json', 'data.csv'])
        ]
        mock_getmtime.return_value = time.time() # Current time, doesn't matter for this test

        sweeper = DigitalDebrisSweeper(self.patterns)
        debris = sweeper.find_debris(['/mock/project'])
        self.assertEqual(len(debris), 0)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_debris_with_debris(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory with some debris files.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            ('/mock/project', [], ['main.py', 'error.log', 'temp.tmp', 'backup.py~', 'data.csv'])
        ]
        mock_getmtime.return_value = time.time() # Current time, doesn't matter for this test

        sweeper = DigitalDebrisSweeper(self.patterns)
        debris = sweeper.find_debris(['/mock/project'])
        self.assertEqual(len(debris), 3)
        self.assertIn('/mock/project/error.log', debris)
        self.assertIn('/mock/project/temp.tmp', debris)
        self.assertIn('/mock/project/backup.py~', debris)
        self.assertNotIn('/mock/project/main.py', debris)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_debris_with_age_filter(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate files with different modification times to test age filtering.
        mock_isdir.return_value = True
        
        # Simulate current time for comparison
        now = datetime.now()
        
        # File modified 10 days ago (should be considered debris if age_days=7)
        old_file_timestamp = (now - timedelta(days=10)).timestamp()
        # File modified 5 days ago (should NOT be considered debris if age_days=7)
        recent_file_timestamp = (now - timedelta(days=5)).timestamp()

        # Mock getmtime to return specific timestamps for specific files
        def mock_getmtime_side_effect(path):
            if 'old_log.log' in path:
                return old_file_timestamp
            elif 'recent_log.log' in path:
                return recent_file_timestamp
            return now.timestamp() # Default for other files

        mock_getmtime.side_effect = mock_getmtime_side_effect

        mock_walk.return_value = [
            ('/mock/project', [], ['old_log.log', 'recent_log.log', 'main.py'])
        ]

        # Test with age_days = 7
        sweeper = DigitalDebrisSweeper(self.patterns, age_days=7)
        debris = sweeper.find_debris(['/mock/project'])
        self.assertEqual(len(debris), 1)
        self.assertIn('/mock/project/old_log.log', debris)
        self.assertNotIn('/mock/project/recent_log.log', debris)

        # Test with age_days = 0 (age filter disabled)
        sweeper_no_age = DigitalDebrisSweeper(self.patterns, age_days=0)
        debris_no_age = sweeper_no_age.find_debris(['/mock/project'])
        self.assertEqual(len(debris_no_age), 2) # Both logs should be found
        self.assertIn('/mock/project/old_log.log', debris_no_age)
        self.assertIn('/mock/project/recent_log.log', debris_no_age)

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_debris_non_existent_scan_dir(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a non-existent scan directory.
        mock_isdir.side_effect = lambda x: x == '/mock/existing_project' # Only one dir exists
        mock_walk.return_value = [
            ('/mock/existing_project', [], ['file.log'])
        ]
        mock_getmtime.return_value = time.time()

        sweeper = DigitalDebrisSweeper(self.patterns)
        debris = sweeper.find_debris(['/mock/non_existent', '/mock/existing_project'])
        self.assertEqual(len(debris), 1)
        self.assertIn('/mock/existing_project/file.log', debris)

    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists')
    def test_quarantine_debris_success(self, mock_exists, mock_move, mock_makedirs):
        # Mock rationale: Simulate successful quarantining of files.
        # os.path.exists is mocked to prevent collision logic from triggering initially.
        mock_exists.return_value = False 
        
        debris_files = ['/mock/project/error.log', '/mock/project/temp.tmp']
        sweeper = DigitalDebrisSweeper(self.patterns, self.quarantine_dir)
        
        quarantined_count = sweeper.quarantine_debris(debris_files)
        
        self.assertEqual(quarantined_count, 2)
        mock_makedirs.assert_called_once_with(self.quarantine_dir, exist_ok=True)
        mock_move.assert_any_call('/mock/project/error.log', '/mock/quarantine/error.log')
        mock_move.assert_any_call('/mock/project/temp.tmp', '/mock/quarantine/temp.tmp')
        self.assertEqual(mock_move.call_count, 2)

    @patch('os.makedirs')
    @patch('shutil.move')
    @patch('os.path.exists')
    def test_quarantine_debris_with_collision(self, mock_exists, mock_move, mock_makedirs):
        # Mock rationale: Simulate a file collision in the quarantine directory.
        # The first call to exists for 'file.log' should be True, then False for 'file_1.log'.
        mock_exists.side_effect = [True, False] 
        
        debris_files = ['/mock/project/file.log']
        sweeper = DigitalDebrisSweeper(self.patterns, self.quarantine_dir)
        
        quarantined_count = sweeper.quarantine_debris(debris_files)
        
        self.assertEqual(quarantined_count, 1)
        mock_makedirs.assert_called_once_with(self.quarantine_dir, exist_ok=True)
        # Expect move to the renamed path
        mock_move.assert_called_once_with('/mock/project/file.log', '/mock/quarantine/file_1.log')

    @patch('os.makedirs')
    @patch('shutil.move')
    def test_quarantine_debris_no_quarantine_dir(self, mock_move, mock_makedirs):
        # Mock rationale: Test the error handling when quarantine_dir is not provided.
        sweeper = DigitalDebrisSweeper(self.patterns) # No quarantine_dir
        debris_files = ['/mock/project/error.log']
        
        with self.assertRaises(ValueError) as cm:
            sweeper.quarantine_debris(debris_files)
        self.assertIn("Quarantine directory must be specified", str(cm.exception))
        mock_makedirs.assert_not_called()
        mock_move.assert_not_called()

    @patch('os.makedirs')
    @patch('shutil.move', side_effect=OSError("Permission denied"))
    @patch('os.path.exists', return_value=False)
    def test_quarantine_debris_move_failure(self, mock_exists, mock_move, mock_makedirs):
        # Mock rationale: Simulate a failure during the move operation (e.g., permission error).
        debris_files = ['/mock/project/error.log']
        sweeper = DigitalDebrisSweeper(self.patterns, self.quarantine_dir)
        
        # The method should catch the exception and print an error, but still return a count.
        # Since the move failed, the count should be 0 for successful moves.
        quarantined_count = sweeper.quarantine_debris(debris_files)
        
        self.assertEqual(quarantined_count, 0)
        mock_makedirs.assert_called_once()
        mock_move.assert_called_once()

if __name__ == '__main__':
    unittest.main()
