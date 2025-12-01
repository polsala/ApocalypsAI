import datetime
from unittest import mock

# Import the module using its package path relative to the test runner.
from src.forecast import get_forecast, _seed_from_date, EMOJIS


def test_mocked_seed():
    """Ensure the forecast logic respects the derived indices.

    We mock the internal seed function to a known value so the output is predictable.
    """
    date = datetime.date(2023, 1, 1)
    # Mock rationale: replace the hash‑based seed with a constant to avoid reliance on MD5.
    with mock.patch('src.forecast._seed_from_date', return_value=0x12345678):
        forecast = get_forecast(date)
        # Seed 0x12345678 => binary ... 0001 0010 0011 0100 0101 0110 0111 1000
        # Extracted 4‑bit chunks (least‑significant first): 0x8, 0x7, 0x6
        # Map to emojis list (mod length): indices 8, 7, 6 -> "❄️", "🌩️", "⛈️"
        assert forecast == "❄️🌩️⛈️"


def test_forecast_is_three_emojis():
    """A normal (non‑mocked) date should always return exactly three emojis."""
    today = datetime.date.today()
    forecast = get_forecast(today)
    # Each emoji is a single Unicode grapheme; length of the string should be 3 characters.
    assert len(forecast) == 3
    # Ensure each character is one of the allowed emojis.
    for char in forecast:
        assert char in EMOJIS
