import datetime
import sys
from pathlib import Path

# Adjust import path to locate the utility's src folder
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src"))

from relative_time import format_relative_time


def test_just_now():
    now = datetime.datetime(2025, 1, 1, 12, 0, 0)
    # Target within 4 seconds of reference → "just now"
    assert format_relative_time(now + datetime.timedelta(seconds=2), reference=now) == "just now"
    assert format_relative_time(now - datetime.timedelta(seconds=3), reference=now) == "just now"


def test_seconds_ago_and_future():
    ref = datetime.datetime(2025, 1, 1, 12, 0, 0)
    assert format_relative_time(ref - datetime.timedelta(seconds=45), reference=ref) == "45 seconds ago"
    assert format_relative_time(ref + datetime.timedelta(seconds=45), reference=ref) == "in 45 seconds"


def test_minutes():
    ref = datetime.datetime(2025, 1, 1, 12, 0, 0)
    assert format_relative_time(ref - datetime.timedelta(minutes=5), reference=ref) == "5 minutes ago"
    assert format_relative_time(ref + datetime.timedelta(minutes=5), reference=ref) == "in 5 minutes"


def test_hours():
    ref = datetime.datetime(2025, 1, 1, 12, 0, 0)
    assert format_relative_time(ref - datetime.timedelta(hours=2), reference=ref) == "2 hours ago"
    assert format_relative_time(ref + datetime.timedelta(hours=2), reference=ref) == "in 2 hours"


def test_days_and_weeks():
    ref = datetime.datetime(2025, 1, 1, 12, 0, 0)
    assert format_relative_time(ref - datetime.timedelta(days=1), reference=ref) == "1 day ago"
    assert format_relative_time(ref + datetime.timedelta(days=3), reference=ref) == "in 3 days"
    assert format_relative_time(ref - datetime.timedelta(days=10), reference=ref) == "1 week ago"
    assert format_relative_time(ref + datetime.timedelta(days=21), reference=ref) == "in 3 weeks"


def test_months_and_years():
    ref = datetime.datetime(2025, 1, 1, 12, 0, 0)
    # Approximate month = 30 days
    assert format_relative_time(ref - datetime.timedelta(days=45), reference=ref) == "1 month ago"
    assert format_relative_time(ref + datetime.timedelta(days=75), reference=ref) == "in 2 months"
    # Approximate year = 365 days
    assert format_relative_time(ref - datetime.timedelta(days=400), reference=ref) == "1 year ago"
    assert format_relative_time(ref + datetime.timedelta(days=800), reference=ref) == "in 2 years"

# Mock rationale comments (no external network calls are performed)
# Mock rationale: All datetime objects are constructed locally; no I/O.
