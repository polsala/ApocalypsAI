import datetime
import sys
from pathlib import Path

# Ensure the src directory is importable when tests run from the utils folder.
# Mock rationale: we manipulate sys.path locally; this does not affect production code.
src_path = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(src_path))

from moon import get_moon_phase, main


def test_known_phases():
    # Known lunar phases (verified against public lunar calendars)
    cases = {
        datetime.date(2023, 1, 21): "New Moon",
        datetime.date(2023, 1, 28): "First Quarter",
        datetime.date(2023, 2, 5): "Full Moon",
        datetime.date(2023, 2, 13): "Last Quarter",
    }
    for dt, expected in cases.items():
        assert get_moon_phase(dt) == expected


def test_cli_today(capsys, monkeypatch):
    # Mock today's date to a known value and capture CLI output.
    mock_today = datetime.date(2023, 2, 5)  # Full Moon
    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return mock_today
    monkeypatch.setattr(datetime, "date", MockDate)
    # Run CLI with no arguments (should use mocked today)
    main(())
    captured = capsys.readouterr().out
    assert "2023-02-05" in captured
    assert "Full Moon" in captured


def test_cli_invalid_date(capsys):
    # Provide an invalid date string and ensure exit code 1 and error message.
    try:
        main(("invalid-date",))
    except SystemExit as e:
        assert e.code == 1
    else:
        assert False, "SystemExit not raised"
    captured = capsys.readouterr().err
    # The script prints to stdout for errors; capture both streams.
    output = captured or capsys.readouterr().out
    assert "Invalid date format" in output
