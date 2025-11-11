"""Tests for the Emoji Calendar utility."""

import datetime
from unittest import mock

# Import the function under test
from src.emoji_calendar import get_emoji_for_date


def test_weekday_emojis():
    """Ensure each weekday maps to the correct emoji."""
    # Monday 2025-01-06
    monday = datetime.date(2025, 1, 6)
    assert get_emoji_for_date(monday) == "📅"

    # Tuesday 2025-01-07
    tuesday = datetime.date(2025, 1, 7)
    assert get_emoji_for_date(tuesday) == "🗓️"

    # Wednesday 2025-01-08
    wednesday = datetime.date(2025, 1, 8)
    assert get_emoji_for_date(wednesday) == "📆"

    # Thursday 2025-01-09
    thursday = datetime.date(2025, 1, 9)
    assert get_emoji_for_date(thursday) == "🗒️"

    # Friday 2025-01-10
    friday = datetime.date(2025, 1, 10)
    assert get_emoji_for_date(friday) == "📖"

    # Saturday 2025-01-11
    saturday = datetime.date(2025, 1, 11)
    assert get_emoji_for_date(saturday) == "🛌"

    # Sunday 2025-01-12
    sunday = datetime.date(2025, 1, 12)
    assert get_emoji_for_date(sunday) == "☀️"


def test_holiday_overrides_weekday():
    """Holiday emojis should take precedence over weekday emojis."""
    # New Year's Day 2025-01-01 is a Wednesday but should return 🎉
    new_year = datetime.date(2025, 1, 1)
    assert get_emoji_for_date(new_year) == "🎉"

    # Christmas 2025-12-25 is a Thursday but should return 🎄
    christmas = datetime.date(2025, 12, 25)
    assert get_emoji_for_date(christmas) == "🎄"


def test_cli_uses_today_when_no_arg(monkeypatch):
    """CLI should default to today's date when no argument is given."""
    # Mock datetime.date.today() to a known date
    mock_today = datetime.date(2025, 2, 14)  # Friday
    with mock.patch("datetime.date") as mock_date:
        # # Mock rationale: we replace today() while preserving other date constructors
        mock_date.today.return_value = mock_today
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        # Import the CLI entry point lazily to pick up the mock
        from src import emoji_calendar as ec
        # Capture stdout
        with mock.patch("builtins.print") as mock_print:
            ec.main()
            mock_print.assert_called_once_with("📖")  # Friday emoji
