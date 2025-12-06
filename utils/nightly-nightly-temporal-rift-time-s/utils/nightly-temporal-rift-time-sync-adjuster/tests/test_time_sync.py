import pytest
import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

from src.time_sync import get_current_times, convert_time

# Mock rationale: We need deterministic results for 'current time' tests.
# By patching datetime.datetime.now, we ensure the test always runs with the same reference time.
@pytest.fixture
def mock_datetime_now():
    fixed_utc_now = datetime.datetime(2024, 7, 20, 10, 30, 0, tzinfo=datetime.timezone.utc)
    with patch('datetime.datetime') as mock_dt:
        # Configure mock_dt.now to return aware datetimes when a timezone is passed,
        # and a naive datetime otherwise, mimicking real behavior.
        mock_dt.now.side_effect = lambda tz=None: fixed_utc_now if tz == datetime.timezone.utc else fixed_utc_now.astimezone(tz) if tz else fixed_utc_now.replace(tzinfo=None)
        # Ensure other datetime methods are not mocked out, as they are used by the utility.
        mock_dt.strptime = datetime.datetime.strptime
        mock_dt.fromtimestamp = datetime.datetime.fromtimestamp
        mock_dt.utcfromtimestamp = datetime.datetime.utcfromtimestamp
        mock_dt.fromisoformat = datetime.datetime.fromisoformat
        yield mock_dt


def test_get_current_times_valid_zones(mock_datetime_now):
    zones = ["UTC", "Europe/London", "America/New_York"]
    times = get_current_times(zones)

    assert len(times) == 3
    assert "UTC" in times
    assert "Europe/London" in times
    assert "America/New_York" in times

    # Expected times based on fixed_utc_now = 2024-07-20 10:30:00 UTC
    assert times["UTC"] == datetime.datetime(2024, 7, 20, 10, 30, 0, tzinfo=ZoneInfo("UTC"))
    assert times["Europe/London"] == datetime.datetime(2024, 7, 20, 11, 30, 0, tzinfo=ZoneInfo("Europe/London")) # UTC+1
    assert times["America/New_York"] == datetime.datetime(2024, 7, 20, 6, 30, 0, tzinfo=ZoneInfo("America/New_York")) # UTC-4


def test_get_current_times_invalid_zone():
    zones = ["Invalid/Zone"]
    with pytest.raises(ValueError, match="Invalid time zone: Invalid/Zone"):
        get_current_times(zones)


def test_convert_time_basic_conversion():
    dt_str = "2024-07-20 10:00"
    from_tz_str = "UTC"
    to_tz_strs = ["Europe/Berlin", "Asia/Tokyo"]
    converted = convert_time(dt_str, from_tz_str, to_tz_strs)

    assert "original" in converted
    assert "Europe/Berlin" in converted
    assert "Asia/Tokyo" in converted

    original_dt = datetime.datetime(2024, 7, 20, 10, 0, 0, tzinfo=ZoneInfo("UTC"))
    assert converted["original"] == original_dt
    assert converted["Europe/Berlin"] == datetime.datetime(2024, 7, 20, 12, 0, 0, tzinfo=ZoneInfo("Europe/Berlin")) # UTC+2
    assert converted["Asia/Tokyo"] == datetime.datetime(2024, 7, 20, 19, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo")) # UTC+9


def test_convert_time_different_input_format():
    dt_str = "2024/07/20 10-00-00"
    dt_format = "%Y/%m/%d %H-%M-%S"
    from_tz_str = "America/Los_Angeles"
    to_tz_strs = ["UTC"]
    converted = convert_time(dt_str, from_tz_str, to_tz_strs, dt_format=dt_format)

    original_dt = datetime.datetime(2024, 7, 20, 10, 0, 0, tzinfo=ZoneInfo("America/Los_Angeles")) # UTC-7
    assert converted["original"] == original_dt
    assert converted["UTC"] == datetime.datetime(2024, 7, 20, 17, 0, 0, tzinfo=ZoneInfo("UTC"))


def test_convert_time_invalid_from_zone():
    dt_str = "2024-07-20 10:00"
    from_tz_str = "Bad/Zone"
    to_tz_strs = ["UTC"]
    with pytest.raises(ValueError, match="Invalid time zone: Bad/Zone"):
        convert_time(dt_str, from_tz_str, to_tz_strs)


def test_convert_time_invalid_to_zone():
    dt_str = "2024-07-20 10:00"
    from_tz_str = "UTC"
    to_tz_strs = ["Another/Bad/Zone"]
    with pytest.raises(ValueError, match="Invalid time zone: Another/Bad/Zone"):
        convert_time(dt_str, from_tz_str, to_tz_strs)


def test_convert_time_invalid_datetime_format():
    dt_str = "2024-07-20 10-00" # Mismatch with default format '%Y-%m-%d %H:%M'
    from_tz_str = "UTC"
    to_tz_strs = ["Europe/Berlin"]
    with pytest.raises(ValueError, match="Invalid datetime format or value"):
        convert_time(dt_str, from_tz_str, to_tz_strs)


def test_convert_time_non_existent_time_due_to_dst():
    # Example: March 10, 2024, 2:30 AM in America/New_York (spring forward, 2:00 AM -> 3:00 AM)
    # The naive time 2:30 AM on March 10, 2024, does not exist in America/New_York due to DST.
    dt_str = "2024-03-10 02:30"
    from_tz_str = "America/New_York"
    to_tz_strs = ["UTC"]

    with pytest.raises(ValueError, match="datetime is ambiguous or non-existent"):
        convert_time(dt_str, from_tz_str, to_tz_strs)


def test_convert_time_ambiguous_time_due_to_dst():
    # Example: November 3, 2024, 1:30 AM in America/New_York (fall back, 2:00 AM -> 1:00 AM twice)
    # The naive time 1:30 AM on November 3, 2024, occurs twice in America/New_York due to DST.
    dt_str = "2024-11-03 01:30"
    from_tz_str = "America/New_York"
    to_tz_strs = ["UTC"]

    with pytest.raises(ValueError, match="datetime is ambiguous or non-existent"):
        convert_time(dt_str, from_tz_str, to_tz_strs)
