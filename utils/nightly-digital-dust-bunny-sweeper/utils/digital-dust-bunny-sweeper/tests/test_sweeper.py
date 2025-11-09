import unittest
import os
import sys
import io
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Adjust sys.path to allow importing sweeper from the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import sweeper
sys.path.pop(0)

class TestDigitalDustBunnySweeper(unittest.TestCase):

    def setUp(self):
        # Capture stdout for testing print statements
        self.held_stdout = sys.stdout
        self.mock_stdout = io.StringIO()
        sys.stdout = self.mock_stdout

        # Define a fixed 'now' for deterministic testing
        self.mock_now = datetime(2023, 10, 26, 10, 0, 0) # October 26, 2023

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('sweeper.datetime')
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_find_dust_bunnies_basic(self, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Simulate a file system structure without actual files.
        # Mock rationale: Control file modification times for age-based filtering.
        # Mock rationale: Fix the current time for deterministic age calculations.

        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp = datetime.fromtimestamp # Use real fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow datetime constructor

        # Simulate a directory structure:
        # root_dir/
        #   old_file.txt (modified 40 days ago)
        #   new_file.txt (modified 10 days ago)
        #   old_dir/ (modified 40 days ago)
        #     another_old_file.log (modified 40 days ago, but ignored by default)
        #   new_dir/ (modified 10 days ago)
        #     yet_another_new_file.txt (modified 10 days ago)

        root_dir = '/mock/project'
        mock_os_walk.return_value = [
            (root_dir, ['old_dir', 'new_dir'], ['old_file.txt', 'new_file.txt']),
            (os.path.join(root_dir, 'old_dir'), [], ['another_old_file.log']),
            (os.path.join(root_dir, 'new_dir'), [], ['yet_another_new_file.txt']),
        ]

        # Define modification times relative to mock_now
        # 40 days old
        old_timestamp = (self.mock_now - timedelta(days=40)).timestamp()
        # 10 days old
        new_timestamp = (self.mock_now - timedelta(days=10)).timestamp()

        def mock_getmtime_side_effect(path):
            if 'old_file.txt' in path or 'old_dir' == os.path.basename(path) or 'another_old_file.log' in path:
                return old_timestamp
            elif 'new_file.txt' in path or 'new_dir' == os.path.basename(path) or 'yet_another_new_file.txt' in path:
                return new_timestamp
            return self.mock_now.timestamp() # Default for root_dir if needed

        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Test with default age (30 days)
        dust_bunnies = sweeper.find_dust_bunnies(root_dir, 30, sweeper.get_default_ignore_patterns())

        expected_bunnies = [
            os.path.join(root_dir, 'old_file.txt'),
            os.path.join(root_dir, 'old_dir')
        ]
        # Note: 'another_old_file.log' is ignored by default patterns

        self.assertCountEqual(dust_bunnies, expected_bunnies)

    @patch('sweeper.datetime')
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_find_dust_bunnies_custom_age_and_ignore(self, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Simulate a file system structure without actual files.
        # Mock rationale: Control file modification times for age-based filtering.
        # Mock rationale: Fix the current time for deterministic age calculations.

        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        root_dir = '/mock/project'
        mock_os_walk.return_value = [
            (root_dir, ['temp_dir', 'important_dir'], ['old_data.csv', 'new_report.pdf', 'temp_log.txt']),
            (os.path.join(root_dir, 'temp_dir'), [], ['temp_file_1.tmp', 'temp_file_2.log']),
            (os.path.join(root_dir, 'important_dir'), [], ['config.json']),
        ]

        # 60 days old
        very_old_timestamp = (self.mock_now - timedelta(days=60)).timestamp()
        # 40 days old
        old_timestamp = (self.mock_now - timedelta(days=40)).timestamp()
        # 10 days old
        new_timestamp = (self.mock_now - timedelta(days=10)).timestamp()

        def mock_getmtime_side_effect(path):
            if 'old_data.csv' in path or 'temp_dir' == os.path.basename(path) or 'temp_file_1.tmp' in path or 'temp_file_2.log' in path:
                return very_old_timestamp
            elif 'new_report.pdf' in path:
                return new_timestamp
            elif 'config.json' in path or 'important_dir' == os.path.basename(path):
                return old_timestamp
            return self.mock_now.timestamp()

        mock_getmtime.side_effect = mock_getmtime_side_effect

        # Test with age=50 days, ignore 'temp_*' and '*.pdf'
        custom_ignore = ['temp_*', '*.pdf']
        dust_bunnies = sweeper.find_dust_bunnies(root_dir, 50, custom_ignore)

        expected_bunnies = [
            os.path.join(root_dir, 'old_data.csv'),
        ]
        # 'temp_dir' and its contents are ignored by 'temp_*'
        # 'new_report.pdf' is ignored by '*.pdf'
        # 'important_dir' and 'config.json' are not old enough (40 days < 50 days)

        self.assertCountEqual(dust_bunnies, expected_bunnies)

    @patch('sweeper.datetime')
    @patch('os.path.getmtime')
    @patch('os.walk')
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('sys.exit')
    def test_main_invalid_path(self, mock_sys_exit, mock_stderr, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Simulate an invalid directory path.
        # Mock rationale: Capture stderr output to check error messages.
        # Mock rationale: Prevent actual program exit during test.

        mock_os_walk.return_value = [] # No walk happens if path is invalid
        mock_getmtime.return_value = self.mock_now.timestamp()
        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp = datetime.fromtimestamp

        with patch('os.path.isdir', return_value=False):
            # Mock rationale: Force os.path.isdir to return False for the given path.
            test_args = ['sweeper.py', '/nonexistent/path']
            with patch('sys.argv', test_args):
                sweeper.main()

        mock_sys_exit.assert_called_once_with(1)
        self.assertIn("Error: The provided path '/nonexistent/path' is not a valid directory.", mock_stderr.getvalue())

    @patch('sweeper.datetime')
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_main_no_dust_bunnies(self, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Simulate a clean directory with no old files.
        # Mock rationale: Control file modification times.
        # Mock rationale: Fix the current time for deterministic age calculations.

        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        root_dir = '/mock/project'
        mock_os_walk.return_value = [
            (root_dir, [], ['new_file_1.txt', 'new_file_2.py']),
        ]

        new_timestamp = (self.mock_now - timedelta(days=5)).timestamp()
        mock_getmtime.return_value = new_timestamp

        with patch('os.path.isdir', return_value=True):
            # Mock rationale: Assume the root directory exists.
            test_args = ['sweeper.py', root_dir, '--age', '10']
            with patch('sys.argv', test_args):
                sweeper.main()

        output = self.mock_stdout.getvalue()
        self.assertIn("No digital dust bunnies found! Your project is sparkling clean.", output)

    @patch('sweeper.datetime')
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_main_with_dust_bunnies(self, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Simulate a directory with old files.
        # Mock rationale: Control file modification times.
        # Mock rationale: Fix the current time for deterministic age calculations.

        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        root_dir = '/mock/project'
        mock_os_walk.return_value = [
            (root_dir, ['old_dir'], ['old_file.txt', 'new_file.txt']),
            (os.path.join(root_dir, 'old_dir'), [], ['another_old_file.log']),
        ]

        old_timestamp = (self.mock_now - timedelta(days=40)).timestamp()
        new_timestamp = (self.mock_now - timedelta(days=10)).timestamp()

        def mock_getmtime_side_effect(path):
            if 'old_file.txt' in path or 'old_dir' == os.path.basename(path):
                return old_timestamp
            elif 'new_file.txt' in path:
                return new_timestamp
            elif 'another_old_file.log' in path:
                return old_timestamp # This will be ignored by default patterns
            return self.mock_now.timestamp()

        mock_getmtime.side_effect = mock_getmtime_side_effect

        with patch('os.path.isdir', return_value=True):
            # Mock rationale: Assume the root directory exists.
            test_args = ['sweeper.py', root_dir, '--age', '30']
            with patch('sys.argv', test_args):
                sweeper.main()

        output = self.mock_stdout.getvalue()
        self.assertIn("Found the following digital dust bunnies", output)
        self.assertIn(os.path.join(root_dir, 'old_file.txt'), output)
        self.assertIn(os.path.join(root_dir, 'old_dir'), output)
        self.assertNotIn(os.path.join(root_dir, 'new_file.txt'), output)
        self.assertNotIn(os.path.join(root_dir, 'old_dir', 'another_old_file.log'), output) # Ignored
        self.assertIn("Total: 2 items.", output)

    @patch('sweeper.datetime')
    @patch('os.path.getmtime')
    @patch('os.walk')
    def test_main_with_custom_ignore_patterns(self, mock_os_walk, mock_getmtime, mock_datetime):
        # Mock rationale: Simulate a directory with old files and custom ignore patterns.
        # Mock rationale: Control file modification times.
        # Mock rationale: Fix the current time for deterministic age calculations.

        mock_datetime.now.return_value = self.mock_now
        mock_datetime.fromtimestamp = datetime.fromtimestamp
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        root_dir = '/mock/project'
        mock_os_walk.return_value = [
            (root_dir, ['build'], ['old_file.txt', 'report.pdf']),
            (os.path.join(root_dir, 'build'), [], ['temp.log']),
        ]

        old_timestamp = (self.mock_now - timedelta(days=40)).timestamp()
        new_timestamp = (self.mock_now - timedelta(days=10)).timestamp()

        def mock_getmtime_side_effect(path):
            if 'old_file.txt' in path or 'build' == os.path.basename(path) or 'temp.log' in path:
                return old_timestamp
            elif 'report.pdf' in path:
                return new_timestamp
            return self.mock_now.timestamp()

        mock_getmtime.side_effect = mock_getmtime_side_effect

        with patch('os.path.isdir', return_value=True):
            # Mock rationale: Assume the root directory exists.
            test_args = ['sweeper.py', root_dir, '--age', '30', '--ignore-patterns', '*.pdf,build']
            with patch('sys.argv', test_args):
                sweeper.main()

        output = self.mock_stdout.getvalue()
        self.assertIn("Found the following digital dust bunnies", output)
        self.assertIn(os.path.join(root_dir, 'old_file.txt'), output)
        self.assertNotIn(os.path.join(root_dir, 'report.pdf'), output) # Ignored
        self.assertNotIn(os.path.join(root_dir, 'build'), output) # Ignored
        self.assertNotIn(os.path.join(root_dir, 'build', 'temp.log'), output) # Ignored because parent dir is ignored
        self.assertIn("Total: 1 items.", output)
