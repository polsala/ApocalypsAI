import unittest
from unittest.mock import patch, MagicMock
import datetime
import os

# Import the functions to be tested
from src.sweeper import is_dust_bunny, find_digital_dust_bunnies, generate_whimsical_suggestion

class TestDigitalDustBunnySweeper(unittest.TestCase):

    @patch('src.sweeper.datetime')
    @patch('src.sweeper.os.stat')
    def test_is_dust_bunny_positive(self, mock_os_stat, mock_datetime):
        # Mock rationale: Control current time and file stats to simulate an old, large file.
        mock_datetime.datetime.now.return_value = datetime.datetime(2024, 1, 1)
        mock_os_stat.return_value = MagicMock(st_mtime=datetime.datetime(2022, 1, 1).timestamp(), st_size=2 * 1024 * 1024) # 2MB

        filepath = '/path/to/old_large_file.txt'
        current_time = datetime.datetime(2024, 1, 1)
        age_days = 365 # 1 year
        min_size_bytes = 1 * 1024 * 1024 # 1MB

        self.assertTrue(is_dust_bunny(filepath, current_time, age_days, min_size_bytes))

    @patch('src.sweeper.datetime')
    @patch('src.sweeper.os.stat')
    def test_is_dust_bunny_too_recent(self, mock_os_stat, mock_datetime):
        # Mock rationale: Control current time and file stats to simulate a recent file.
        mock_datetime.datetime.now.return_value = datetime.datetime(2024, 1, 1)
        mock_os_stat.return_value = MagicMock(st_mtime=datetime.datetime(2023, 10, 1).timestamp(), st_size=2 * 1024 * 1024)

        filepath = '/path/to/recent_large_file.txt'
        current_time = datetime.datetime(2024, 1, 1)
        age_days = 365
        min_size_bytes = 1 * 1024 * 1024

        self.assertFalse(is_dust_bunny(filepath, current_time, age_days, min_size_bytes))

    @patch('src.sweeper.datetime')
    @patch('src.sweeper.os.stat')
    def test_is_dust_bunny_too_small(self, mock_os_stat, mock_datetime):
        # Mock rationale: Control current time and file stats to simulate an old, small file.
        mock_datetime.datetime.now.return_value = datetime.datetime(2024, 1, 1)
        mock_os_stat.return_value = MagicMock(st_mtime=datetime.datetime(2022, 1, 1).timestamp(), st_size=500 * 1024) # 500KB

        filepath = '/path/to/old_small_file.txt'
        current_time = datetime.datetime(2024, 1, 1)
        age_days = 365
        min_size_bytes = 1 * 1024 * 1024

        self.assertFalse(is_dust_bunny(filepath, current_time, age_days, min_size_bytes))

    @patch('src.sweeper.datetime')
    @patch('src.sweeper.os.stat', side_effect=OSError) # Simulate file not found
    def test_is_dust_bunny_file_error(self, mock_os_stat, mock_datetime):
        # Mock rationale: Simulate an OSError when trying to stat a file.
        mock_datetime.datetime.now.return_value = datetime.datetime(2024, 1, 1)

        filepath = '/path/to/non_existent_file.txt'
        current_time = datetime.datetime(2024, 1, 1)
        age_days = 365
        min_size_bytes = 1 * 1024 * 1024

        self.assertFalse(is_dust_bunny(filepath, current_time, age_days, min_size_bytes))

    @patch('src.sweeper.datetime')
    @patch('src.sweeper.os.path.isdir', return_value=True)
    @patch('src.sweeper.os.walk')
    @patch('src.sweeper.os.stat')
    def test_find_digital_dust_bunnies(self, mock_os_stat, mock_os_walk, mock_os_path_isdir, mock_datetime):
        # Mock rationale: Simulate a directory structure with files of varying age and size.
        # Control current time for age calculation.
        mock_datetime.datetime.now.return_value = datetime.datetime(2024, 1, 1)

        # Simulate directory structure
        mock_os_walk.return_value = [
            ('/test_dir', [], ['old_large.txt', 'recent_large.txt', 'old_small.txt', 'another_old_large.log'])
        ]

        # Simulate os.stat for each file
        def mock_stat_side_effect(path):
            if 'old_large.txt' in path:
                return MagicMock(st_mtime=datetime.datetime(2022, 1, 1).timestamp(), st_size=2 * 1024 * 1024) # Old, large
            elif 'recent_large.txt' in path:
                return MagicMock(st_mtime=datetime.datetime(2023, 10, 1).timestamp(), st_size=3 * 1024 * 1024) # Recent, large
            elif 'old_small.txt' in path:
                return MagicMock(st_mtime=datetime.datetime(2022, 1, 1).timestamp(), st_size=500 * 1024) # Old, small
            elif 'another_old_large.log' in path:
                return MagicMock(st_mtime=datetime.datetime(2021, 5, 1).timestamp(), st_size=1.5 * 1024 * 1024) # Very old, large
            raise FileNotFoundError # Should not happen with the above paths

        mock_os_stat.side_effect = mock_stat_side_effect

        target_path = '/test_dir'
        age_days = 365
        min_size_kb = 1024 # 1MB

        dust_bunnies = find_digital_dust_bunnies(target_path, age_days, min_size_kb)

        self.assertEqual(len(dust_bunnies), 2)
        self.assertIn('/test_dir/old_large.txt', [b['filepath'] for b in dust_bunnies])
        self.assertIn('/test_dir/another_old_large.log', [b['filepath'] for b in dust_bunnies])
        self.assertNotIn('/test_dir/recent_large.txt', [b['filepath'] for b in dust_bunnies])
        self.assertNotIn('/test_dir/old_small.txt', [b['filepath'] for b in dust_bunnies])

    def test_generate_whimsical_suggestion_determinism(self):
        # Mock rationale: Ensure the suggestion is deterministic for a given filepath.
        filepath1 = '/path/to/file1.txt'
        filepath2 = '/path/to/file2.txt'
        filepath1_again = '/path/to/file1.txt'

        # The actual datetime and size don't influence the suggestion choice in the current implementation
        # as it's based on hash(filepath) % len(suggestions).
        mock_mod_datetime = datetime.datetime(2022, 1, 1)
        mock_size_bytes = 1000000

        suggestion1 = generate_whimsical_suggestion(filepath1, mock_mod_datetime, mock_size_bytes)
        suggestion2 = generate_whimsical_suggestion(filepath2, mock_mod_datetime, mock_size_bytes)
        suggestion1_again = generate_whimsical_suggestion(filepath1_again, mock_mod_datetime, mock_size_bytes)

        self.assertEqual(suggestion1, suggestion1_again)
        self.assertNotEqual(suggestion1, suggestion2)

if __name__ == '__main__':
    unittest.main()
