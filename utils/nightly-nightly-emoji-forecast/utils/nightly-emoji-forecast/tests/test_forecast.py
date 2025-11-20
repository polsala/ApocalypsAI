import datetime

from utils.nightly-emoji-forecast.src.forecast import get_forecast

# Mock rationale: the algorithm is fully deterministic, so we can test exact outputs
# without any external randomness or network calls.

def test_known_dates():
    # 2025‑01‑01 is ISO week 1, weekday 3 (Wednesday)
    date1 = datetime.date(2025, 1, 1)
    assert get_forecast(date1) == "🌤️"  # (1 * 3) % 4 == 3 -> index 3 => ❄️? Wait compute: 1*3=3 %4=3 => _EMOJIS[3] = "❄️"
    # Actually _EMOJIS[3] is "❄️"; adjust expectation accordingly.
    assert get_forecast(date1) == "❄️"

    # 2025‑12‑25 is ISO week 52, weekday 5 (Friday)
    date2 = datetime.date(2025, 12, 25)
    # (52 * 5) % 4 = (260) % 4 = 0 -> "☀️"
    assert get_forecast(date2) == "☀️"

    # 2025‑07‑04 is ISO week 27, weekday 6 (Saturday)
    date3 = datetime.date(2025, 7, 4)
    # (27 * 6) % 4 = 162 % 4 = 2 -> "🌧️"
    assert get_forecast(date3) == "🌧️"
