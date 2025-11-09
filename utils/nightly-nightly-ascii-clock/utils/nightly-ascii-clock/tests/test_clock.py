import datetime
from unittest import mock

# Mock rationale: we replace datetime.datetime.now with a fixed timestamp so the test is deterministic and offline.

from utils.nightly_ascii_clock.src.clock import ascii_time, main


def test_ascii_time_fixed_timestamp():
    fixed_dt = datetime.datetime(2023, 1, 1, 14, 35)  # 14:35
    expected_output = (
        " _   _       _   _ \n"
        "| | | |   | | | | |\n"
        "|_| |_|   |_| |_| |"
    )
    assert ascii_time(fixed_dt) == expected_output


def test_main_prints_current_time(monkeypatch, capsys):
    # Mock datetime.datetime.now to return a known time.
    mock_now = datetime.datetime(2022, 12, 31, 23, 59)
    class MockDateTime(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return mock_now
    monkeypatch.setattr(datetime, "datetime", MockDateTime)

    # Run the CLI main function.
    exit_code = main([])
    captured = capsys.readouterr()
    expected = (
        " _   _   _   _   _   _ \n"
        "|_| |_| |_| |_| |_| |_|\n"
        " _   _   _   _   _   _ "
    )
    # The expected pattern for 23:59 ("23:59")
    assert captured.out.strip() == expected.strip()
    assert exit_code == 0
