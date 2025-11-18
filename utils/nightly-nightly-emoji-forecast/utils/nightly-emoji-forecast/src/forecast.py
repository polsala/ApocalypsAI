"""
emoji_forecast utility

Provides a quick emoji representation of the current weather for a city.
"""

import argparse
from typing import Dict

# Mapping of weather condition keywords to emojis
_WEATHER_EMOJI_MAP: Dict[str, str] = {
    "clear": "☀️",
    "sunny": "☀️",
    "cloudy": "☁️",
    "overcast": "☁️",
    "rain": "🌧️",
    "drizzle": "🌦️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
    "fog": "🌫️",
    "unknown": "❓",
}


def _fetch_weather(city: str) -> str:
    """Placeholder for real weather fetching logic.

    Returns a lowercase weather condition string.
    In production this could call an API like OpenWeatherMap.
    """
    # Mock rationale: In offline mode we raise NotImplementedError so callers can handle it.
    raise NotImplementedError("Weather fetching not implemented. Patch this function in tests or provide a real implementation.")


def get_emoji_forecast(city: str) -> str:
    """Return an emoji representing the current weather in *city*.

    If the underlying fetch fails, the function falls back to the "unknown" emoji.
    """
    try:
        condition = _fetch_weather(city).lower()
    except Exception:
        condition = "unknown"
    return _WEATHER_EMOJI_MAP.get(condition, _WEATHER_EMOJI_MAP["unknown"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Get an emoji weather forecast for a city.")
    parser.add_argument("city", help="Name of the city to get the forecast for")
    args = parser.parse_args()
    emoji = get_emoji_forecast(args.city)
    print(f"{args.city}: {emoji}")


if __name__ == "__main__":
    main()
