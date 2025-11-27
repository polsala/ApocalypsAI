import sys
import datetime
import hashlib
from typing import List

# A curated list of weather‑related emojis (sun, clouds, rain, etc.)
EMOJI_POOL: List[str] = [
    "☀️",  # sunny
    "🌤️",  # sun behind small cloud
    "⛅",   # sun behind cloud
    "🌥️",  # sun behind large cloud
    "☁️",  # cloud
    "🌦️",  # sun behind rain cloud
    "🌧️",  # cloud with rain
    "⛈️",  # cloud with lightning
    "🌩️",  # lightning
    "🌨️",  # cloud with snow
    "❄️",  # snowflake
    "🌈",  # rainbow
    "🌪️",  # tornado
    "🌫️",  # fog
    "💨",  # wind
]


def _seed_from_date(date: datetime.date) -> int:
    """Create a deterministic integer seed from a date.

    The function hashes the ISO‑format string of the date using SHA‑256 and
    converts the first 8 bytes of the digest into an integer.
    """
    iso = date.isoformat().encode("utf-8")
    digest = hashlib.sha256(iso).digest()
    # Use int.from_bytes to get a reproducible positive integer
    return int.from_bytes(digest[:8], "big")


def get_forecast(date: datetime.date | None = None) -> str:
    """Return a three‑emoji weather forecast for *date*.

    If *date* is ``None`` the current local date is used.
    The result is deterministic: the same date always yields the same forecast.
    """
    if date is None:
        date = datetime.date.today()
    seed = _seed_from_date(date)
    # Deterministically shuffle the emoji pool using the seed
    shuffled = EMOJI_POOL.copy()
    # Simple Fisher‑Yates shuffle with our own PRNG (linear congruential)
    # to avoid importing ``random`` which would otherwise use system entropy.
    a, c, m = 1664525, 1013904223, 2 ** 32
    state = seed
    for i in range(len(shuffled) - 1, 0, -1):
        state = (a * state + c) % m
        j = state % (i + 1)
        shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
    # Take the first three emojis as the forecast
    return " ".join(shuffled[:3])


def _parse_cli_arg(arg: str) -> datetime.date:
    """Parse a ``YYYY-MM-DD`` string into a ``datetime.date``.

    # Mock rationale: No external libraries are used; parsing is done manually.
    """
    try:
        year, month, day = map(int, arg.split("-"))
        return datetime.date(year, month, day)
    except Exception as exc:
        raise ValueError(f"Invalid date format '{arg}'. Expected YYYY-MM-DD.") from exc


def main() -> None:
    """CLI entry point.

    Usage:
        python -m nightly_emoji_forecast.src.forecast [YYYY-MM-DD]
    """
    if len(sys.argv) > 2:
        print("Usage: python -m nightly_emoji_forecast.src.forecast [YYYY-MM-DD]", file=sys.stderr)
        sys.exit(1)
    date = None
    if len(sys.argv) == 2:
        try:
            date = _parse_cli_arg(sys.argv[1])
        except ValueError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
    forecast = get_forecast(date)
    print(forecast)


if __name__ == "__main__":
    main()
