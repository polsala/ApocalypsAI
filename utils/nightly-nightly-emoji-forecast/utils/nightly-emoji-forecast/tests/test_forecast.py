import pytest
from utils.nightly-emoji-forecast.src import forecast


def test_forecast_with_mocked_seed(monkeypatch):
    """Ensure the deterministic selection logic works as expected.

    We mock ``_seed_from_date`` to return a known integer so the emoji indices are predictable.
    """
    # Mock rationale: By fixing the seed we avoid any dependence on the actual hash of a date.
    def mock_seed(_):
        # Arbitrary 48‑bit value: 0x12345678ABCDEF
        return 0x12345678ABCDEF

    monkeypatch.setattr(forecast, "_seed_from_date", mock_seed)

    # The seed yields the following byte windows (little‑endian view):
    #   byte0 = 0xEF -> 239 % 10 = 9 -> "🌈"
    #   byte1 = 0xCD -> 205 % 10 = 5 -> "🌧️"
    #   byte2 = 0xAB -> 171 % 10 = 1 -> "🌤️"
    expected = "🌈🌧️🌤️"
    result = forecast.get_forecast("2099-12-31")
    assert result == expected


def test_default_uses_utc_today(monkeypatch):
    """Verify that calling ``get_forecast()`` without arguments uses ``datetime.utcnow``.

    We monkey‑patch ``datetime.utcnow`` to a fixed date and check the output.
    """
    class DummyDateTime(datetime):
        @classmethod
        def utcnow(cls):
            return datetime(2025, 11, 27)  # Fixed date for reproducibility

    # Mock rationale: Replacing ``datetime.utcnow`` isolates the function from the real clock.
    monkeypatch.setattr(forecast, "datetime", DummyDateTime)

    # With the deterministic date, the seed is derived from "2025-11-27".
    # Compute expected emojis using the same algorithm.
    seed = forecast._seed_from_date("2025-11-27")
    emojis = []
    for i in range(3):
        idx = (seed >> (i * 8)) % len(forecast.EMOJI_MAP)
        emojis.append(forecast.EMOJI_MAP[idx])
    expected = "".join(emojis)

    result = forecast.get_forecast()
    assert result == expected
