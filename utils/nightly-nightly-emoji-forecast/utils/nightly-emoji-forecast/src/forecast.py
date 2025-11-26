"""
emoji forecast utility
"""

import sys
import datetime
from typing import List

EMOJIS: List[str] = [
    "☀️", "🌤️", "⛅", "🌥️", "☁️", "🌦️",
    "🌧️", "⛈️", "🌩️", "❄️", "🌪️", "🌈"
]

def get_forecast(target_date: datetime.date) -> str:
    """
    Return an emoji representing the forecast for the given date.
    Deterministic based on the date's ordinal.
    """
    index = target_date.toordinal() % len(EMOJIS)
    return EMOJIS[index]

def _parse_date(arg: str) -> datetime.date:
    try:
        return datetime.datetime.strptime(arg, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"Invalid date format '{arg}'. Expected YYYY-MM-DD.") from exc

def main() -> None:
    if len(sys.argv) > 1:
        date = _parse_date(sys.argv[1])
    else:
        date = datetime.date.today()
    forecast = get_forecast(date)
    print(forecast)

if __name__ == "__main__":
    main()
