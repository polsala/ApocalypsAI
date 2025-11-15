import datetime
from unittest import mock

# Mock rationale: we replace datetime.datetime.utcnow to return a fixed timestamp
# so the test runs deterministically offline.

from utils.nightly-emoji-clock.src.emoji_clock import get_emoji_time

def test_get_emoji_time_fixed_datetime():
    fixed_dt = datetime.datetime(2025, 1, 1, 14, 22)  # 14:22 UTC
    with mock.patch('datetime.datetime') as mock_dt:
        # Configure the mock to return our fixed datetime for utcnow()
        mock_dt.utcnow.return_value = fixed_dt
        # Ensure other datetime constructors behave normally
        mock_dt.side_effect = lambda *args, **kwargs: datetime.datetime(*args, **kwargs)
        result = get_emoji_time()
        # 14:22 rounds hour up to 15 (🕒) and minute to 30 (🕧)
        assert result == "🕒🕧"

def test_get_emoji_time_edge_cases():
    # 00:04 -> hour 0 (🕛), minute 0 (🕛)
    dt1 = datetime.datetime(2025, 1, 1, 0, 4)
    # 23:45 -> hour rounds to 0 (🕛), minute 30 (🕧)
    dt2 = datetime.datetime(2025, 1, 1, 23, 45)
    assert get_emoji_time(dt1) == "🕛🕛"
    assert get_emoji_time(dt2) == "🕛🕧"
