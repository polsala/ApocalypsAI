import unittest
from unittest.mock import patch
from datetime import datetime, timezone, timedelta

# Mock rationale: Freeze ``datetime.now`` to a known instant so that relative calculations are deterministic.
# The frozen moment is 2025‑01‑01 12:30:00 UTC.
FROZEN_NOW = datetime(2025, 1, 1, 12, 30, 0, tzinfo=timezone.utc)


def _mock_now(*args, **kwargs):
    # ``datetime.now(tz)`` is called with a ``ZoneInfo`` instance; we ignore it and return the frozen UTC time.
    return FROZEN_NOW


class TestEmojiClock(unittest.TestCase):
    @patch("emoji_clock.datetime")
    def test_future_timestamp(self, mock_datetime):
        # Arrange: mock ``datetime.now`` and ``datetime.fromisoformat``.
        mock_datetime.now.side_effect = _mock_now
        mock_datetime.fromisoformat.side_effect = lambda s: datetime.fromisoformat(s)
        mock_datetime.timezone = timezone
        mock_datetime.timedelta = timedelta
        mock_datetime.timezone.utc = timezone.utc
        # Act
        from emoji_clock import format_time
        result = format_time("2025-01-01T15:30:00+00:00")
        # Expected: 3:30 PM → 🕒, 3 hours in the future.
        self.assertEqual(result, "🕒 3:30 PM (in 3 hours)")

    @patch("emoji_clock.datetime")
    def test_past_timestamp(self, mock_datetime):
        mock_datetime.now.side_effect = _mock_now
        mock_datetime.fromisoformat.side_effect = lambda s: datetime.fromisoformat(s)
        mock_datetime.timezone = timezone
        mock_datetime.timedelta = timedelta
        mock_datetime.timezone.utc = timezone.utc
        from emoji_clock import format_time
        result = format_time("2024-12-30T10:00:00+00:00")
        # Difference: 2 days, 2 hours, 30 minutes ago → largest unit is days.
        self.assertEqual(result, "🕙 10:00 AM (2 days ago)")

    @patch("emoji_clock.datetime")
    def test_midnight_emoji(self, mock_datetime):
        mock_datetime.now.side_effect = _mock_now
        mock_datetime.fromisoformat.side_effect = lambda s: datetime.fromisoformat(s)
        mock_datetime.timezone = timezone
        mock_datetime.timedelta = timedelta
        mock_datetime.timezone.utc = timezone.utc
        from emoji_clock import format_time
        # 00:15 UTC on the same day → 🕛 12:15 AM, 12 hours 15 minutes ago.
        result = format_time("2025-01-01T00:15:00+00:00")
        self.assertEqual(result, "🕛 12:15 AM (12 hours ago)")


if __name__ == "__main__":
    unittest.main()
