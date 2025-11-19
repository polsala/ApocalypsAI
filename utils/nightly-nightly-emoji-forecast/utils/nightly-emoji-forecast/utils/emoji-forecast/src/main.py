import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict

# Mapping of weather condition keywords to emojis
WEATHER_EMOJI_MAP: Dict[str, str] = {
    "clear": "🌞",
    "sunny": "🌞",
    "partly cloudy": "⛅",
    "cloudy": "☁️",
    "overcast": "☁️",
    "rain": "☔️",
    "drizzle": "🌦️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
    "fog": "🌫️",
    "night": "🌙",
    "moon": "🌙",
    "storm": "⛈️",
}

# Mock weather data used when no external file is supplied
MOCK_WEATHER = {
    "forecast": [
        {"time": "morning", "condition": "clear"},
        {"time": "afternoon", "condition": "rain"},
        {"time": "evening", "condition": "clear"},
        {"time": "night", "condition": "clear"},
    ]
}


def load_weather_data(path: Path | None) -> Dict:
    """Load weather JSON from *path* or fall back to the built‑in mock.

    The function is deliberately simple – it expects a top‑level object with a
    ``forecast`` list where each entry contains a ``condition`` string.
    """
    if path is None:
        return MOCK_WEATHER
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        print(f"[emoji‑forecast] Failed to read {path}: {exc}", file=sys.stderr)
        sys.exit(1)


def condition_to_emoji(condition: str) -> str:
    """Return the emoji that best matches *condition*.

    Matching is case‑insensitive and looks for the first key that is a substring
    of the supplied condition.
    """
    lowered = condition.lower()
    for key, emoji in WEATHER_EMOJI_MAP.items():
        if key in lowered:
            return emoji
    # Default fallback
    return "❓"


def build_emoji_forecast(weather: Dict) -> List[str]:
    """Convert the ``forecast`` list into a sequence of emojis.

    Returns a list preserving the original order (e.g. ["🌞", "☔️", ...]).
    """
    emojis: List[str] = []
    for entry in weather.get("forecast", []):
        condition = entry.get("condition", "")
        emojis.append(condition_to_emoji(condition))
    return emojis


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert weather data to an emoji forecast.")
    parser.add_argument(
        "--data",
        type=Path,
        help="Path to a JSON file containing weather data. If omitted, a mock forecast is used.",
    )
    args = parser.parse_args(argv)

    weather = load_weather_data(args.data)
    emojis = build_emoji_forecast(weather)
    print(" ".join(emojis))
    return 0


if __name__ == "__main__":
    sys.exit(main())
