"""emoji_forecast – map simple weather conditions to emojis.

The module provides a single public function :func:`get_emoji_forecast` and a small
CLI for convenience.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Mapping

# Mapping from weather condition to emoji string
_CONDITION_EMOJI_MAP: Mapping[str, str] = {
    "clear": "☀️",
    "cloudy": "☁️",
    "rain": "🌧️",
    "snow": "❄️",
    "storm": "⛈️",
    "fog": "🌫️",
}


def get_emoji_forecast(weather_data: Mapping[str, str]) -> str:
    """Return an emoji forecast based on *weather_data*.

    Parameters
    ----------
    weather_data:
        Mapping containing at least the key ``"condition"`` whose value is one of the
        supported weather strings.

    Returns
    -------
    str
        Emoji representing the condition. If the condition is unknown, returns a
        generic "❓" emoji.
    """
    condition = str(weather_data.get("condition", "")).lower()
    return _CONDITION_EMOJI_MAP.get(condition, "❓")


def _load_json(path: Path) -> Mapping[str, str]:
    """Load a tiny JSON file containing weather data.

    The function is deliberately simple – it raises ``FileNotFoundError`` or ``json.JSONDecodeError``
    which the CLI propagates as a user‑friendly message.
    """
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _default_mock_path() -> Path:
    """Return a Path to an embedded mock JSON file.

    The file lives next to this module and contains a deterministic example used by the
    CLI when no argument is supplied.
    """
    return Path(__file__).with_name("mock_weather.json")


def _write_default_mock():
    """Create the bundled mock JSON file if it does not exist.

    This helper is executed on import so that the CLI can always fall back to a known
    dataset without requiring the repository to ship an extra file manually.
    """
    mock_path = _default_mock_path()
    if not mock_path.exists():
        mock_path.write_text(json.dumps({"condition": "clear"}), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """Entry‑point for ``python -m emoji_forecast``.

    Returns an exit code suitable for ``sys.exit``.
    """
    argv = argv if argv is not None else sys.argv[1:]
    try:
        if argv:
            data_path = Path(argv[0])
        else:
            # Ensure the bundled mock exists and use it
            _write_default_mock()
            data_path = _default_mock_path()
        weather = _load_json(data_path)
        forecast = get_emoji_forecast(weather)
        print(forecast)
        return 0
    except FileNotFoundError:
        print("Error: JSON file not found.", file=sys.stderr)
        return 1
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.", file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover – unexpected safety net
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
