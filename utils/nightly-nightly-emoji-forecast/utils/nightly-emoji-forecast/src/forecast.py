import sys
import datetime
import hashlib
from typing import List

EMOJI_WEATHER = [
    "☀️",  # sunny
    "🌤️",  # partly sunny
    "⛅",   # cloudy
    "🌥️",  # mostly cloudy
    "☁️",  # overcast
    "🌦️",  # rain showers
    "🌧️",  # rain
    "⛈️",  # thunderstorm
    "🌨️",  # snow
    "❄️",   # snowflake
    "🌪️",  # tornado (just for fun)
]

def _hash_date(date: datetime.date) -> int:
    """Return a stable integer hash for *date*.

    The hash is based on the ISO format of the date and the SHA‑256 algorithm,
    then reduced modulo the length of ``EMOJI_WEATHER``.
    """
    iso = date.isoformat().encode("utf-8")
    digest = hashlib.sha256(iso).hexdigest()
    # Convert a slice of the hex digest to int for reproducibility
    return int(digest[:8], 16)

def get_forecast(date: datetime.date) -> str:
    """Return a deterministic emoji forecast for *date*.

    The forecast consists of 1‑3 emojis selected based on the hashed date.
    """
    idx = _hash_date(date) % len(EMOJI_WEATHER)
    # Choose a length between 1 and 3 based on another slice of the hash
    length = (int(hashlib.sha256(date.isoformat().encode()).hexdigest()[8:10], 16) % 3) + 1
    forecast: List[str] = []
    for i in range(length):
        forecast.append(EMOJI_WEATHER[(idx + i) % len(EMOJI_WEATHER)])
    return " ".join(forecast)

def _parse_cli_args(args: List[str]) -> datetime.date:
    """Parse CLI arguments.

    * If a single argument is provided, treat it as an ISO date string.
    * Otherwise, use today's date.
    """
    if len(args) == 1:
        try:
            return datetime.date.fromisoformat(args[0])
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {args[0]}. Use YYYY-MM-DD") from exc
    elif len(args) == 0:
        return datetime.date.today()
    else:
        raise SystemExit("Usage: python -m src.forecast [YYYY-MM-DD]")

if __name__ == "__main__":
    try:
        target_date = _parse_cli_args(sys.argv[1:])
        print(get_forecast(target_date))
    except SystemExit as e:
        print(e, file=sys.stderr)
        sys.exit(1)
