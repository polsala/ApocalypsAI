"""emoji_forecast – map weather descriptions to emojis.

Provides a simple `forecast` function and a tiny CLI.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict

# Mapping of normalized weather phrases to emojis. Longer keys should appear before shorter ones
_WEATHER_MAP: Dict[str, str] = {
    "partly cloudy": "🌤️",
    "light rain": "🌧️",
    "heavy rain": "🌧️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "fog": "🌫️",
    "windy": "🌬️",
    "sunny": "☀️",
    "clear": "☀️",
    "cloudy": "☁️",
    "overcast": "☁️",
    "rain": "🌧️",
}

def _normalize(text: str) -> str:
    """Return a lower‑cased, stripped version of *text* for matching."""
    return text.strip().lower()

def forecast(description: str) -> str:
    """Return an emoji representing *description*.

    The function looks for the longest matching key in ``_WEATHER_MAP``.
    If nothing matches, it returns the *unknown* emoji ``❓``.
    """
    norm = _normalize(description)
    # Sort keys by length descending to prefer longer matches
    for key in sorted(_WEATHER_MAP, key=len, reverse=True):
        if key in norm:
            return _WEATHER_MAP[key]
    return "❓"

def _cli() -> None:
    parser = argparse.ArgumentParser(description="Convert a weather description to an emoji.")
    parser.add_argument("description", help="Plain‑language weather description, e.g. 'light rain'")
    args = parser.parse_args()
    emoji = forecast(args.description)
    print(emoji)

if __name__ == "__main__":
    # When executed as a module: python -m emoji_forecast "sunny"
    _cli()
