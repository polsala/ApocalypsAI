import unittest
from unittest.mock import patch, MagicMock
import os
import datetime
import shutil
from src.dust_collector import collect_cosmic_dust, is_file_empty, is_file_old, matches_pattern

class TestDustCollector(unittest.TestCase):

    @patch('os.path.exists')
    @patch('os.path.getsize')
    def test_is_file_empty(self, mock_getsize, mock_exists):
        # Mock rationale: os.path.exists and os.path.getsize are system calls that depend on the filesystem state.
        # Mocking them allows deterministic testing of the logic without actual file creation.
        
        mock_exists.return_value = True
        mock_getsize.return_value = 0
        self.assertTrue(is_file_empty("/path/to/empty_file.txt"))

        mock_getsize.return_value = 100
        self.assertFalse(is_file_empty("/path/to/non_empty_file.txt"))

        mock_exists.return_value = False
        self.assertFalse(is_file_empty("/path/to/non_existent_file.txt"))

    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('datetime.datetime')
    def test_is_file_old(self, mock_datetime, mock_getmtime, mock_exists):
        # Mock rationale: os.path.exists and os.path.getmtime are system calls.
        # datetime.datetime.now() is time-dependent. Mocking these ensures deterministic age calculation.
        
        mock_exists.return_value = True
        
        # Current time: Jan 1, 2024
        mock_datetime.now.return_value = datetime.datetime(2024, 1, 1)
        
        # File modified: Oct 1, 2023 (92 days old)
        mock_getmtime.return_value = datetime.datetime(2023, 10, 1).timestamp()
        self.assertTrue(is_file_old("/path/to/old_file.txt", 90)) # 92 > 90 days

        # File modified: Nov 15, 2023 (47 days old)
        mock_getmtime.return_value = datetime.datetime(2023, 11, 15).timestamp()
        self.assertFalse(is_file_old("/path/to/recent_file.txt", 90)) # 47 < 90 days

        mock_exists.return_value = False
        self.assertFalse(is_file_old("/path/to/non_existent_file.txt", 90))

    def test_matches_pattern(self):
        self.assertTrue(matches_pattern("temp.tmp", ["*.tmp"]))
        self.assertTrue(matches_pattern("cache_data.txt", ["cache_*"]))
        self.assertFalse(matches_pattern("report.pdf", ["*.tmp", "*.log"]))
        self.assertFalse(matches_pattern("document.doc", []))
        self.assertFalse(matches_pattern("document.doc", None))

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('src.dust_collector.is_file_empty', return_value=False)
    @patch('src.dust_collector.is_file_old', return_value=False)
    @patch('src.dust_collector.matches_pattern', return_value=False)
    @patch('os.path.exists', return_value=True) # For shutil.move and os.makedirs checks
    @patch('os.makedirs')
    @patch('shutil.move')
    def test_collect_cosmic_dust_dry_run(self, mock_shutil_move, mock_makedirs, mock_exists,
                                         mock_matches_pattern, mock_is_file_old, mock_is_file_empty,
                                         mock_os_walk, mock_isdir):
        # Mock rationale: os.walk, os.path.isdir, os.path.exists, os.makedirs, shutil.move are system calls.
        # is_file_empty, is_file_old, matches_pattern are internal functions whose behavior is controlled for this test.
        # This allows testing the main loop and decision logic of collect_cosmic_dust without actual file system interaction.

        mock_os_walk.return_value = [
            ('/root', [], ['file1.txt', 'file2.tmp']),
            ('/root/subdir', [], ['old_file.log', 'empty.txt'])
        ]

        # Scenario 1: Dry run, find empty file
        mock_is_file_empty.side_effect = lambda f: f == os.path.join('/root/subdir', 'empty.txt')
        mock_is_old_file.return_value = False
        mock_matches_pattern.return_value = False
        
        dust_files = collect_cosmic_dust(root_dir='/root', dry_run=True)
        self.assertEqual(len(dust_files), 1)
        self.assertIn(os.path.join('/root/subdir', 'empty.txt'), dust_files)
        mock_shutil_move.assert_not_called()
        mock_makedirs.assert_not_called()

        # Reset mocks for next scenario
        mock_is_file_empty.reset_mock(side_effect=True)
        mock_is_file_old.reset_mock()
        mock_matches_pattern.reset_mock()

        # Scenario 2: Dry run, find old file
        mock_is_file_empty.return_value = False
        mock_is_file_old.side_effect = lambda f, age: f == os.path.join('/root/subdir', 'old_file.log')
        mock_matches_pattern.return_value = False

        dust_files = collect_cosmic_dust(root_dir='/root', dry_run=True, age_threshold_days=90)
        self.assertEqual(len(dust_files), 1)
        self.assertIn(os.path.join('/root/subdir', 'old_file.log'), dust_files)
        mock_shutil_move.assert_not_called()
        mock_makedirs.assert_not_called()

        # Reset mocks for next scenario
        mock_is_file_empty.reset_mock()
        mock_is_file_old.reset_mock(side_effect=True)
        mock_matches_pattern.reset_mock()

        # Scenario 3: Dry run, find patterned file
        mock_is_file_empty.return_value = False
        mock_is_file_old.return_value = False
        mock_matches_pattern.side_effect = lambda f, p: f == 'file2.tmp' and p == ["*.tmp"]

        dust_files = collect_cosmic_dust(root_dir='/root', dry_run=True, patterns=["*.tmp"])
        self.assertEqual(len(dust_files), 1)
        self.assertIn(os.path.join('/root', 'file2.tmp'), dust_files)
        mock_shutil_move.assert_not_called()
        mock_makedirs.assert_not_called()

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('src.dust_collector.is_file_empty', return_value=False)
    @patch('src.dust_collector.is_file_old', return_value=False)
    @patch('src.dust_collector.matches_pattern', return_value=False)
    @patch('os.path.exists') # For shutil.move and os.makedirs checks
    @patch('os.makedirs')
    @patch('shutil.move')
    def test_collect_cosmic_dust_move_files(self, mock_shutil_move, mock_makedirs, mock_exists,
                                            mock_matches_pattern, mock_is_file_old, mock_is_file_empty,
                                            mock_os_walk, mock_isdir):
        # Mock rationale: Same as dry_run test, but specifically testing the move operation.
        # os.path.exists is mocked to control whether the dustbin exists and if target files exist.

        mock_os_walk.return_value = [
            ('/root', [], ['file_to_move.txt']),
        ]
        mock_is_file_empty.return_value = True # Make 'file_to_move.txt' dust
        mock_exists.side_effect = lambda path: path == '/root' or path == '/root/file_to_move.txt' # Only root and file exist initially

        dustbin_path = '/dustbin'
        dust_files = collect_cosmic_dust(root_dir='/root', dustbin_dir=dustbin_path, dry_run=False)

        self.assertEqual(len(dust_files), 1)
        self.assertIn(os.path.join('/root', 'file_to_move.txt'), dust_files)
        
        # Assert dustbin creation
        mock_makedirs.assert_called_once_with(dustbin_path, exist_ok=True)
        
        # Assert file move
        mock_shutil_move.assert_called_once_with(
            os.path.join('/root', 'file_to_move.txt'),
            os.path.join(dustbin_path, 'file_to_move.txt')
        )

    @patch('os.path.isdir', return_value=False)
    def test_collect_cosmic_dust_invalid_root_dir(self, mock_isdir):
        # Mock rationale: os.path.isdir is a system call. Mocking it allows testing error handling for invalid input.
        dust_files = collect_cosmic_dust(root_dir='/nonexistent', dry_run=True)
        self.assertEqual(len(dust_files), 0)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk', return_value=[])
    def test_collect_cosmic_dust_no_dust_found(self, mock_os_walk, mock_isdir):
        # Mock rationale: os.walk is a system call. Mocking it to return no files ensures no dust is found.
        dust_files = collect_cosmic_dust(root_dir='/root', dry_run=True)
        self.assertEqual(len(dust_files), 0)

    @patch('os.path.isdir', return_value=True)
    @patch('os.walk')
    @patch('src.dust_collector.is_file_empty', return_value=True) # All files are empty
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.move')
    def test_collect_cosmic_dust_collision_handling(self, mock_shutil_move, mock_makedirs, mock_exists,
                                                     mock_is_file_empty, mock_os_walk, mock_isdir):
        # Mock rationale: os.walk, os.path.exists, os.makedirs, shutil.move are system calls.
        # This test specifically checks the collision handling logic when moving files.

        mock_os_walk.return_value = [
            ('/root', [], ['duplicate.txt', 'another_duplicate.txt']),
        ]
        
        # Simulate that 'duplicate.txt' already exists in the dustbin, and then 'duplicate_1.txt'
        def exists_side_effect(path):
            if path == '/root': return True
            if path == '/root/duplicate.txt': return True
            if path == '/root/another_duplicate.txt': return True
            if path == '/dustbin': return True # Dustbin exists
            if path == os.path.join('/dustbin', 'duplicate.txt'): return True # First collision
            if path == os.path.join('/dustbin', 'duplicate_1.txt'): return True # Second collision
            return False

        mock_exists.side_effect = exists_side_effect

        dustbin_path = '/dustbin'
        collect_cosmic_dust(root_dir='/root', dustbin_dir=dustbin_path, dry_run=False)

        # Expect two move calls, with collision resolution for the first file
        self.assertEqual(mock_shutil_move.call_count, 2)
        mock_shutil_move.assert_any_call(
            os.path.join('/root', 'duplicate.txt'),
            os.path.join(dustbin_path, 'duplicate_2.txt') # Should resolve to duplicate_2.txt
        )
        mock_shutil_move.assert_any_call(
            os.path.join('/root', 'another_duplicate.txt'),
            os.path.join(dustbin_path, 'another_duplicate.txt')
        )


if __name__ == '__main__':
    unittest.main()
