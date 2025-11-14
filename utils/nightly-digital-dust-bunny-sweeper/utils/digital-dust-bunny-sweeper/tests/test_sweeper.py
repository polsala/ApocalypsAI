import unittest
from unittest.mock import patch, MagicMock
import datetime
import os
import sys
from io import StringIO

# Mock rationale: We need to control the filesystem state (files, modification times)
# and the current time for deterministic, offline testing. Mocking os.walk,
# os.path.getmtime, and datetime.datetime.now allows us to simulate various scenarios
# without touching the actual filesystem or relying on the system clock.

# Import the function to be tested
# Assuming the test is run from the 'digital-dust-bunny-sweeper' directory
# or that 'src' is in the Python path.
from src.sweeper import find_dust_bunnies, main

class TestDigitalDustBunnySweeper(unittest.TestCase):

    @patch('datetime.datetime')
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_no_dust_bunnies(self, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Simulate a clean directory with no old or temporary files.
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
        mock_datetime.timedelta.side_effect = datetime.timedelta

        # Simulate a directory with recent, non-temp files
        mock_os_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'report.csv'])
        ]
        # All files are recent (e.g., modified yesterday)
        mock_getmtime.side_effect = lambda p: datetime.datetime(2023, 10, 25, 10, 0, 0).timestamp()

        bunnies = find_dust_bunnies('/test_dir', 30, ['\.tmp$', '\.bak$'])
        self.assertEqual(len(bunnies), 0)

    @patch('datetime.datetime')
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_old_files_found(self, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Simulate a directory with files older than the threshold.
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
        mock_datetime.timedelta.side_effect = datetime.timedelta

        mock_os_walk.return_value = [
            ('/test_dir', [], ['old_doc.pdf', 'very_old_image.jpg', 'recent.txt'])
        ]
        # old_doc.pdf and very_old_image.jpg are older than 30 days
        # recent.txt is not
        def getmtime_side_effect(path):
            if 'old_doc.pdf' in path:
                return datetime.datetime(2023, 8, 1, 10, 0, 0).timestamp() # ~86 days old
            elif 'very_old_image.jpg' in path:
                return datetime.datetime(2022, 1, 1, 10, 0, 0).timestamp() # ~660 days old
            else:
                return datetime.datetime(2023, 10, 20, 10, 0, 0).timestamp() # ~6 days old
        mock_getmtime.side_effect = getmtime_side_effect

        bunnies = find_dust_bunnies('/test_dir', 30, []) # No patterns, only age
        self.assertEqual(len(bunnies), 2)
        self.assertIn({'path': '/test_dir/old_doc.pdf', 'reason': 'Older than 30 days', 'last_modified': '2023-08-01'}, bunnies)
        self.assertIn({'path': '/test_dir/very_old_image.jpg', 'reason': 'Older than 30 days', 'last_modified': '2022-01-01'}, bunnies)

    @patch('datetime.datetime')
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_pattern_matched_files_found(self, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Simulate a directory with files matching specific patterns.
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
        mock_datetime.timedelta.side_effect = datetime.timedelta

        mock_os_walk.return_value = [
            ('/test_dir', [], ['temp.tmp', 'backup.bak', 'normal.txt', 'log.log'])
        ]
        # All files are recent, so only patterns should trigger
        mock_getmtime.side_effect = lambda p: datetime.datetime(2023, 10, 25, 10, 0, 0).timestamp()

        bunnies = find_dust_bunnies('/test_dir', 30, ['\.tmp$', '\.bak$', '\.log$'])
        self.assertEqual(len(bunnies), 3)
        self.assertIn({'path': '/test_dir/temp.tmp', 'reason': 'Matches pattern: \\.tmp$', 'last_modified': '2023-10-25'}, bunnies)
        self.assertIn({'path': '/test_dir/backup.bak', 'reason': 'Matches pattern: \\.bak$', 'last_modified': '2023-10-25'}, bunnies)
        self.assertIn({'path': '/test_dir/log.log', 'reason': 'Matches pattern: \\.log$', 'last_modified': '2023-10-25'}, bunnies)

    @patch('datetime.datetime')
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_mixed_dust_bunnies(self, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Simulate a directory with files that are old AND match patterns, or just one criteria.
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
        mock_datetime.timedelta.side_effect = datetime.timedelta

        mock_os_walk.return_value = [
            ('/test_dir', [], ['old_temp.tmp', 'old_file.txt', 'recent_log.log', 'recent_file.txt'])
        ]

        def getmtime_side_effect(path):
            if 'old_temp.tmp' in path: # Old and pattern
                return datetime.datetime(2023, 5, 1, 10, 0, 0).timestamp()
            elif 'old_file.txt' in path: # Only old
                return datetime.datetime(2023, 6, 1, 10, 0, 0).timestamp()
            elif 'recent_log.log' in path: # Only pattern
                return datetime.datetime(2023, 10, 20, 10, 0, 0).timestamp()
            else: # Neither
                return datetime.datetime(2023, 10, 25, 10, 0, 0).timestamp()
        mock_getmtime.side_effect = getmtime_side_effect

        bunnies = find_dust_bunnies('/test_dir', 90, ['\.tmp$', '\.log$'])
        self.assertEqual(len(bunnies), 3)
        # Note: The 'reason' string combines and sorts unique reasons alphabetically
        self.assertIn({'path': '/test_dir/old_temp.tmp', 'reason': 'Matches pattern: \\.tmp$; Older than 90 days', 'last_modified': '2023-05-01'}, bunnies)
        self.assertIn({'path': '/test_dir/old_file.txt', 'reason': 'Older than 90 days', 'last_modified': '2023-06-01'}, bunnies)
        self.assertIn({'path': '/test_dir/recent_log.log', 'reason': 'Matches pattern: \\.log$', 'last_modified': '2023-10-20'}, bunnies)

    @patch('datetime.datetime')
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_os_error_handling(self, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Ensure the utility handles files that become inaccessible during scan.
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.fromtimestamp.side_effect = datetime.datetime.fromtimestamp
        mock_datetime.timedelta.side_effect = datetime.timedelta

        mock_os_walk.return_value = [
            ('/test_dir', [], ['accessible.txt', 'inaccessible.txt'])
        ]

        def getmtime_side_effect(path):
            if 'inaccessible.txt' in path:
                raise OSError("Permission denied")
            else:
                return datetime.datetime(2023, 1, 1, 10, 0, 0).timestamp()
        mock_getmtime.side_effect = getmtime_side_effect

        # Capture stdout to check warning message
        captured_output = StringIO()
        sys.stdout = captured_output

        bunnies = find_dust_bunnies('/test_dir', 30, [])

        sys.stdout = sys.__stdout__ # Reset stdout

        self.assertEqual(len(bunnies), 1) # Only accessible.txt should be found
        self.assertIn({'path': '/test_dir/accessible.txt', 'reason': 'Older than 30 days', 'last_modified': '2023-01-01'}, bunnies)
        self.assertIn("Warning: Could not access /test_dir/inaccessible.txt - Permission denied", captured_output.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.sweeper.find_dust_bunnies')
    def test_main_no_bunnies_output(self, mock_find_dust_bunnies, mock_parse_args, mock_stdout):
        # Mock rationale: Test the main function's output when no dust bunnies are found.
        mock_parse_args.return_value = MagicMock(path='/test_dir', age=30, patterns=[])
        mock_find_dust_bunnies.return_value = []

        main()
        output = mock_stdout.getvalue()
        self.assertIn("Scanning /test_dir for digital dust bunnies...", output)
        self.assertIn("No digital dust bunnies found. Your directory is sparkling clean!", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.sweeper.find_dust_bunnies')
    def test_main_with_bunnies_output(self, mock_find_dust_bunnies, mock_parse_args, mock_stdout):
        # Mock rationale: Test the main function's output when dust bunnies are found.
        mock_parse_args.return_value = MagicMock(path='/test_dir', age=30, patterns=[])
        mock_find_dust_bunnies.return_value = [
            {'path': '/test_dir/bunny1.tmp', 'reason': 'Matches pattern: \\.tmp$', 'last_modified': '2023-10-01'},
            {'path': '/test_dir/bunny2.old', 'reason': 'Older than 30 days', 'last_modified': '2023-01-01'}
        ]

        main()
        output = mock_stdout.getvalue()
        self.assertIn("Scanning /test_dir for digital dust bunnies...", output)
        self.assertIn("Found 2 digital dust bunnies:", output)
        self.assertIn("- /test_dir/bunny1.tmp (Reason: Matches pattern: \\.tmp$, Last modified: 2023-10-01)", output)
        self.assertIn("- /test_dir/bunny2.old (Reason: Older than 30 days, Last modified: 2023-01-01)", output)
        self.assertIn("Consider reviewing these files for potential cleanup.", output)

if __name__ == '__main__':
    unittest.main()
