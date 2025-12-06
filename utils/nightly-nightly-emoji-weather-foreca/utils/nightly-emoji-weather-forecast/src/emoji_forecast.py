#!/usr/bin/env python3
"""
emoji_forecast.py

Provides a function to map weather description strings to emojis.
"""

from __future__ import annotations

import sys
from typing import Dict

# Mapping of keywords to emojis
_WEATHER_EMOJI_MAP: Dict[str, str] = {
    "sunny": "☀️",
    "clear": "☀️",
    "partly cloudy": "🌤️",
    "cloudy": "🌤️",
    "rain": "🌧️",
    "drizzle": "🌧️",
    "light rain": "🌧️",
    "thunderstorm": "⛈️",
    "storm": "⛈️",
    "snow": "❄️",
    "flurries": "❄️",
    "fog": "🌫️",
    "mist": "🌫️",
}


def forecast_to_emoji(description: str) -> str:
    """Convert a weather description to an emoji.

    Parameters
    ----------
    description: str
        Human‑readable weather description (case‑insensitive).

    Returns
    -------
    str
        Emoji representing the weather, or ❓ if unknown.
    """
    desc = description.strip().lower()
    # Direct match
    if desc in _WEATHER_EMOJI_MAP:
        return _WEATHER_EMOJI_MAP[desc]
    # Keyword search: return first matching emoji
    for keyword, emoji in _WEATHER_EMOJI_MAP.items():
        if keyword in desc:
            return emoji
    return "❓"


def _cli() -> None:
    """Simple CLI for manual testing."""
    if len(sys.argv) != 2:
        print("Usage: python -m utils.nightly_emoji_weather_forecast.src.emoji_forecast \"<description>\"")
        sys.exit(1)
    description = sys.argv[1]
    print(forecast_to_emoji(description))


if __name__ == "__main__":
    _cli()
