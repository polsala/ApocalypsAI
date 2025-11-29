'''Emoji weather forecast utility.

Provides a deterministic, whimsical "weather" forecast represented by emojis.
'''

import sys
from datetime import datetime, date
from typing import List

# List of possible emoji forecasts
FORECASTS: List[str] = ["☀️", "☁️", "🌧️", "❄️", "⛈️", "🌈"]


def get_forecast(target_date: date) -> str:
    """Return an emoji forecast for the given date.

    The forecast is deterministic: it uses the day of year modulo the number
    of available emojis.
    """
    index = target_date.timetuple().tm_yday % len(FORECASTS)
    return FORECASTS[index]


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Args:
        argv: Optional list of arguments (excluding the program name). If None,
              sys.argv[1:] is used.

    Returns:
        Exit code (0 on success, 1 on error).
    """
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) == 0:
        target = date.today()
    else:
        try:
            target = datetime.strptime(argv[0], "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            return 1

    print(get_forecast(target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
