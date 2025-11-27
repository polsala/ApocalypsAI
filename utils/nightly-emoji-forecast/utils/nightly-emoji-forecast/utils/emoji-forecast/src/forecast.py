import argparse
import datetime
import hashlib
from typing import Optional

EMOJIS = [
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
    "🌪️",  # tornado
]


def _seed_for_date(date: datetime.date) -> int:
    """Create a deterministic integer seed from a date.

    The seed is derived from the SHA‑256 hash of the ISO‑formatted date string.
    """
    hash_bytes = hashlib.sha256(date.isoformat().encode()).digest()
    return int.from_bytes(hash_bytes, "big")


def get_forecast(date: Optional[datetime.date] = None) -> str:
    """Return a two‑emoji weather forecast for *date*.

    If *date* is ``None`` the current local date is used.
    The result is deterministic: the same date always yields the same emojis.
    """
    if date is None:
        date = datetime.date.today()
    seed = _seed_for_date(date)
    first = EMOJIS[seed % len(EMOJIS)]
    second = EMOJIS[(seed // len(EMOJIS)) % len(EMOJIS)]
    return f"{first}{second}"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deterministic emoji weather forecast")
    parser.add_argument(
        "-d",
        "--date",
        help="Date in YYYY-MM-DD format (defaults to today)",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {exc}")
    else:
        target_date = None
    print(get_forecast(target_date))


if __name__ == "__main__":
    main()
