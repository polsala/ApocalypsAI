import pytest
from timezone_converter.convert import convert_time

# Mock rationale: All tests use fixed timestamps and well‑known IANA zones.
# The zoneinfo database is part of the Python standard library and works offline.

@pytest.mark.parametrize(
    "dt_str, from_tz, to_tz, expected",
    [
        # UTC to UTC – no offset change
        ("2025-01-01 12:00:00", "UTC", "UTC", "2025-01-01 12:00:00+0000"),
        # UTC to Europe/London in winter (UTC+0)
        ("2025-01-01 12:00:00", "UTC", "Europe/London", "2025-01-01 12:00:00+0000"),
        # UTC to Europe/London in summer (UTC+1)
        ("2025-07-01 12:00:00", "UTC", "Europe/London", "2025-07-01 13:00:00+0100"),
        # New York (EST, UTC‑5) to Tokyo (JST, UTC+9)
        ("2025-01-01 15:30:00", "America/New_York", "Asia/Tokyo", "2025-01-02 05:30:00+0900"),
    ],
)
def test_convert_time(dt_str, from_tz, to_tz, expected):
    assert convert_time(dt_str, from_tz, to_tz) == expected

def test_invalid_format():
    with pytest.raises(ValueError):
        convert_time("2025/01/01 12:00:00", "UTC", "UTC")

def test_invalid_timezone():
    with pytest.raises(ValueError):
        convert_time("2025-01-01 12:00:00", "Invalid/Zone", "UTC")
