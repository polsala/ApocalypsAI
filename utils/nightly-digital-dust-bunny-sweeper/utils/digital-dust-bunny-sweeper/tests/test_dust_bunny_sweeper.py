import unittest
from unittest.mock import patch, MagicMock
import os
import time
import sys

# Mock rationale: We need to simulate file system interactions (os.walk, os.path.getmtime,
# os.path.isdir) and the current time (time.time()) without actually touching the disk
# or relying on the system's clock. This ensures deterministic and offline tests.

# Adjust sys.path to allow importing from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from dust_bunny_sweeper import find_dust_bunnies
sys.path.pop(0)

class TestDustBunnySweeper(unittest.TestCase):

    # Define a fixed current time for testing purposes
    MOCK_CURRENT_TIME = time.mktime((2023, 10, 27, 10, 0, 0, 0, 0, 0)) # Oct 27, 2023

    @patch('time.time', MagicMock(return_value=MOCK_CURRENT_TIME))
    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_no_dust_bunnies_found(self, mock_os_walk, mock_getmtime, mock_isdir):
        # Mock rationale: Simulate a directory with only recent files.
        mock_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/path', [], ['recent_file.txt'])
        ]
        # Set modification time to be very recent (e.g., 1 day ago)
        mock_getmtime.return_value = self.MOCK_CURRENT_TIME - (1 * 24 * 60 * 60)

        result = find_dust_bunnies('/mock/path', 90)
        self.assertEqual(result, [])

    @patch('time.time', MagicMock(return_value=MOCK_CURRENT_TIME))
    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_dust_bunnies_found(self, mock_os_walk, mock_getmtime, mock_isdir):
        # Mock rationale: Simulate a directory with old files that should be identified.
        mock_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/path', ['old_dir'], ['old_file.txt', 'recent_file.txt']),
            ('/mock/path/old_dir', [], ['another_old_file.log'])
        ]

        def getmtime_side_effect(path):
            if 'old_file.txt' in path or 'old_dir' in path or 'another_old_file.log' in path:
                # Old: 100 days ago
                return self.MOCK_CURRENT_TIME - (100 * 24 * 60 * 60)
            elif 'recent_file.txt' in path:
                # Recent: 1 day ago
                return self.MOCK_CURRENT_TIME - (1 * 24 * 60 * 60)
            return self.MOCK_CURRENT_TIME # Default for other paths

        mock_getmtime.side_effect = getmtime_side_effect

        result = find_dust_bunnies('/mock/path', 90)
        expected_bunnies = [
            '/mock/path/old_file.txt',
            '/mock/path/old_dir',
            '/mock/path/old_dir/another_old_file.log'
        ]
        # Sort for consistent comparison
        self.assertEqual(sorted(result), sorted(expected_bunnies))

    @patch('time.time', MagicMock(return_value=MOCK_CURRENT_TIME))
    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_ignore_patterns(self, mock_os_walk, mock_getmtime, mock_isdir):
        # Mock rationale: Simulate a directory with old files, some of which should be ignored.
        mock_isdir.return_value = True
        # The mock_os_walk returns the full structure, and the function's internal logic
        # (modifying 'dirs' in-place and checking 'name' against ignore patterns) should filter it.
        mock_os_walk.return_value = [
            ('/mock/path', ['node_modules', 'old_dir'], ['old_file.txt', 'ignored.log', 'recent_file.txt']),
            ('/mock/path/node_modules', [], ['package.json']),
            ('/mock/path/old_dir', [], ['another_old_file.log'])
        ]

        def getmtime_side_effect(path):
            # All files/dirs are old enough to be dust bunnies by default
            return self.MOCK_CURRENT_TIME - (100 * 24 * 60 * 60)

        mock_getmtime.side_effect = getmtime_side_effect

        ignore_patterns = ['node_modules', '*.log']
        result = find_dust_bunnies('/mock/path', 90, ignore_patterns)

        expected_bunnies = [
            '/mock/path/old_file.txt',
            '/mock/path/old_dir'
        ]
        # '/mock/path/ignored.log' and '/mock/path/node_modules' and its contents should be ignored
        self.assertEqual(sorted(result), sorted(expected_bunnies))

    @patch('time.time', MagicMock(return_value=MOCK_CURRENT_TIME))
    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_invalid_path(self, mock_os_walk, mock_getmtime, mock_isdir):
        # Mock rationale: Test behavior when the provided path is not a directory.
        mock_isdir.return_value = False
        result = find_dust_bunnies('/non/existent/path', 90)
        self.assertEqual(result, [])
        mock_os_walk.assert_not_called() # os.walk should not be called if path is invalid

    @patch('time.time', MagicMock(return_value=MOCK_CURRENT_TIME))
    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_empty_directory(self, mock_os_walk, mock_getmtime, mock_isdir):
        # Mock rationale: Simulate an empty directory.
        mock_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/empty_path', [], [])
        ]
        result = find_dust_bunnies('/mock/empty_path', 90)
        self.assertEqual(result, [])

    @patch('time.time', MagicMock(return_value=MOCK_CURRENT_TIME))
    @patch('os.path.isdir')
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_os_error_during_getmtime(self, mock_os_walk, mock_getmtime, mock_isdir):
        # Mock rationale: Simulate a scenario where os.path.getmtime raises an OSError
        # (e.g., due to permissions or file deletion during scan).
        mock_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/path', [], ['good_file.txt', 'bad_file.txt'])
        ]

        def getmtime_side_effect(path):
            if 'bad_file.txt' in path:
                raise OSError("Permission denied")
            # Old file, should be a dust bunny if not for the error
            return self.MOCK_CURRENT_TIME - (100 * 24 * 60 * 60)

        mock_getmtime.side_effect = getmtime_side_effect

        result = find_dust_bunnies('/mock/path', 90)
        # Only 'good_file.txt' should be found, 'bad_file.txt' should be skipped due to error
        expected_bunnies = [
            '/mock/path/good_file.txt'
        ]
        self.assertEqual(result, expected_bunnies)


if __name__ == '__main__':
    unittest.main()
