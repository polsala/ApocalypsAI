import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the src directory to the path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import dust_bunny_sweeper

class TestDustBunnySweeper(unittest.TestCase):

    @patch('os.listdir')
    def test_is_empty_dir(self, mock_listdir):
        # Mock rationale: os.listdir is mocked to simulate directory contents without actual file system interaction.
        mock_listdir.return_value = []
        self.assertTrue(dust_bunny_sweeper.is_empty_dir('/path/to/empty'))

        mock_listdir.return_value = ['file.txt']
        self.assertFalse(dust_bunny_sweeper.is_empty_dir('/path/to/not_empty'))

        mock_listdir.return_value = ['subdir']
        self.assertFalse(dust_bunny_sweeper.is_empty_dir('/path/to/not_empty_with_subdir'))

    @patch('os.path.isfile', return_value=True)
    @patch('os.path.getmtime')
    @patch('dust_bunny_sweeper.datetime') # Mock datetime from the module under test
    def test_is_old_file(self, mock_datetime, mock_getmtime, mock_isfile):
        # Mock rationale: os.path.getmtime is mocked to control file modification times.
        # datetime.now is mocked to control the 'current' time for age calculation.
        # os.path.isfile is mocked to ensure the function thinks it's dealing with a file.

        # Set a fixed current time for deterministic testing
        mock_datetime.now.return_value = datetime(2023, 10, 26)
        mock_datetime.fromtimestamp = datetime.fromtimestamp # Keep original for conversion
        mock_datetime.timedelta = timedelta # Keep original for timedelta

        # File modified 40 days ago (older than 30-day threshold)
        old_file_mtime = (datetime(2023, 10, 26) - timedelta(days=40)).timestamp()
        mock_getmtime.return_value = old_file_mtime
        self.assertTrue(dust_bunny_sweeper.is_old_file('/path/to/old_file.log', 30))

        # File modified 20 days ago (not older than 30-day threshold)
        recent_file_mtime = (datetime(2023, 10, 26) - timedelta(days=20)).timestamp()
        mock_getmtime.return_value = recent_file_mtime
        self.assertFalse(dust_bunny_sweeper.is_old_file('/path/to/recent_file.log', 30))

        # File modified exactly 30 days ago (not strictly older)
        boundary_file_mtime = (datetime(2023, 10, 26) - timedelta(days=30)).timestamp()
        mock_getmtime.return_value = boundary_file_mtime
        self.assertFalse(dust_bunny_sweeper.is_old_file('/path/to/boundary_file.log', 30))

        # Test with a non-file path
        mock_isfile.return_value = False
        self.assertFalse(dust_bunny_sweeper.is_old_file('/path/to/dir', 30))

    def test_matches_pattern(self):
        # Mock rationale: This function is pure and doesn't require mocking.
        patterns = ['.log', '.tmp', '~']
        self.assertTrue(dust_bunny_sweeper.matches_pattern('app.log', patterns))
        self.assertTrue(dust_bunny_sweeper.matches_pattern('cache.tmp', patterns))
        self.assertTrue(dust_bunny_sweeper.matches_pattern('config.bak~', patterns))
        self.assertFalse(dust_bunny_sweeper.matches_pattern('document.pdf', patterns))
        self.assertFalse(dust_bunny_sweeper.matches_pattern('image.jpg', patterns))

    @patch('os.path.getmtime')
    @patch('dust_bunny_sweeper.datetime')
    @patch('os.walk')
    @patch('os.path.isfile', return_value=True) # Assume all files in walk are files
    @patch('os.listdir', return_value=[]) # Assume all dirs are empty unless specified by os.walk
    def test_scan_for_dust_bunnies(self, mock_listdir, mock_isfile, mock_os_walk, mock_datetime, mock_getmtime):
        # Mock rationale: os.walk is mocked to simulate directory structure.
        # os.path.getmtime and datetime.now are mocked for age-based filtering.
        # os.path.isfile is mocked to simplify file existence checks.
        # os.listdir is mocked to ensure empty dir checks are controlled.

        # Set a fixed current time for deterministic testing
        mock_datetime.now.return_value = datetime(2023, 10, 26)
        mock_datetime.fromtimestamp = datetime.fromtimestamp
        mock_datetime.timedelta = timedelta

        # Simulate a file system structure
        # root, dirs, files
        mock_os_walk.return_value = [
            ('/project', ['empty_dir', 'logs', 'temp'], ['main.py', 'config.ini']),
            ('/project/empty_dir', [], []), # This should be detected as empty
            ('/project/logs', [], ['app.log', 'old.log', 'recent.log']),
            ('/project/temp', [], ['cache.tmp', 'data.txt~', 'current.tmp']),
        ]

        # Define modification times for files
        file_mtimes = {
            '/project/logs/app.log': (datetime(2023, 10, 26) - timedelta(days=40)).timestamp(), # Old
            '/project/logs/old.log': (datetime(2023, 10, 26) - timedelta(days=60)).timestamp(), # Very Old
            '/project/logs/recent.log': (datetime(2023, 10, 26) - timedelta(days=10)).timestamp(), # Recent
            '/project/temp/cache.tmp': (datetime(2023, 10, 26) - timedelta(days=35)).timestamp(), # Old
            '/project/temp/data.txt~': (datetime(2023, 10, 26) - timedelta(days=50)).timestamp(), # Old
            '/project/temp/current.tmp': (datetime(2023, 10, 26) - timedelta(days=5)).timestamp(), # Recent
            '/project/main.py': (datetime(2023, 10, 26) - timedelta(days=1)).timestamp(), # Not a pattern file
            '/project/config.ini': (datetime(2023, 10, 26) - timedelta(days=1)).timestamp(), # Not a pattern file
        }
        mock_getmtime.side_effect = lambda path: file_mtimes.get(path, datetime.now().timestamp())

        empty_dirs, old_temp_files = dust_bunny_sweeper.scan_for_dust_bunnies(
            '/project', age_threshold_days=30, file_patterns=['.log', '.tmp', '~']
        )

        self.assertIn('/project/empty_dir', empty_dirs)
        self.assertEqual(len(empty_dirs), 1)

        # Expected old/temp files based on age_threshold_days=30
        expected_old_temp_files = [
            ('/project/logs/app.log', datetime(2023, 9, 16)),
            ('/project/logs/old.log', datetime(2023, 8, 27)),
            ('/project/temp/cache.tmp', datetime(2023, 9, 21)),
            ('/project/temp/data.txt~', datetime(2023, 9, 6)),
        ]
        # Convert the list of tuples to sets for order-independent comparison
        self.assertSetEqual(set(old_temp_files), set(expected_old_temp_files))
        self.assertEqual(len(old_temp_files), 4)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('os.path.isdir', return_value=True)
    @patch('dust_bunny_sweeper.scan_for_dust_bunnies', return_value=(
        ['/test_dir/empty_folder'],
        [('/test_dir/logs/old.log', datetime(2023, 1, 15)),
         ('/test_dir/temp/cache.tmp', datetime(2023, 2, 1))]
    ))
    def test_main_output(self, mock_scan, mock_isdir, mock_exit, mock_stdout):
        # Mock rationale: sys.stdout is mocked to capture printed output.
        # sys.exit is mocked to prevent the test from terminating prematurely.
        # os.path.isdir is mocked to simulate a valid target directory.
        # scan_for_dust_bunnies is mocked to provide controlled results for output testing.

        # Simulate command-line arguments
        with patch('sys.argv', ['dust_bunny_sweeper.py', '/test_dir', '--age', '45', '--patterns', '.bak,.old']):
            dust_bunny_sweeper.main()

            output = mock_stdout.write.call_args_list
            output_str = "".join(call.args[0] for call in output)

            self.assertIn("🧹🐰 Digital Dust Bunny Sweeper Report 🐰🧹", output_str)
            self.assertIn("Scanning: /test_dir", output_str)
            self.assertIn("Age Threshold: 45 days", output_str)
            self.assertIn("File Patterns: ['.bak', '.old']", output_str)
            self.assertIn("--- Empty Directories ---", output_str)
            self.assertIn("- /test_dir/empty_folder", output_str)
            self.assertIn("--- Old/Temporary Files ---", output_str)
            self.assertIn("- /test_dir/logs/old.log (Last modified: 2023-01-15)", output_str)
            self.assertIn("- /test_dir/temp/cache.tmp (Last modified: 2023-02-01)", output_str)
            self.assertIn("Found 3 digital dust bunnies. Consider giving them a good sweep!", output_str)
            self.assertIn("--- Scan Complete!", output_str)
            mock_exit.assert_not_called() # Ensure it didn't exit prematurely

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('os.path.isdir', return_value=False)
    def test_main_invalid_dir_exit(self, mock_isdir, mock_exit, mock_stdout):
        # Mock rationale: sys.stdout is mocked to capture printed output.
        # sys.exit is mocked to prevent the test from terminating prematurely.
        # os.path.isdir is mocked to simulate an invalid target directory.

        with patch('sys.argv', ['dust_bunny_sweeper.py', '/nonexistent_dir']):
            dust_bunny_sweeper.main()
            mock_exit.assert_called_once_with(1)
            output_str = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
            self.assertIn("Error: Target directory '/nonexistent_dir' does not exist or is not a directory.", output_str)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('os.path.isdir', return_value=True)
    @patch('dust_bunny_sweeper.scan_for_dust_bunnies', return_value=([], []))
    def test_main_no_dust_bunnies_found(self, mock_scan, mock_isdir, mock_exit, mock_stdout):
        # Mock rationale: sys.stdout is mocked to capture printed output.
        # sys.exit is mocked to prevent the test from terminating prematurely.
        # os.path.isdir is mocked to simulate a valid target directory.
        # scan_for_dust_bunnies is mocked to return no findings.

        with patch('sys.argv', ['dust_bunny_sweeper.py', '/clean_dir']):
            dust_bunny_sweeper.main()
            output_str = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
            self.assertIn("Your digital space is sparkling clean! No dust bunnies found.", output_str)
            self.assertIn("--- No Empty Directories Found ---", output_str)
            self.assertIn("--- No Old/Temporary Files Found ---", output_str)
            mock_exit.assert_not_called()

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_main_missing_args(self, mock_exit, mock_stdout):
        # Mock rationale: sys.stdout is mocked to capture printed output.
        # sys.exit is mocked to prevent the test from terminating prematurely.

        with patch('sys.argv', ['dust_bunny_sweeper.py']):
            dust_bunny_sweeper.main()
            mock_exit.assert_called_once_with(1)
            output_str = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
            self.assertIn("Usage: python dust_bunny_sweeper.py <target_directory> [--age <days>] [--patterns <pattern1,pattern2,...>]", output_str)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('os.path.isdir', return_value=True)
    def test_main_invalid_age_arg(self, mock_isdir, mock_exit, mock_stdout):
        # Mock rationale: sys.stdout is mocked to capture printed output.
        # sys.exit is mocked to prevent the test from terminating prematurely.
        # os.path.isdir is mocked to simulate a valid target directory.

        with patch('sys.argv', ['dust_bunny_sweeper.py', '/test_dir', '--age', 'not_a_number']):
            dust_bunny_sweeper.main()
            mock_exit.assert_called_once_with(1)
            output_str = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
            self.assertIn("Error: --age must be an integer.", output_str)


if __name__ == '__main__':
    unittest.main()
