import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the function to be tested
from src.collector import find_dust_bunnies

class TestDigitalDustBunnyCollector(unittest.TestCase):

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_basic(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a directory structure and file modification times
        # without touching the actual filesystem, ensuring deterministic tests.
        mock_isdir.return_value = True
        
        # Simulate current time for consistent age calculation
        mock_now = datetime(2024, 1, 1)
        
        # Define mock file system structure and modification times
        # Files:
        #   - old_file.txt: modified 100 days ago (dust bunny)
        #   - recent_file.py: modified 10 days ago (not a dust bunny)
        #   - another_old.log: modified 120 days ago (dust bunny, but will be excluded by extension)
        #   - sub/very_old.doc: modified 200 days ago (dust bunny)
        #   - sub/recent_sub.txt: modified 5 days ago (not a dust bunny)
        # Directories:
        #   - .git/: should be excluded
        #   - node_modules/: should be excluded
        
        root_path = "/mock/scan/path"
        
        # Mock os.walk to return a predefined directory structure
        mock_walk.return_value = [
            (root_path, ["sub", ".git", "node_modules"], ["old_file.txt", "recent_file.py", "another_old.log"]),
            (os.path.join(root_path, "sub"), [], ["very_old.doc", "recent_sub.txt"]),
            (os.path.join(root_path, ".git"), [], ["HEAD"]), # Should be ignored
            (os.path.join(root_path, "node_modules"), [], ["package.json"]), # Should be ignored
        ]

        # Mock os.path.getmtime for specific files
        # Use a helper to calculate timestamps relative to mock_now
        def get_timestamp_from_days_ago(days_ago):
            return (mock_now - timedelta(days=days_ago)).timestamp()

        # Map file paths to their mock modification timestamps
        mock_mtimes = {
            os.path.join(root_path, "old_file.txt"): get_timestamp_from_days_ago(100),
            os.path.join(root_path, "recent_file.py"): get_timestamp_from_days_ago(10),
            os.path.join(root_path, "another_old.log"): get_timestamp_from_days_ago(120),
            os.path.join(root_path, "sub", "very_old.doc"): get_timestamp_from_days_ago(200),
            os.path.join(root_path, "sub", "recent_sub.txt"): get_timestamp_from_days_ago(5),
            os.path.join(root_path, ".git", "HEAD"): get_timestamp_from_days_ago(300),
            os.path.join(root_path, "node_modules", "package.json"): get_timestamp_from_days_ago(300),
        }
        mock_getmtime.side_effect = lambda p: mock_mtimes.get(p, time.time()) # Default to current if not mocked

        # Patch datetime.now() to control the "current" time
        with patch('src.collector.datetime') as mock_dt:
            # Mock rationale: Fix the current time to ensure age calculations are deterministic.
            mock_dt.now.return_value = mock_now
            mock_dt.fromtimestamp.side_effect = datetime.fromtimestamp # Keep original behavior for conversion
            mock_dt.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs) # Allow datetime constructor
            mock_dt.timedelta = timedelta # Allow timedelta

            # Test with default min_age_days (90)
            dust_bunnies = find_dust_bunnies(root_path)
            
            expected_bunnies = [
                (os.path.join(root_path, "old_file.txt"), datetime.fromtimestamp(get_timestamp_from_days_ago(100))),
                (os.path.join(root_path, "sub", "very_old.doc"), datetime.fromtimestamp(get_timestamp_from_days_ago(200))),
            ]
            
            # Sort for consistent comparison
            self.assertEqual(sorted(dust_bunnies), sorted(expected_bunnies))

            # Test with custom min_age_days (150)
            dust_bunnies_150 = find_dust_bunnies(root_path, min_age_days=150)
            expected_bunnies_150 = [
                (os.path.join(root_path, "sub", "very_old.doc"), datetime.fromtimestamp(get_timestamp_from_days_ago(200))),
            ]
            self.assertEqual(sorted(dust_bunnies_150), sorted(expected_bunnies_150))

            # Test with exclude_extensions
            dust_bunnies_exclude_ext = find_dust_bunnies(root_path, exclude_extensions=['.log', '.doc'])
            expected_bunnies_exclude_ext = [
                (os.path.join(root_path, "old_file.txt"), datetime.fromtimestamp(get_timestamp_from_days_ago(100))),
            ]
            self.assertEqual(sorted(dust_bunnies_exclude_ext), sorted(expected_bunnies_exclude_ext))

            # Test with exclude_dirs
            dust_bunnies_exclude_dir = find_dust_bunnies(root_path, exclude_dirs=['.git', 'sub'])
            expected_bunnies_exclude_dir = [
                (os.path.join(root_path, "old_file.txt"), datetime.fromtimestamp(get_timestamp_from_days_ago(100))),
            ]
            self.assertEqual(sorted(dust_bunnies_exclude_dir), sorted(expected_bunnies_exclude_dir))

            # Test with all exclusions combined
            dust_bunnies_all_excluded = find_dust_bunnies(
                root_path,
                min_age_days=90,
                exclude_extensions=['.log', '.doc'],
                exclude_dirs=['.git', 'sub', 'node_modules']
            )
            expected_bunnies_all_excluded = [
                (os.path.join(root_path, "old_file.txt"), datetime.fromtimestamp(get_timestamp_from_days_ago(100))),
            ]
            self.assertEqual(sorted(dust_bunnies_all_excluded), sorted(expected_bunnies_all_excluded))

            # Test with no dust bunnies
            mock_walk.return_value = [
                (root_path, [], ["recent_file.py"]),
            ]
            mock_mtimes = {
                os.path.join(root_path, "recent_file.py"): get_timestamp_from_days_ago(10),
            }
            dust_bunnies_none = find_dust_bunnies(root_path)
            self.assertEqual(dust_bunnies_none, [])

    @patch('os.path.isdir')
    def test_find_dust_bunnies_invalid_path(self, mock_isdir):
        # Mock rationale: Simulate an invalid path without actual filesystem interaction.
        mock_isdir.return_value = False
        dust_bunnies = find_dust_bunnies("/non/existent/path")
        self.assertEqual(dust_bunnies, [])

    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_find_dust_bunnies_os_error(self, mock_getmtime, mock_walk, mock_isdir):
        # Mock rationale: Simulate a file becoming inaccessible during scan,
        # ensuring the utility handles errors gracefully and continues.
        mock_isdir.return_value = True
        mock_now = datetime(2024, 1, 1)
        
        root_path = "/mock/scan/path"
        mock_walk.return_value = [
            (root_path, [], ["file1.txt", "file2.txt"]),
        ]

        # file1.txt is old and accessible
        # file2.txt is old but raises an OSError when trying to get mtime
        def get_timestamp_from_days_ago(days_ago):
            return (mock_now - timedelta(days=days_ago)).timestamp()

        def mock_getmtime_side_effect(path):
            if path == os.path.join(root_path, "file1.txt"):
                return get_timestamp_from_days_ago(100)
            elif path == os.path.join(root_path, "file2.txt"):
                raise OSError("Permission denied")
            return time.time()

        mock_getmtime.side_effect = mock_getmtime_side_effect

        with patch('src.collector.datetime') as mock_dt:
            mock_dt.now.return_value = mock_now
            mock_dt.fromtimestamp.side_effect = datetime.fromtimestamp
            mock_dt.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
            mock_dt.timedelta = timedelta

            dust_bunnies = find_dust_bunnies(root_path, min_age_days=90)
            expected_bunnies = [
                (os.path.join(root_path, "file1.txt"), datetime.fromtimestamp(get_timestamp_from_days_ago(100))),
            ]
            self.assertEqual(sorted(dust_bunnies), sorted(expected_bunnies))


if __name__ == '__main__':
    unittest.main()
