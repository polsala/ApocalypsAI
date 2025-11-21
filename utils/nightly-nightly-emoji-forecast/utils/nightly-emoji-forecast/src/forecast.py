#!/usr/bin/env python3
"""Emoji weather forecast utility.

Provides a function ``get_emoji_forecast(city)`` that returns an emoji
representing the current temperature for *city*.
"""

import sys
import requests


def _fetch_weather(city: str) -> dict:
    """Fetch weather data from a (mocked) API.

    The real endpoint is a placeholder; during testing the ``requests.get``
    call is patched to return deterministic data.
    """
    url = f"https://api.example.com/weather?city={city}"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return resp.json()


def _temp_to_emoji(temp_c: float) -> str:
    """Map a temperature in Celsius to an emoji."""
    if temp_c < 0:
        return "🥶"
    if temp_c < 10:
        return "🧣"
    if temp_c < 20:
        return "🌤️"
    if temp_c < 30:
        return "☀️"
    return "🔥"


def get_emoji_forecast(city: str) -> str:
    """Return an emoji representing the current weather for *city*.

    Raises ``ValueError`` if the API response does not contain a temperature.
    """
    data = _fetch_weather(city)
    temp = data.get("temperature_c")
    if temp is None:
        raise ValueError("Missing temperature in response")
    return _temp_to_emoji(temp)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m forecast <city>")
        sys.exit(1)
    city = sys.argv[1]
    try:
        emoji = get_emoji_forecast(city)
        print(f"Weather in {city}: {emoji}")
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
