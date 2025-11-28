import unittest
import os
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import the function to be tested
from src.sweeper import find_dust_bunnies

class TestDigitalDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        self.test_root = '/mock/test/path'
        self.now_timestamp = time.time()
        self.one_day_ago = self.now_timestamp - (1 * 24 * 60 * 60)
        self.seven_days_ago = self.now_timestamp - (7 * 24 * 60 * 60)
        self.thirty_one_days_ago = self.now_timestamp - (31 * 24 * 60 * 60)

        # Mock file system structure and properties
        self.mock_files = {
            # File, mtime (timestamp), size (bytes)
            '/mock/test/path/old_log.log': (self.thirty_one_days_ago, 100),
            '/mock/test/path/recent_report.txt': (self.one_day_ago, 200),
            '/mock/test/path/subdir/temp_file.tmp': (self.seven_days_ago, 50),
            '/mock/test/path/subdir/large_data.bin': (self.thirty_one_days_ago, 2000000), # ~2MB
            '/mock/test/path/subdir/small_config.json': (self.thirty_one_days_ago, 5),
            '/mock/test/path/important_doc.docx': (self.thirty_one_days_ago, 500),
            '/mock/test/path/another_recent.txt': (self.one_day_ago, 150)
        }

        # Mock os.walk to simulate directory traversal
        # Mock rationale: os.walk is a generator that traverses the file system. Mocking it allows us to define a static, deterministic file system structure for tests without actual disk I/O.
        self.mock_os_walk_return = [
            (self.test_root, ['subdir'], ['old_log.log', 'recent_report.txt', 'important_doc.docx', 'another_recent.txt']),
            (os.path.join(self.test_root, 'subdir'), [], ['temp_file.tmp', 'large_data.bin', 'small_config.json'])
        ]

    @patch('os.path.isfile', side_effect=lambda p: p in self.mock_files)
    @patch('os.path.getmtime', side_effect=lambda p: self.mock_files[p][0] if p in self.mock_files else 0)
    @patch('os.path.getsize', side_effect=lambda p: self.mock_files[p][1] if p in self.mock_files else 0)
    @patch('os.walk')
    def test_find_dust_bunnies_default_age(self, mock_os_walk, mock_getsize, mock_getmtime, mock_isfile):
        # Mock rationale: os.path.isfile, os.path.getmtime, os.path.getsize are system calls that interact with the actual file system. Mocking them allows us to control the properties (existence, modification time, size) of files deterministically for testing without relying on the real file system state.
        mock_os_walk.return_value = self.mock_os_walk_return

        # Default age is 30 days
        bunnies = find_dust_bunnies(
            root_path=self.test_root,
            age_days=30,
            min_size=0,
            max_size=2**63 - 1,
            include_patterns=[],
            exclude_patterns=[]
        )
        expected_bunnies = [
            '/mock/test/path/old_log.log',
            '/mock/test/path/subdir/large_data.bin',
            '/mock/test/path/subdir/small_config.json',
            '/mock/test/path/important_doc.docx'
        ]
        self.assertCountEqual(bunnies, expected_bunnies)

    @patch('os.path.isfile', side_effect=lambda p: p in self.mock_files)
    @patch('os.path.getmtime', side_effect=lambda p: self.mock_files[p][0] if p in self.mock_files else 0)
    @patch('os.path.getsize', side_effect=lambda p: self.mock_files[p][1] if p in self.mock_files else 0)
    @patch('os.walk')
    def test_find_dust_bunnies_custom_age(self, mock_os_walk, mock_getsize, mock_getmtime, mock_isfile):
        # Mock rationale: Same as above, controlling file properties for deterministic testing.
        mock_os_walk.return_value = self.mock_os_walk_return

        # Age threshold 5 days (should include temp_file.tmp which is 7 days old)
        bunnies = find_dust_bunnies(
            root_path=self.test_root,
            age_days=5,
            min_size=0,
            max_size=2**63 - 1,
            include_patterns=[],
            exclude_patterns=[]
        )
        expected_bunnies = [
            '/mock/test/path/old_log.log',
            '/mock/test/path/subdir/temp_file.tmp',
            '/mock/test/path/subdir/large_data.bin',
            '/mock/test/path/subdir/small_config.json',
            '/mock/test/path/important_doc.docx'
        ]
        self.assertCountEqual(bunnies, expected_bunnies)

    @patch('os.path.isfile', side_effect=lambda p: p in self.mock_files)
    @patch('os.path.getmtime', side_effect=lambda p: self.mock_files[p][0] if p in self.mock_files else 0)
    @patch('os.path.getsize', side_effect=lambda p: self.mock_files[p][1] if p in self.mock_files else 0)
    @patch('os.walk')
    def test_find_dust_bunnies_min_size(self, mock_os_walk, mock_getsize, mock_getmtime, mock_isfile):
        # Mock rationale: Same as above, controlling file properties for deterministic testing.
        mock_os_walk.return_value = self.mock_os_walk_return

        # Find files older than 30 days and larger than 1MB (1048576 bytes)
        bunnies = find_dust_bunnies(
            root_path=self.test_root,
            age_days=30,
            min_size=1048576,
            max_size=2**63 - 1,
            include_patterns=[],
            exclude_patterns=[]
        )
        expected_bunnies = [
            '/mock/test/path/subdir/large_data.bin'
        ]
        self.assertCountEqual(bunnies, expected_bunnies)

    @patch('os.path.isfile', side_effect=lambda p: p in self.mock_files)
    @patch('os.path.getmtime', side_effect=lambda p: self.mock_files[p][0] if p in self.mock_files else 0)
    @patch('os.path.getsize', side_effect=lambda p: self.mock_files[p][1] if p in self.mock_files else 0)
    @patch('os.walk')
    def test_find_dust_bunnies_max_size(self, mock_os_walk, mock_getsize, mock_getmtime, mock_isfile):
        # Mock rationale: Same as above, controlling file properties for deterministic testing.
        mock_os_walk.return_value = self.mock_os_walk_return

        # Find files older than 30 days and smaller than 10 bytes
        bunnies = find_dust_bunnies(
            root_path=self.test_root,
            age_days=30,
            min_size=0,
            max_size=10,
            include_patterns=[],
            exclude_patterns=[]
        )
        expected_bunnies = [
            '/mock/test/path/subdir/small_config.json'
        ]
        self.assertCountEqual(bunnies, expected_bunnies)

    @patch('os.path.isfile', side_effect=lambda p: p in self.mock_files)
    @patch('os.path.getmtime', side_effect=lambda p: self.mock_files[p][0] if p in self.mock_files else 0)
    @patch('os.path.getsize', side_effect=lambda p: self.mock_files[p][1] if p in self.mock_files else 0)
    @patch('os.walk')
    def test_find_dust_bunnies_include_pattern(self, mock_os_walk, mock_getsize, mock_getmtime, mock_isfile):
        # Mock rationale: Same as above, controlling file properties for deterministic testing.
        mock_os_walk.return_value = self.mock_os_walk_return

        # Find files older than 30 days, only .log files
        bunnies = find_dust_bunnies(
            root_path=self.test_root,
            age_days=30,
            min_size=0,
            max_size=2**63 - 1,
            include_patterns=['*.log'],
            exclude_patterns=[]
        )
        expected_bunnies = [
            '/mock/test/path/old_log.log'
        ]
        self.assertCountEqual(bunnies, expected_bunnies)

    @patch('os.path.isfile', side_effect=lambda p: p in self.mock_files)
    @patch('os.path.getmtime', side_effect=lambda p: self.mock_files[p][0] if p in self.mock_files else 0)
    @patch('os.path.getsize', side_effect=lambda p: self.mock_files[p][1] if p in self.mock_files else 0)
    @patch('os.walk')
    def test_find_dust_bunnies_exclude_pattern(self, mock_os_walk, mock_getsize, mock_getmtime, mock_isfile):
        # Mock rationale: Same as above, controlling file properties for deterministic testing.
        mock_os_walk.return_value = self.mock_os_walk_return

        # Find files older than 30 days, exclude .json files
        bunnies = find_dust_bunnies(
            root_path=self.test_root,
            age_days=30,
            min_size=0,
            max_size=2**63 - 1,
            include_patterns=[],
            exclude_patterns=['*.json']
        )
        expected_bunnies = [
            '/mock/test/path/old_log.log',
            '/mock/test/path/subdir/large_data.bin',
            '/mock/test/path/important_doc.docx'
        ]
        self.assertCountEqual(bunnies, expected_bunnies)

    @patch('os.path.isfile', side_effect=lambda p: p in self.mock_files)
    @patch('os.path.getmtime', side_effect=lambda p: self.mock_files[p][0] if p in self.mock_files else 0)
    @patch('os.path.getsize', side_effect=lambda p: self.mock_files[p][1] if p in self.mock_files else 0)
    @patch('os.walk')
    def test_find_dust_bunnies_combined_criteria(self, mock_os_walk, mock_getsize, mock_getmtime, mock_isfile):
        # Mock rationale: Same as above, controlling file properties for deterministic testing.
        mock_os_walk.return_value = self.mock_os_walk_return

        # Find files older than 5 days, smaller than 100 bytes, include *.tmp
        bunnies = find_dust_bunnies(
            root_path=self.test_root,
            age_days=5,
            min_size=0,
            max_size=100,
            include_patterns=['*.tmp'],
            exclude_patterns=[]
        )
        expected_bunnies = [
            '/mock/test/path/subdir/temp_file.tmp'
        ]
        self.assertCountEqual(bunnies, expected_bunnies)

    @patch('os.path.isfile', side_effect=lambda p: p in self.mock_files)
    @patch('os.path.getmtime', side_effect=lambda p: self.mock_files[p][0] if p in self.mock_files else 0)
    @patch('os.path.getsize', side_effect=lambda p: self.mock_files[p][1] if p in self.mock_files else 0)
    @patch('os.walk')
    @patch('os.remove')
    @patch('builtins.print') # Mock print to capture output
    def test_main_delete_mode(self, mock_print, mock_os_remove, mock_os_walk, mock_getsize, mock_getmtime, mock_isfile):
        # Mock rationale: os.remove performs actual file deletion, which is undesirable in tests. Mocking it ensures we can verify it's called without side effects. Mocking builtins.print allows us to assert on the console output of the script.
        mock_os_walk.return_value = self.mock_os_walk_return

        # Simulate command line arguments for main
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args:
            mock_parse_args.return_value = MagicMock(
                path=self.test_root,
                age_days=30,
                min_size=0,
                max_size=2**63 - 1,
                include_pattern=[],
                exclude_pattern=[],
                delete=True
            )
            from src.sweeper import main
            main()

            # Check that os.remove was called for the expected dust bunnies
            expected_deletions = [
                '/mock/test/path/old_log.log',
                '/mock/test/path/subdir/large_data.bin',
                '/mock/test/path/subdir/small_config.json',
                '/mock/test/path/important_doc.docx'
            ]
            self.assertEqual(mock_os_remove.call_count, len(expected_deletions))
            for bunny in expected_deletions:
                mock_os_remove.assert_any_call(bunny)

            # Check print output for deletion confirmation
            mock_print.assert_any_call("\n--- Initiating Dust Bunny Extermination! --- ")
            mock_print.assert_any_call(f"  Deleted: {expected_deletions[0]}")

    @patch('os.path.isfile', side_effect=lambda p: p in self.mock_files)
    @patch('os.path.getmtime', side_effect=lambda p: self.mock_files[p][0] if p in self.mock_files else 0)
    @patch('os.path.getsize', side_effect=lambda p: self.mock_files[p][1] if p in self.mock_files else 0)
    @patch('os.walk')
    @patch('os.remove')
    @patch('builtins.print')
    def test_main_dry_run_mode(self, mock_print, mock_os_remove, mock_os_walk, mock_getsize, mock_getmtime, mock_isfile):
        # Mock rationale: Same as above, ensuring no actual deletion and capturing print output.
        mock_os_walk.return_value = self.mock_os_walk_return

        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args:
            mock_parse_args.return_value = MagicMock(
                path=self.test_root,
                age_days=30,
                min_size=0,
                max_size=2**63 - 1,
                include_pattern=[],
                exclude_pattern=[],
                delete=False # Dry run
            )
            from src.sweeper import main
            main()

            # Ensure os.remove was NOT called
            mock_os_remove.assert_not_called()

            # Check print output for dry run message
            mock_print.assert_any_call("\n(Dry run: Use --delete to actually remove these files.)")

    @patch('os.path.isfile', side_effect=lambda p: p in self.mock_files)
    @patch('os.path.getmtime', side_effect=lambda p: self.mock_files[p][0] if p in self.mock_files else 0)
    @patch('os.path.getsize', side_effect=lambda p: self.mock_files[p][1] if p in self.mock_files else 0)
    @patch('os.walk')
    @patch('builtins.print')
    def test_main_no_bunnies_found(self, mock_print, mock_os_walk, mock_getsize, mock_getmtime, mock_isfile):
        # Mock rationale: Same as above, controlling file properties and capturing print output.
        mock_os_walk.return_value = self.mock_os_walk_return

        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args:
            mock_parse_args.return_value = MagicMock(
                path=self.test_root,
                age_days=0, # All files are 'old enough'
                min_size=1000000000, # Very large min size, no files will match
                max_size=2**63 - 1,
                include_pattern=[],
                exclude_pattern=[],
                delete=False
            )
            from src.sweeper import main
            main()

            mock_print.assert_any_call("No digital dust bunnies found. Your digital space is sparkling clean! ✨")

    @patch('os.path.isdir', return_value=False)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_sys_exit, mock_print, mock_isdir):
        # Mock rationale: os.path.isdir checks for directory existence. Mocking it allows us to simulate an invalid path without needing to create or verify a real directory. sys.exit is mocked to prevent the test runner from exiting.
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args:
            mock_parse_args.return_value = MagicMock(
                path='/non/existent/path',
                age_days=30,
                min_size=0,
                max_size=2**63 - 1,
                include_pattern=[],
                exclude_pattern=[],
                delete=False
            )
            from src.sweeper import main
            main()

            mock_print.assert_any_call("Error: Path '/non/existent/path' is not a valid directory.")
            mock_sys_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
