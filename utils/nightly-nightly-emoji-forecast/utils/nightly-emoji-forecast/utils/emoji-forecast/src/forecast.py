"""
emoji_forecast utility
Provides deterministic emoji weather forecasts based on the date.
"""

import datetime
from typing import Tuple

# Define weather conditions and associated emojis
_WEATHER_CONDITIONS: Tuple[Tuple[str, str], ...] = (
    ("Sunny", "☀️"),
    ("Cloudy", "☁️"),
    ("Rainy", "🌧️"),
    ("Snowy", "❄️"),
    ("Stormy", "⛈️"),
)

# Temperature emoji mapping thresholds
def _temp_emoji(temp_c: int) -> str:
    if temp_c < 0:
        return "🥶"
    if temp_c < 15:
        return "🧥"
    return "🌡️"


def get_emoji_forecast(date: datetime.date) -> str:
    """
    Return an emoji string representing the weather forecast for the given date.

    The algorithm is fully deterministic and offline:
    * Choose a weather condition based on the day of year.
    * Derive a pseudo temperature from the day of year.
    * Map temperature to an emoji.
    """
    day_of_year = date.timetuple().tm_yday
    # Select weather condition
    weather_idx = (day_of_year - 1) % len(_WEATHER_CONDITIONS)
    _, weather_emoji = _WEATHER_CONDITIONS[weather_idx]

    # Pseudo temperature: range -10..29°C
    pseudo_temp = (day_of_year % 40) - 10
    temp_emoji = _temp_emoji(pseudo_temp)

    return f"{weather_emoji}{temp_emoji}"


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m src.forecast <YYYY-MM-DD>")
        sys.exit(1)
    try:
        input_date = datetime.date.fromisoformat(sys.argv[1])
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        sys.exit(1)
    print(get_emoji_forecast(input_date))
