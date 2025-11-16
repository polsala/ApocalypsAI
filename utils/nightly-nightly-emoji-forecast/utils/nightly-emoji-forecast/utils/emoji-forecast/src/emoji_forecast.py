"""
Emoji Forecast Utility
"""

from datetime import datetime
from typing import Dict

# Mock weather description → emoji mapping
_WEATHER_EMOJI_MAP: Dict[str, str] = {
    "sunny": "☀️",
    "clear": "☀️",
    "partly cloudy": "⛅",
    "cloudy": "☁️",
    "rain": "🌧️",
    "rainy": "🌧️",
    "storm": "⛈️",
    "snow": "❄️",
    "snowy": "❄️",
    "fog": "🌫️",
    "windy": "🌬️",
    "unknown": "❓",
}


def _fetch_weather(date: str, location: str) -> str:
    """Mock function to fetch a weather description.

    In a real implementation this would call an external API. For offline deterministic
    behavior it returns a pseudo‑weather based on the hash of the inputs.
    """
    # Simple deterministic pseudo‑weather based on the sum of character codes
    hash_val = sum(ord(c) for c in date + location) % len(_WEATHER_EMOJI_MAP)
    weather = list(_WEATHER_EMOJI_MAP.keys())[hash_val]
    return weather


def get_emoji_forecast(date: str, location: str) -> str:
    """Return an emoji representing the weather forecast for *date* and *location*.

    Args:
        date: A string in ``YYYY-MM-DD`` format.
        location: Arbitrary location name.

    Raises:
        ValueError: If *date* is not in the required format.
    """
    # Validate date format
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("date must be in YYYY-MM-DD format") from exc

    weather = _fetch_weather(date, location)
    return _WEATHER_EMOJI_MAP.get(weather, _WEATHER_EMOJI_MAP["unknown"])


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python -m utils.nightly_emoji_forecast.src.emoji_forecast <YYYY-MM-DD> <location>")
        sys.exit(1)
    date_arg, location_arg = sys.argv[1], sys.argv[2]
    print(get_emoji_forecast(date_arg, location_arg))
