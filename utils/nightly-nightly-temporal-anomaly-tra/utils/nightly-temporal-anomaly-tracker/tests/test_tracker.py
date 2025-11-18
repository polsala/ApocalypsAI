import unittest
from unittest.mock import patch, MagicMock
import datetime
import os
from pathlib import Path
import sys

# Add the src directory to the path to allow importing tracker.py
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
import tracker

class TestTemporalAnomalyTracker(unittest.TestCase):

    def setUp(self):
        # Define a fixed 'current' time for deterministic tests (UTC)
        self.fixed_current_time = datetime.datetime(2024, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
        # Define some common timestamps relative to the fixed current time (as UTC timestamps)
        self.future_time_far = (self.fixed_current_time + datetime.timedelta(days=5)).timestamp()
        self.future_time_near = (self.fixed_current_time + datetime.timedelta(hours=1)).timestamp()
        self.past_time_recent = (self.fixed_current_time - datetime.timedelta(days=10)).timestamp()
        self.past_time_ancient = (self.fixed_current_time - datetime.timedelta(days=400)).timestamp()
        self.past_time_very_ancient = (self.fixed_current_time - datetime.timedelta(days=1000)).timestamp()

    @patch('tracker.get_current_time')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_scan_no_anomalies(self, mock_getmtime, mock_os_walk, mock_get_current_time):
        # Mock rationale: get_current_time needs to be fixed for deterministic tests.
        mock_get_current_time.return_value = self.fixed_current_time

        # Mock rationale: os.walk simulates the file system structure without actual disk access.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['file1.txt', 'file2.log'])
        ]

        # Mock rationale: os.path.getmtime controls the modification times of simulated files.
        # All files are within normal bounds.
        mock_getmtime.side_effect = lambda p: {
            Path('/test_dir/file1.txt'): self.past_time_recent,
            Path('/test_dir/file2.log'): self.past_time_recent,
        }.get(Path(p), self.fixed_current_time.timestamp())

        future, ancient = tracker.scan_for_anomalies(Path('/test_dir'), future_threshold_days=1, old_threshold_days=365)

        self.assertEqual(len(future), 0)
        self.assertEqual(len(ancient), 0)

    @patch('tracker.get_current_time')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_scan_future_anomalies(self, mock_getmtime, mock_os_walk, mock_get_current_time):
        # Mock rationale: get_current_time needs to be fixed for deterministic tests.
        mock_get_current_time.return_value = self.fixed_current_time

        # Mock rationale: os.walk simulates the file system structure without actual disk access.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['future_file.txt', 'normal_file.log'])
        ]

        # Mock rationale: os.path.getmtime controls the modification times of simulated files.
        # 'future_file.txt' is set to be in the future.
        mock_getmtime.side_effect = lambda p: {
            Path('/test_dir/future_file.txt'): self.future_time_far,
            Path('/test_dir/normal_file.log'): self.past_time_recent,
        }.get(Path(p), self.fixed_current_time.timestamp())

        # future_threshold_days=0 means any future modification is flagged.
        future, ancient = tracker.scan_for_anomalies(Path('/test_dir'), future_threshold_days=0, old_threshold_days=365)

        self.assertEqual(len(future), 1)
        self.assertEqual(future[0][0], Path('/test_dir/future_file.txt'))
        self.assertEqual(len(ancient), 0)

    @patch('tracker.get_current_time')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_scan_ancient_anomalies(self, mock_getmtime, mock_os_walk, mock_get_current_time):
        # Mock rationale: get_current_time needs to be fixed for deterministic tests.
        mock_get_current_time.return_value = self.fixed_current_time

        # Mock rationale: os.walk simulates the file system structure without actual disk access.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['ancient_report.pdf', 'normal_file.txt'])
        ]

        # Mock rationale: os.path.getmtime controls the modification times of simulated files.
        # 'ancient_report.pdf' is set to be very old.
        mock_getmtime.side_effect = lambda p: {
            Path('/test_dir/ancient_report.pdf'): self.past_time_ancient,
            Path('/test_dir/normal_file.txt'): self.past_time_recent,
        }.get(Path(p), self.fixed_current_time.timestamp())

        future, ancient = tracker.scan_for_anomalies(Path('/test_dir'), future_threshold_days=0, old_threshold_days=365)

        self.assertEqual(len(future), 0)
        self.assertEqual(len(ancient), 1)
        self.assertEqual(ancient[0][0], Path('/test_dir/ancient_report.pdf'))

    @patch('tracker.get_current_time')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_scan_both_anomalies(self, mock_getmtime, mock_os_walk, mock_get_current_time):
        # Mock rationale: get_current_time needs to be fixed for deterministic tests.
        mock_get_current_time.return_value = self.fixed_current_time

        # Mock rationale: os.walk simulates the file system structure without actual disk access.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['future.txt', 'ancient.log', 'normal.py'])
        ]

        # Mock rationale: os.path.getmtime controls the modification times of simulated files.
        mock_getmtime.side_effect = lambda p: {
            Path('/test_dir/future.txt'): self.future_time_far,
            Path('/test_dir/ancient.log'): self.past_time_very_ancient,
            Path('/test_dir/normal.py'): self.past_time_recent,
        }.get(Path(p), self.fixed_current_time.timestamp())

        future, ancient = tracker.scan_for_anomalies(Path('/test_dir'), future_threshold_days=0, old_threshold_days=365)

        self.assertEqual(len(future), 1)
        self.assertEqual(future[0][0], Path('/test_dir/future.txt'))
        self.assertEqual(len(ancient), 1)
        self.assertEqual(ancient[0][0], Path('/test_dir/ancient.log'))

    @patch('tracker.get_current_time')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_future_threshold_days(self, mock_getmtime, mock_os_walk, mock_get_current_time):
        # Mock rationale: get_current_time needs to be fixed for deterministic tests.
        mock_get_current_time.return_value = self.fixed_current_time

        # Mock rationale: os.walk simulates the file system structure without actual disk access.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['future_near.txt', 'future_far.txt'])
        ]

        # Mock rationale: os.path.getmtime controls the modification times of simulated files.
        mock_getmtime.side_effect = lambda p: {
            Path('/test_dir/future_near.txt'): self.future_time_near, # 1 hour in future
            Path('/test_dir/future_far.txt'): self.future_time_far,   # 5 days in future
        }.get(Path(p), self.fixed_current_time.timestamp())

        # With future_threshold_days=1, future_near.txt (1 hour) should NOT be flagged.
        # future_far.txt (5 days) SHOULD be flagged.
        future, ancient = tracker.scan_for_anomalies(Path('/test_dir'), future_threshold_days=1, old_threshold_days=365)

        self.assertEqual(len(future), 1)
        self.assertEqual(future[0][0], Path('/test_dir/future_far.txt'))
        self.assertEqual(len(ancient), 0)

    @patch('tracker.get_current_time')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_old_threshold_days(self, mock_getmtime, mock_os_walk, mock_get_current_time):
        # Mock rationale: get_current_time needs to be fixed for deterministic tests.
        mock_get_current_time.return_value = self.fixed_current_time

        # Mock rationale: os.walk simulates the file system structure without actual disk access.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['old_recent.txt', 'old_ancient.txt'])
        ]

        # Mock rationale: os.path.getmtime controls the modification times of simulated files.
        mock_getmtime.side_effect = lambda p: {
            Path('/test_dir/old_recent.txt'): self.past_time_recent, # 10 days old
            Path('/test_dir/old_ancient.txt'): self.past_time_ancient, # 400 days old
        }.get(Path(p), self.fixed_current_time.timestamp())

        # With old_threshold_days=365, old_recent.txt (10 days) should NOT be flagged.
        # old_ancient.txt (400 days) SHOULD be flagged.
        future, ancient = tracker.scan_for_anomalies(Path('/test_dir'), future_threshold_days=0, old_threshold_days=365)

        self.assertEqual(len(future), 0)
        self.assertEqual(len(ancient), 1)
        self.assertEqual(ancient[0][0], Path('/test_dir/old_ancient.txt'))

    @patch('tracker.get_current_time')
    @patch('os.walk')
    @patch('os.path.getmtime')
    def test_os_error_handling(self, mock_getmtime, mock_os_walk, mock_get_current_time):
        # Mock rationale: get_current_time needs to be fixed for deterministic tests.
        mock_get_current_time.return_value = self.fixed_current_time

        # Mock rationale: os.walk simulates the file system structure without actual disk access.
        mock_os_walk.return_value = [
            ('/test_dir', [], ['accessible.txt', 'inaccessible.txt'])
        ]

        # Mock rationale: os.path.getmtime controls the modification times of simulated files.
        # Simulate an OSError for 'inaccessible.txt'.
        def getmtime_side_effect(p):
            if Path(p) == Path('/test_dir/inaccessible.txt'):
                raise OSError("Permission denied")
            return self.past_time_recent

        mock_getmtime.side_effect = getmtime_side_effect

        # Mock rationale: Capture stdout to check if the warning message is printed.
        with patch('sys.stdout', new=MagicMock()) as mock_stdout:
            future, ancient = tracker.scan_for_anomalies(Path('/test_dir'))

            self.assertEqual(len(future), 0)
            self.assertEqual(len(ancient), 0)
            # Check if the warning message was printed
            mock_stdout.assert_any_call('Warning: Could not access /test_dir/inaccessible.txt: Permission denied\n')

    @patch('tracker.Path.is_dir', return_value=False)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_invalid_path(self, mock_print, mock_exit, mock_parse_args, mock_is_dir):
        # Mock rationale: Simulate command-line arguments.
        mock_parse_args.return_value = MagicMock(path='/nonexistent_dir', future_threshold_days=0, old_threshold_days=365)
        # Mock rationale: Prevent actual program exit during test.
        mock_exit.side_effect = SystemExit

        with self.assertRaises(SystemExit) as cm:
            tracker.main()
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_any_call("Error: Path '/nonexistent_dir' is not a valid directory.")

    @patch('tracker.scan_for_anomalies', return_value=([], []))
    @patch('tracker.Path.is_dir', return_value=True)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_no_anomalies_exit_0(self, mock_print, mock_exit, mock_parse_args, mock_is_dir, mock_scan):
        # Mock rationale: Simulate command-line arguments.
        mock_parse_args.return_value = MagicMock(path='/test_dir', future_threshold_days=0, old_threshold_days=365)
        # Mock rationale: Prevent actual program exit during test.
        mock_exit.side_effect = SystemExit

        with self.assertRaises(SystemExit) as cm:
            tracker.main()
        self.assertEqual(cm.exception.code, 0)
        mock_print.assert_any_call("\nScan complete.")

    @patch('tracker.scan_for_anomalies', return_value=([('future.txt', 'mod_time', 'curr_time')], []))
    @patch('tracker.Path.is_dir', return_value=True)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_with_anomalies_exit_1(self, mock_print, mock_exit, mock_parse_args, mock_is_dir, mock_scan):
        # Mock rationale: Simulate command-line arguments.
        mock_parse_args.return_value = MagicMock(path='/test_dir', future_threshold_days=0, old_threshold_days=365)
        # Mock rationale: Prevent actual program exit during test.
        mock_exit.side_effect = SystemExit

        with self.assertRaises(SystemExit) as cm:
            tracker.main()
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_any_call("\nScan complete.")

if __name__ == '__main__':
    unittest.main()
