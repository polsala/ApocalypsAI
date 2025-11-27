import json
import sys
from pathlib import Path
from typing import Dict

# Mapping of weather conditions to emojis
_CONDITION_EMOJI = {
    "clear": "🌞",
    "partly_cloudy": "⛅",
    "cloudy": "☁️",
    "rain": "🌧️",
    "snow": "❄️",
    "thunderstorm": "⛈️",
    "fog": "🌫️",
}


def _select_emoji(condition: str) -> str:
    """Return an emoji for a given weather condition.

    If the condition is unknown, fall back to a generic weather emoji.
    """
    return _CONDITION_EMOJI.get(condition.lower(), "🌈")


def get_forecast(data: Dict) -> str:
    """Convert a weather dict into a human‑readable emoji forecast.

    Expected keys in *data*:
    - ``temperature_c`` (int or float)
    - ``condition`` (str) – e.g. ``"clear"``
    - ``precipitation_mm`` (int or float) – optional, used for extra context.
    """
    temp = data.get("temperature_c")
    condition = data.get("condition", "unknown")
    precip = data.get("precipitation_mm", 0)

    emoji = _select_emoji(condition)
    # Simple textual description based on condition
    description = condition.replace("_", " ").title()
    forecast = f"{emoji} {temp}°C – {description}"
    if precip:
        forecast += f" (Precip: {precip}mm)"
    return forecast


def _load_json_file(path: Path) -> Dict:
    """Load a JSON file from *path*.

    # Mock rationale: In production this would read a real API response.
    """
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main(argv=None) -> int:
    """CLI entry point.

    Usage: ``python -m emoji_forecast <path-to-json>``
    If no path is provided, reads from stdin.
    """
    argv = argv or sys.argv[1:]
    if not argv:
        # Read JSON from stdin
        data = json.load(sys.stdin)
    else:
        json_path = Path(argv[0])
        data = _load_json_file(json_path)
    print(get_forecast(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
