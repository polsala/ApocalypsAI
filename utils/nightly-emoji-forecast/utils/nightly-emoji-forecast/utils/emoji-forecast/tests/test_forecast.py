import datetime
from src.forecast import generate_forecast


def test_known_date():
    """# Mock rationale: verify deterministic output for a fixed date."""
    date = datetime.date(2023, 1, 1)
    result = generate_forecast(date)
    assert result == "☀️ 22°C"


def test_today_mock(monkeypatch):
    """# Mock rationale: ensure generate_forecast uses datetime.date.today when no date supplied."""
    fake_today = datetime.date(2022, 12, 25)
    monkeypatch.setattr(datetime.date, "today", lambda: fake_today)
    result = generate_forecast()
    expected_temp = ((fake_today.toordinal() * 7) % 51) - 10
    if expected_temp < 0:
        expected_emoji = "❄️"
    elif expected_temp < 10:
        expected_emoji = "☁️"
    elif expected_temp < 20:
        expected_emoji = "🌤️"
    elif expected_temp < 30:
        expected_emoji = "☀️"
    else:
        expected_emoji = "🔥"
    assert result == f"{expected_emoji} {expected_temp}°C"
