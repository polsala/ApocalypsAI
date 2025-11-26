import datetime
from unittest import mock

from utils.nightly-emoji-forecast.src.forecast import get_forecast

def test_known_date():
    """Ensure a known date maps to the expected forecast."""
    date = datetime.date(2023, 1, 1)  # ordinal 738521 -> index 1
    assert get_forecast(date) == "🌧️ Rainy"

def test_today_uses_mocked_date():
    """# Mock rationale: replace datetime.date.today to guarantee deterministic output."""
    mock_today = datetime.date(2022, 12, 25)  # ordinal 738486 -> 738486 % 5 = 1 -> "🌧️ Rainy"
    with mock.patch("utils.nightly-emoji-forecast.src.forecast.datetime.date") as mock_date:
        mock_date.today.return_value = mock_today
        # Preserve normal constructor behavior for other calls
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        assert get_forecast(mock_date.today()) == "🌧️ Rainy"
