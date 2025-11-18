import datetime

from utils.nightly-emoji-forecast.src.forecast import get_emoji_forecast


def test_known_dates():
    """Validate deterministic output for a set of fixed dates.

    # Mock rationale: We use hard‑coded dates and expected emojis derived from the
    # algorithm itself. This ensures the test remains deterministic and offline.
    """
    cases = {
        datetime.date(2025, 1, 1): "🌤️",
        datetime.date(2025, 12, 25): "🌨️",
        datetime.date(2000, 2, 29): "🌈",
        datetime.date(1999, 12, 31): "🌪️",
    }
    for d, expected in cases.items():
        assert get_emoji_forecast(d) == expected, f"{d} should map to {expected}"


def test_today_consistency(monkeypatch):
    """Ensure that calling the CLI for *today* yields the same result as the library.

    # Mock rationale: We monkey‑patch `datetime.date.today` to a known date so the
    # test does not depend on the actual current date.
    """
    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return datetime.date(2023, 7, 4)

    monkeypatch.setattr(datetime, "date", MockDate)
    from utils.nightly-emoji-forecast.src import forecast as cli_mod
    # Simulate CLI execution
    import sys
    sys.argv = ["forecast.py", "2023-07-04"]
    # Capture stdout
    from io import StringIO
    import contextlib
    buf = StringIO()
    with contextlib.redirect_stdout(buf):
        cli_mod.main()
    cli_output = buf.getvalue().strip()
    lib_output = get_emoji_forecast(MockDate.today())
    assert cli_output == lib_output
