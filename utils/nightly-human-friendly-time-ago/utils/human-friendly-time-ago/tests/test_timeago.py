import datetime
import pytest
from utils.human-friendly-time-ago.src.timeago import time_ago

# Mock rationale: All tests are deterministic by providing an explicit ``now`` argument.

@pytest.fixture
def fixed_now():
    # Fixed reference point: 2025‑01‑01 12:00:00 UTC
    return datetime.datetime(2025, 1, 1, 12, 0, 0)


def test_just_now(fixed_now):
    assert time_ago(fixed_now, now=fixed_now, emoji=False) == "just now"
    assert time_ago(fixed_now - datetime.timedelta(seconds=5), now=fixed_now, emoji=False) == "just now"


def test_seconds_ago(fixed_now):
    ts = fixed_now - datetime.timedelta(seconds=42)
    assert time_ago(ts, now=fixed_now, emoji=False) == "42s ago"


def test_minutes_ago(fixed_now):
    ts = fixed_now - datetime.timedelta(minutes=7, seconds=15)
    assert time_ago(ts, now=fixed_now, emoji=False) == "7\u202Fmin ago"


def test_hours_ago(fixed_now):
    ts = fixed_now - datetime.timedelta(hours=3, minutes=5)
    assert time_ago(ts, now=fixed_now, emoji=False) == "3\u202Fh ago"


def test_yesterday(fixed_now):
    ts = fixed_now - datetime.timedelta(days=1, hours=2)
    assert time_ago(ts, now=fixed_now, emoji=False) == "yesterday"


def test_multiple_days(fixed_now):
    ts = fixed_now - datetime.timedelta(days=4)
    assert time_ago(ts, now=fixed_now, emoji=False) == "4\u202Fdays ago"


def test_date_format(fixed_now):
    ts = datetime.datetime(2023, 12, 25, 9, 30, 0)
    assert time_ago(ts, now=fixed_now, emoji=False) == "on Dec\u202F25,\u202F2023"


def test_iso_string_input(fixed_now):
    iso = (fixed_now - datetime.timedelta(minutes=3)).isoformat()
    assert time_ago(iso, now=fixed_now, emoji=False) == "3\u202Fmin ago"


def test_future_timestamp(fixed_now):
    future = fixed_now + datetime.timedelta(hours=1)
    # Future times are treated as "just now"
    assert time_ago(future, now=fixed_now, emoji=False) == "just now"
