import unittest
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the functions from the duster module
from src.duster import find_old_files, clean_debris, get_file_age_in_days

class TestDataDebrisDuster(unittest.TestCase):

    # Mock rationale: We need a fixed point in time for 'now' to ensure
    # deterministic age calculations for files, regardless of when the test runs.
    MOCK_NOW = datetime(2023, 10, 26, 12, 0, 0)

    @patch('src.duster.datetime')
    def test_get_file_age_in_days(self, mock_datetime):
        mock_datetime.now.return_value = self.MOCK_NOW
        mock_datetime.fromtimestamp = datetime.fromtimestamp # Use real fromtimestamp

        # Mock rationale: We need to simulate a file's modification time without
        # actually creating a file, to ensure tests are fast and don't touch the filesystem.
        mock_path = MagicMock(spec=Path)
        mock_stat = MagicMock()
        
        # File modified 100 days ago
        old_timestamp = (self.MOCK_NOW - timedelta(days=100)).timestamp()
        mock_stat.st_mtime = old_timestamp
        mock_path.stat.return_value = mock_stat
        mock_path.is_file.return_value = True

        age = get_file_age_in_days(mock_path)
        self.assertAlmostEqual(age, 100.0, places=5)

        # File modified 50 days ago
        recent_timestamp = (self.MOCK_NOW - timedelta(days=50)).timestamp()
        mock_stat.st_mtime = recent_timestamp
        mock_path.stat.return_value = mock_stat
        
        age = get_file_age_in_days(mock_path)
        self.assertAlmostEqual(age, 50.0, places=5)

        # Mock rationale: Simulate a FileNotFoundError without actual file system interaction.
        mock_path.stat.side_effect = FileNotFoundError
        age = get_file_age_in_days(mock_path)
        self.assertEqual(age, -1)


    @patch('src.duster.datetime')
    @patch('src.duster.os.walk')
    @patch('src.duster.Path.is_dir')
    @patch('src.duster.Path.is_file')
    @patch('src.duster.Path.stat')
    def test_find_old_files_non_recursive(self, mock_stat, mock_is_file, mock_is_dir, mock_os_walk, mock_datetime):
        mock_datetime.now.return_value = self.MOCK_NOW
        mock_datetime.fromtimestamp = datetime.fromtimestamp

        mock_is_dir.return_value = True
        mock_is_file.return_value = True

        # Mock rationale: Simulate directory structure and file modification times
        # without creating actual files, for deterministic and isolated testing.
        # File 1: old (100 days)
        # File 2: recent (50 days)
        # File 3: old (120 days)
        
        # Mock os.walk to return a single directory with files
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['old_file_1.txt', 'recent_file.log', 'old_file_2.tmp'])
        ]

        # Mock stat for each file
        def mock_stat_side_effect(path_obj):
            mock_s = MagicMock()
            if 'old_file_1.txt' in str(path_obj):
                mock_s.st_mtime = (self.MOCK_NOW - timedelta(days=100)).timestamp()
            elif 'recent_file.log' in str(path_obj):
                mock_s.st_mtime = (self.MOCK_NOW - timedelta(days=50)).timestamp()
            elif 'old_file_2.tmp' in str(path_obj):
                mock_s.st_mtime = (self.MOCK_NOW - timedelta(days=120)).timestamp()
            else:
                raise FileNotFoundError
            return mock_s
        mock_stat.side_effect = mock_stat_side_effect

        target_dir = Path('/mock/dir')
        
        # Test with age threshold 90 days
        old_files = find_old_files(target_dir, 90, recursive=False)
        self.assertEqual(len(old_files), 2)
        self.assertIn(Path('/mock/dir/old_file_1.txt'), old_files)
        self.assertIn(Path('/mock/dir/old_file_2.tmp'), old_files)
        self.assertNotIn(Path('/mock/dir/recent_file.log'), old_files)

        # Test with age threshold 110 days
        old_files = find_old_files(target_dir, 110, recursive=False)
        self.assertEqual(len(old_files), 1)
        self.assertIn(Path('/mock/dir/old_file_2.tmp'), old_files)
        self.assertNotIn(Path('/mock/dir/old_file_1.txt'), old_files)


    @patch('src.duster.datetime')
    @patch('src.duster.os.walk')
    @patch('src.duster.Path.is_dir')
    @patch('src.duster.Path.is_file')
    @patch('src.duster.Path.stat')
    def test_find_old_files_recursive(self, mock_stat, mock_is_file, mock_is_dir, mock_os_walk, mock_datetime):
        mock_datetime.now.return_value = self.MOCK_NOW
        mock_datetime.fromtimestamp = datetime.fromtimestamp

        mock_is_dir.return_value = True
        mock_is_file.return_value = True

        # Mock rationale: Simulate a deeper directory structure for recursive scanning
        # without actual filesystem interaction.
        mock_os_walk.return_value = [
            ('/mock/dir', ['subdir1'], ['old_file_1.txt', 'recent_file.log']),
            ('/mock/dir/subdir1', [], ['old_file_2.tmp', 'recent_file_2.txt'])
        ]

        def mock_stat_side_effect(path_obj):
            mock_s = MagicMock()
            if 'old_file_1.txt' in str(path_obj):
                mock_s.st_mtime = (self.MOCK_NOW - timedelta(days=100)).timestamp()
            elif 'recent_file.log' in str(path_obj):
                mock_s.st_mtime = (self.MOCK_NOW - timedelta(days=50)).timestamp()
            elif 'old_file_2.tmp' in str(path_obj):
                mock_s.st_mtime = (self.MOCK_NOW - timedelta(days=120)).timestamp()
            elif 'recent_file_2.txt' in str(path_obj):
                mock_s.st_mtime = (self.MOCK_NOW - timedelta(days=60)).timestamp()
            else:
                raise FileNotFoundError
            return mock_s
        mock_stat.side_effect = mock_stat_side_effect

        target_dir = Path('/mock/dir')
        
        old_files = find_old_files(target_dir, 90, recursive=True)
        self.assertEqual(len(old_files), 2)
        self.assertIn(Path('/mock/dir/old_file_1.txt'), old_files)
        self.assertIn(Path('/mock/dir/subdir1/old_file_2.tmp'), old_files)
        self.assertNotIn(Path('/mock/dir/recent_file.log'), old_files)
        self.assertNotIn(Path('/mock/dir/subdir1/recent_file_2.txt'), old_files)


    @patch('src.duster.datetime')
    @patch('src.duster.os.walk')
    @patch('src.duster.Path.is_dir')
    @patch('src.duster.Path.is_file')
    @patch('src.duster.Path.stat')
    @patch('src.duster.os.remove')
    @patch('builtins.print') # Mock print to suppress output during tests
    def test_clean_debris_dry_run(self, mock_print, mock_os_remove, mock_stat, mock_is_file, mock_is_dir, mock_os_walk, mock_datetime):
        mock_datetime.now.return_value = self.MOCK_NOW
        mock_datetime.fromtimestamp = datetime.fromtimestamp

        mock_is_dir.return_value = True
        mock_is_file.return_value = True

        # Mock rationale: Simulate files that would be found by find_old_files
        # without actually creating them.
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['old_file_1.txt', 'recent_file.log'])
        ]

        def mock_stat_side_effect(path_obj):
            mock_s = MagicMock()
            if 'old_file_1.txt' in str(path_obj):
                mock_s.st_mtime = (self.MOCK_NOW - timedelta(days=100)).timestamp()
            elif 'recent_file.log' in str(path_obj):
                mock_s.st_mtime = (self.MOCK_NOW - timedelta(days=50)).timestamp()
            else:
                raise FileNotFoundError
            return mock_s
        mock_stat.side_effect = mock_stat_side_effect

        target_dir = Path('/mock/dir')
        
        processed_files = clean_debris(target_dir, 90, dry_run=True)
        
        self.assertEqual(len(processed_files), 1)
        self.assertIn(Path('/mock/dir/old_file_1.txt'), processed_files)
        mock_os_remove.assert_not_called() # Crucial for dry run

        # Check print calls for dry run message
        mock_print.assert_any_call("\nThis was a DRY RUN. No files were actually deleted.")


    @patch('src.duster.datetime')
    @patch('src.duster.os.walk')
    @patch('src.duster.Path.is_dir')
    @patch('src.duster.Path.is_file')
    @patch('src.duster.Path.stat')
    @patch('src.duster.os.remove')
    @patch('builtins.print') # Mock print to suppress output during tests
    def test_clean_debris_delete(self, mock_print, mock_os_remove, mock_stat, mock_is_file, mock_is_dir, mock_os_walk, mock_datetime):
        mock_datetime.now.return_value = self.MOCK_NOW
        mock_datetime.fromtimestamp = datetime.fromtimestamp

        mock_is_dir.return_value = True
        mock_is_file.return_value = True

        # Mock rationale: Simulate files that would be found by find_old_files
        # without actually creating them.
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['old_file_1.txt', 'recent_file.log'])
        ]

        def mock_stat_side_effect(path_obj):
            mock_s = MagicMock()
            if 'old_file_1.txt' in str(path_obj):
                mock_s.st_mtime = (self.MOCK_NOW - timedelta(days=100)).timestamp()
            elif 'recent_file.log' in str(path_obj):
                mock_s.st_mtime = (self.MOCK_NOW - timedelta(days=50)).timestamp()
            else:
                raise FileNotFoundError
            return mock_s
        mock_stat.side_effect = mock_stat_side_effect

        target_dir = Path('/mock/dir')
        
        processed_files = clean_debris(target_dir, 90, dry_run=False)
        
        self.assertEqual(len(processed_files), 1)
        self.assertIn(Path('/mock/dir/old_file_1.txt'), processed_files)
        mock_os_remove.assert_called_once_with(Path('/mock/dir/old_file_1.txt')) # Ensure deletion was called

        # Check print calls for deletion message
        mock_print.assert_any_call(f"\nSuccessfully cleared 1 pieces of data debris.")


    @patch('src.duster.datetime')
    @patch('src.duster.os.walk')
    @patch('src.duster.Path.is_dir')
    @patch('src.duster.Path.is_file')
    @patch('src.duster.Path.stat')
    @patch('src.duster.os.remove')
    @patch('builtins.print')
    def test_clean_debris_no_files_found(self, mock_print, mock_os_remove, mock_stat, mock_is_file, mock_is_dir, mock_os_walk, mock_datetime):
        mock_datetime.now.return_value = self.MOCK_NOW
        mock_datetime.fromtimestamp = datetime.fromtimestamp

        mock_is_dir.return_value = True
        mock_is_file.return_value = True

        # Mock rationale: Simulate a scenario where no files meet the age criteria.
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['recent_file_1.txt', 'recent_file_2.log'])
        ]

        def mock_stat_side_effect(path_obj):
            mock_s = MagicMock()
            mock_s.st_mtime = (self.MOCK_NOW - timedelta(days=10)).timestamp() # All files are recent
            return mock_s
        mock_stat.side_effect = mock_stat_side_effect

        target_dir = Path('/mock/dir')
        
        processed_files = clean_debris(target_dir, 90, dry_run=True)
        
        self.assertEqual(len(processed_files), 0)
        mock_os_remove.assert_not_called()
        mock_print.assert_any_call("No data debris found. Your digital wasteland is surprisingly clean!")


    @patch('src.duster.datetime')
    @patch('src.duster.os.walk')
    @patch('src.duster.Path.is_dir')
    @patch('src.duster.Path.is_file')
    @patch('src.duster.Path.stat')
    @patch('src.duster.os.remove')
    @patch('builtins.print')
    def test_clean_debris_deletion_error(self, mock_print, mock_os_remove, mock_stat, mock_is_file, mock_is_dir, mock_os_walk, mock_datetime):
        mock_datetime.now.return_value = self.MOCK_NOW
        mock_datetime.fromtimestamp = datetime.fromtimestamp

        mock_is_dir.return_value = True
        mock_is_file.return_value = True

        # Mock rationale: Simulate a file that exists but cannot be deleted due to permissions or other errors.
        mock_os_walk.return_value = [
            ('/mock/dir', [], ['problem_file.txt'])
        ]

        def mock_stat_side_effect(path_obj):
            mock_s = MagicMock()
            mock_s.st_mtime = (self.MOCK_NOW - timedelta(days=100)).timestamp()
            return mock_s
        mock_stat.side_effect = mock_stat_side_effect

        mock_os_remove.side_effect = OSError("Permission denied")

        target_dir = Path('/mock/dir')
        
        processed_files = clean_debris(target_dir, 90, dry_run=False)
        
        self.assertEqual(len(processed_files), 0) # No files were successfully processed/deleted
        mock_os_remove.assert_called_once_with(Path('/mock/dir/problem_file.txt'))
        mock_print.assert_any_call(f"    [ERROR] Could not delete {Path('/mock/dir/problem_file.txt')}: Permission denied")


if __name__ == '__main__':
    unittest.main()
