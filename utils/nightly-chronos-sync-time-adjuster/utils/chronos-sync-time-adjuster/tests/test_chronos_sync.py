import unittest
from unittest.mock import patch
import datetime
import io
import sys

# Import the functions from the utility script
from src.chronos_sync import (
    get_current_utc_time,
    get_cosmic_alignment_time,
    format_timedelta,
    main,
    COSMIC_ALIGNMENT_TIME_STR,
    DATE_FORMAT
)

class TestChronosSync(unittest.TestCase):

    def test_get_current_utc_time(self):
        # Mock rationale: Ensure deterministic current time for testing.
        mock_now = datetime.datetime(2024, 10, 27, 10, 0, 0)
        with patch('datetime.datetime') as mock_dt:
            mock_dt.utcnow.return_value = mock_now
            mock_dt.strptime = datetime.datetime.strptime # Keep original strptime
            mock_dt.timedelta = datetime.timedelta # Keep original timedelta
            self.assertEqual(get_current_utc_time(), mock_now)

    def test_get_cosmic_alignment_time(self):
        expected_cat = datetime.datetime(2025, 1, 1, 0, 0, 0)
        self.assertEqual(get_cosmic_alignment_time(), expected_cat)

    def test_format_timedelta_positive(self):
        td = datetime.timedelta(days=1, hours=2, minutes=3, seconds=4)
        self.assertEqual(format_timedelta(td), "1 days, 02:03:04")

        td_seconds_only = datetime.timedelta(seconds=45)
        self.assertEqual(format_timedelta(td_seconds_only), "0 days, 00:00:45")

        td_large = datetime.timedelta(days=365, hours=12, minutes=30, seconds=0)
        self.assertEqual(format_timedelta(td_large), "365 days, 12:30:00")

    def test_format_timedelta_negative(self):
        td = datetime.timedelta(days=-1, hours=-2, minutes=-3, seconds=-4)
        self.assertEqual(format_timedelta(td), "1 days, 02:03:04") # Should return absolute value

        td_seconds_only = datetime.timedelta(seconds=-45)
        self.assertEqual(format_timedelta(td_seconds_only), "0 days, 00:00:45")

    def test_format_timedelta_zero(self):
        td = datetime.timedelta(0)
        self.assertEqual(format_timedelta(td), "0 days, 00:00:00")

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('datetime.datetime')
    def test_main_behind_target(self, mock_dt, mock_parse_args, mock_stdout):
        # Mock rationale: Control current time and CLI arguments for deterministic test scenarios.
        # Mock datetime.datetime to control utcnow() and keep strptime/timedelta functional.
        mock_dt.utcnow.return_value = datetime.datetime(2024, 10, 27, 10, 0, 0)
        mock_dt.strptime = datetime.datetime.strptime
        mock_dt.timedelta = datetime.timedelta
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw) # Allow datetime.datetime() calls

        # Mock argparse to simulate command-line arguments
        mock_parse_args.return_value.offset_hours = 0

        main()
        output = mock_stdout.getvalue()

        self.assertIn("Current UTC Time: 2024-10-27 10:00:00", output)
        self.assertIn("Cosmic Alignment Time: 2025-01-01 00:00:00", output)
        self.assertIn("Apocalypse Offset: +0 hours", output)
        self.assertIn("Target Sync Time: 2025-01-01 00:00:00", output)
        self.assertIn("Temporal Drift: Your system clock is currently 65 days, 14:00:00 behind the Target Sync Time.", output)
        self.assertIn("To synchronize, you need to advance your clock by 65 days, 14:00:00.", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('datetime.datetime')
    def test_main_ahead_of_target(self, mock_dt, mock_parse_args, mock_stdout):
        # Mock rationale: Control current time and CLI arguments for deterministic test scenarios.
        mock_dt.utcnow.return_value = datetime.datetime(2025, 1, 1, 0, 0, 5)
        mock_dt.strptime = datetime.datetime.strptime
        mock_dt.timedelta = datetime.timedelta
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

        mock_parse_args.return_value.offset_hours = 0

        main()
        output = mock_stdout.getvalue()

        self.assertIn("Current UTC Time: 2025-01-01 00:00:05", output)
        self.assertIn("Target Sync Time: 2025-01-01 00:00:00", output)
        self.assertIn("Temporal Drift: Your system clock is currently 0 days, 00:00:05 ahead of the Target Sync Time.", output)
        self.assertIn("To synchronize, you need to rewind your clock by 0 days, 00:00:05.", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('datetime.datetime')
    def test_main_perfectly_aligned(self, mock_dt, mock_parse_args, mock_stdout):
        # Mock rationale: Control current time and CLI arguments for deterministic test scenarios.
        mock_dt.utcnow.return_value = datetime.datetime(2025, 1, 1, 0, 0, 0)
        mock_dt.strptime = datetime.datetime.strptime
        mock_dt.timedelta = datetime.timedelta
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

        mock_parse_args.return_value.offset_hours = 0

        main()
        output = mock_stdout.getvalue()

        self.assertIn("Current UTC Time: 2025-01-01 00:00:00", output)
        self.assertIn("Target Sync Time: 2025-01-01 00:00:00", output)
        self.assertIn("Temporal Drift: Your system clock is perfectly aligned with the Target Sync Time. No adjustment needed.", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('datetime.datetime')
    def test_main_with_positive_offset(self, mock_dt, mock_parse_args, mock_stdout):
        # Mock rationale: Control current time and CLI arguments for deterministic test scenarios.
        mock_dt.utcnow.return_value = datetime.datetime(2024, 12, 31, 23, 0, 0) # 1 hour before CAT
        mock_dt.strptime = datetime.datetime.strptime
        mock_dt.timedelta = datetime.timedelta
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

        mock_parse_args.return_value.offset_hours = 1 # CAT + 1 hour

        main()
        output = mock_stdout.getvalue()

        self.assertIn("Current UTC Time: 2024-12-31 23:00:00", output)
        self.assertIn("Apocalypse Offset: +1 hours", output)
        self.assertIn("Target Sync Time: 2025-01-01 01:00:00", output) # CAT (00:00) + 1 hour offset
        self.assertIn("Temporal Drift: Your system clock is currently 0 days, 02:00:00 behind the Target Sync Time.", output)
        self.assertIn("To synchronize, you need to advance your clock by 0 days, 02:00:00.", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('datetime.datetime')
    def test_main_with_negative_offset(self, mock_dt, mock_parse_args, mock_stdout):
        # Mock rationale: Control current time and CLI arguments for deterministic test scenarios.
        mock_dt.utcnow.return_value = datetime.datetime(2025, 1, 1, 0, 0, 0) # Exactly CAT
        mock_dt.strptime = datetime.datetime.strptime
        mock_dt.timedelta = datetime.timedelta
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

        mock_parse_args.return_value.offset_hours = -1 # CAT - 1 hour

        main()
        output = mock_stdout.getvalue()

        self.assertIn("Current UTC Time: 2025-01-01 00:00:00", output)
        self.assertIn("Apocalypse Offset: -1 hours", output)
        self.assertIn("Target Sync Time: 2024-12-31 23:00:00", output) # CAT (00:00) - 1 hour offset
        self.assertIn("Temporal Drift: Your system clock is currently 0 days, 01:00:00 ahead of the Target Sync Time.", output)
        self.assertIn("To synchronize, you need to rewind your clock by 0 days, 01:00:00.", output)


if __name__ == '__main__':
    unittest.main()
