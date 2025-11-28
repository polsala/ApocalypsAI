import json
import sys
from pathlib import Path

EMOJI_MAP = {
    "sunny": "🌞",
    "clear": "🌞",
    "rainy": "🌧️",
    "cloudy": "☁️",
    "snow": "❄️",
    "storm": "⛈️",
    "windy": "🌬️",
}

def load_weather(file_path: str) -> dict:
    """Load weather JSON from file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def emoji_for(condition: str) -> str:
    """Return an emoji for a given weather condition."""
    return EMOJI_MAP.get(condition.lower(), "❓")

def format_forecast(weather: dict) -> str:
    """Create a human‑readable forecast string."""
    temp = weather.get("temperature")
    cond = weather.get("condition", "unknown")
    emoji = emoji_for(cond)
    return f"{emoji} {temp}°C – {cond.capitalize()}"

def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: python -m emoji_forecast <weather.json>", file=sys.stderr)
        sys.exit(1)
    path = argv[0]
    weather = load_weather(path)
    print(format_forecast(weather))

if __name__ == "__main__":
    main()
