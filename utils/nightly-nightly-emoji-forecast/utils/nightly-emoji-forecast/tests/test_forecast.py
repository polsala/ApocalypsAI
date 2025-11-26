import datetime
from src.forecast import get_emoji_forecast


def test_known_date():
    # 2023-01-01 => (2023 + 1 + 1) % 8 = 1 => "🌤️"
    date = datetime.date(2023, 1, 1)
    assert get_emoji_forecast(date) == "🌤️"


def test_today_mock(monkeypatch):
    # Mock rationale: replace date.today to ensure deterministic test.
    mock_date = datetime.date(2022, 12, 30)  # (2022+12+30) % 8 = 0 => "☀️"

    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return mock_date

    monkeypatch.setattr(datetime, "date", MockDate)
    assert get_emoji_forecast(datetime.date.today()) == "☀️"
