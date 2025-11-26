import datetime
import pytest
from src.forecast import generate_forecast, _pick_emojis


def test_pick_emojis_is_deterministic():
    seed = 123456
    first = _pick_emojis(seed)
    second = _pick_emojis(seed)
    assert first == second, "Same seed should produce identical emoji lists"


def test_generate_forecast_returns_three_valid_emojis():
    date = datetime.date(2023, 1, 1)
    forecast = generate_forecast(date)
    parts = forecast.split()
    assert len(parts) == 3, "Forecast should contain exactly three emojis"
    for emoji in parts:
        assert emoji in [
            "☀️",
            "🌤️",
            "⛅",
            "🌥️",
            "🌧️",
            "⛈️",
            "❄️",
            "🌪️",
            "🌈",
            "🌫️",
        ], f"Unexpected emoji {emoji}"


def test_generate_forecast_is_consistent_for_same_date():
    date = datetime.date(2025, 12, 31)
    first = generate_forecast(date)
    second = generate_forecast(date)
    assert first == second, "Forecast must be deterministic for a given date"


def test_generate_forecast_uses_today_when_no_date(monkeypatch):
    # Mock today's date to a known value
    mock_today = datetime.date(2024, 2, 29)
    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return mock_today
    monkeypatch.setattr(datetime, "date", MockDate)
    forecast = generate_forecast()
    # Ensure we still get three valid emojis
    parts = forecast.split()
    assert len(parts) == 3
    for emoji in parts:
        assert emoji in [
            "☀️",
            "🌤️",
            "⛅",
            "🌥️",
            "🌧️",
            "⛈️",
            "❄️",
            "🌪️",
            "🌈",
            "🌫️",
        ]
