import unittest
from unittest.mock import patch, MagicMock
import datetime
import os

# Import the functions to be tested
from src.dust_bunny_sweeper import find_dust_bunnies, format_size, get_file_info

class TestDustBunnySweeper(unittest.TestCase):

    @patch('datetime.datetime')
    def test_find_dust_bunnies_no_bunnies(self, mock_dt):
        # Mock rationale: Control the current time for age calculation.
        mock_dt.now.return_value = datetime.datetime(2023, 10, 26)
        mock_dt.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
        mock_dt.timedelta = datetime.timedelta

        # Mock rationale: Simulate a file system with no old files.
        mock_os_walk_return = [
            ('/mock_repo', [], ['file_recent.txt', 'another_recent.log'])
        ]
        with patch('os.walk', return_value=mock_os_walk_return),
             patch('os.path.isdir', return_value=True),
             patch('os.stat') as mock_os_stat:

            # Mock rationale: Provide stat info for files, making them recent.
            mock_os_stat.return_value = MagicMock(st_mtime=datetime.datetime(2023, 10, 20).timestamp(), st_size=100)

            bunnies = find_dust_bunnies('/mock_repo', 30)
            self.assertEqual(len(bunnies), 0)

    @patch('datetime.datetime')
    def test_find_dust_bunnies_with_bunnies(self, mock_dt):
        # Mock rationale: Control the current time for age calculation.
        mock_dt.now.return_value = datetime.datetime(2023, 10, 26)
        mock_dt.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
        mock_dt.timedelta = datetime.timedelta

        # Mock rationale: Simulate a file system with old and recent files.
        mock_os_walk_return = [
            ('/mock_repo', ['sub_dir'], ['recent.txt', 'old_file.log']),
            ('/mock_repo/sub_dir', [], ['very_old.tmp'])
        ]
        with patch('os.walk', return_value=mock_os_walk_return),
             patch('os.path.isdir', return_value=True),
             patch('os.stat') as mock_os_stat:

            # Mock rationale: Provide specific stat info for each file.
            def mock_stat_side_effect(path):
                if 'recent.txt' in path:
                    return MagicMock(st_mtime=datetime.datetime(2023, 10, 25).timestamp(), st_size=100)
                elif 'old_file.log' in path:
                    return MagicMock(st_mtime=datetime.datetime(2023, 9, 1).timestamp(), st_size=5000)
                elif 'very_old.tmp' in path:
                    return MagicMock(st_mtime=datetime.datetime(2023, 8, 15).timestamp(), st_size=100000)
                raise FileNotFoundError # Should not happen with our mock walk

            mock_os_stat.side_effect = mock_stat_side_effect

            bunnies = find_dust_bunnies('/mock_repo', 30)
            self.assertEqual(len(bunnies), 2)

            # Verify the found bunnies
            found_paths = {b[0] for b in bunnies}
            self.assertIn(os.path.join('/mock_repo', 'old_file.log'), found_paths)
            self.assertIn(os.path.join('/mock_repo/sub_dir', 'very_old.tmp'), found_paths)

            # Check details for one bunny
            old_log_bunny = next(b for b in bunnies if 'old_file.log' in b[0])
            self.assertGreaterEqual(old_log_bunny[1], 55) # 2023-10-26 - 2023-09-01 = 55 days
            self.assertEqual(old_log_bunny[2], 5000)

    @patch('datetime.datetime')
    def test_find_dust_bunnies_invalid_path(self, mock_dt):
        # Mock rationale: Control the current time for age calculation.
        mock_dt.now.return_value = datetime.datetime(2023, 10, 26)
        mock_dt.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
        mock_dt.timedelta = datetime.timedelta

        # Mock rationale: Simulate an invalid directory path.
        with patch('os.path.isdir', return_value=False),
             patch('builtins.print') as mock_print:
            bunnies = find_dust_bunnies('/non_existent_repo', 30)
            self.assertEqual(len(bunnies), 0)
            mock_print.assert_called_with("Error: Path '/non_existent_repo' is not a valid directory.")

    def test_format_size(self):
        self.assertEqual(format_size(0), "0 B")
        self.assertEqual(format_size(500), "500 B")
        self.assertEqual(format_size(1024), "1.0 KB")
        self.assertEqual(format_size(1536), "1.5 KB")
        self.assertEqual(format_size(1024 * 1024), "1.0 MB")
        self.assertEqual(format_size(1.5 * 1024 * 1024), "1.5 MB")
        self.assertEqual(format_size(1024 * 1024 * 1024), "1.0 GB")

    @patch('os.stat')
    def test_get_file_info_success(self, mock_os_stat):
        # Mock rationale: Simulate successful os.stat call.
        mock_stat_result = MagicMock(st_mtime=1678886400.0, st_size=12345)
        mock_os_stat.return_value = mock_stat_result

        mtime, size = get_file_info('/mock/file.txt')
        self.assertEqual(mtime, 1678886400.0)
        self.assertEqual(size, 12345)
        mock_os_stat.assert_called_once_with('/mock/file.txt')

    @patch('os.stat', side_effect=OSError)
    def test_get_file_info_os_error(self, mock_os_stat):
        # Mock rationale: Simulate an OSError during os.stat (e.g., file not found, permissions).
        mtime, size = get_file_info('/nonexistent/file.txt')
        self.assertIsNone(mtime)
        self.assertIsNone(size)
        mock_os_stat.assert_called_once_with('/nonexistent/file.txt')

if __name__ == '__main__':
    unittest.main()
