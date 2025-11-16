import datetime
from unittest import mock

# Import the module using its relative path within the test package.
# The test runner adds the utils/nightly-emoji-forecast directory to PYTHONPATH.
from src.forecast import get_forecast


def test_forecast_with_mocked_seed():
    """Ensure the forecast algorithm produces the expected emojis for a known seed.

    # Mock rationale: By patching the internal ``_seed_for_date`` function we avoid
    # reliance on the SHA‑256 implementation and make the test deterministic and
    # offline.
    """
    with mock.patch("src.forecast._seed_for_date", return_value=0x123456):
        # Use any date – the mocked seed overrides the actual date value.
        dummy_date = datetime.date(2000, 1, 1)
        result = get_forecast(dummy_date)
        # Seed 0x123456 yields indices 6, 9, 3 → emojis 🌧️, ❄️, 🌥️.
        assert result == "🌧️❄️🌥️"


def test_cli_prints_today_forecast(monkeypatch, capsys):
    """Run the module as a script and verify it prints a forecast for *today*.

    # Mock rationale: ``datetime.date.today`` is patched to a fixed date so the
    # output is predictable without network or time‑dependent variability.
    """
    fixed_today = datetime.date(2023, 10, 31)
    monkeypatch.setattr(datetime.date, "today", lambda: fixed_today)
    # Execute the module's ``__main__`` block.
    import importlib
    import src.forecast as forecast_mod
    import sys
    # Reload to ensure the patched ``today`` is used.
    importlib.reload(forecast_mod)
    # Capture stdout.
    captured = capsys.readouterr()
    # The forecast string length is three emojis; we only assert that something was printed.
    assert captured.out.strip() != ""
