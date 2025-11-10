import datetime
from unittest import mock

# Mock rationale: we patch datetime.datetime.utcnow to return a deterministic "now" value.
# This ensures the tests are deterministic and offline.

from utils.emoji_time_ago.src.main import time_ago

FIXED_NOW = datetime.datetime(2023, 1, 1, 12, 0, 0)  # UTC naive

def _mock_utcnow():
    return FIXED_NOW

def test_seconds_ago():
    ts = "2023-01-01T11:59:30Z"  # 30 seconds before FIXED_NOW
    with mock.patch("utils.emoji_time_ago.src.main.datetime.datetime") as mock_dt:
        mock_dt.utcnow.side_effect = _mock_utcnow
        mock_dt.fromisoformat.side_effect = datetime.datetime.fromisoformat
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
        result = time_ago(ts)
    assert result == "⏱️ 30 seconds ago"

def test_minutes_ago():
    ts = "2023-01-01T11:55:00Z"  # 5 minutes before FIXED_NOW
    with mock.patch("utils.emoji_time_ago.src.main.datetime.datetime") as mock_dt:
        mock_dt.utcnow.side_effect = _mock_utcnow
        mock_dt.fromisoformat.side_effect = datetime.datetime.fromisoformat
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
        result = time_ago(ts)
    assert result == "🕐 5 minutes ago"

def test_hours_ago():
    ts = "2023-01-01T09:00:00Z"  # 3 hours before FIXED_NOW
    with mock.patch("utils.emoji_time_ago.src.main.datetime.datetime") as mock_dt:
        mock_dt.utcnow.side_effect = _mock_utcnow
        mock_dt.fromisoformat.side_effect = datetime.datetime.fromisoformat
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
        result = time_ago(ts)
    assert result == "🕑 3 hours ago"

def test_days_ago():
    ts = "2022-12-28T12:00:00Z"  # 4 days before FIXED_NOW
    with mock.patch("utils.emoji_time_ago.src.main.datetime.datetime") as mock_dt:
        mock_dt.utcnow.side_effect = _mock_utcnow
        mock_dt.fromisoformat.side_effect = datetime.datetime.fromisoformat
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
        result = time_ago(ts)
    assert result == "📅 4 days ago"

def test_future_timestamp():
    ts = "2023-01-01T12:05:00Z"  # 5 minutes in the future
    with mock.patch("utils.emoji_time_ago.src.main.datetime.datetime") as mock_dt:
        mock_dt.utcnow.side_effect = _mock_utcnow
        mock_dt.fromisoformat.side_effect = datetime.datetime.fromisoformat
        mock_dt.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)
        result = time_ago(ts)
    # Future timestamps are treated as "just now"
    assert result == "⏱️ just now"
