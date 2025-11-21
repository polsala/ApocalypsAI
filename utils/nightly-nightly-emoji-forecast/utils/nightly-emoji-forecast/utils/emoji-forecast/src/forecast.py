import datetime
import hashlib
from typing import List

EMOJIS = [
    "☀️",
    "🌤️",
    "⛅",
    "🌥️",
    "☁️",
    "🌧️",
    "⛈️",
    "🌩️",
    "🌨️",
    "❄️",
    "🌈",
    "🌪️",
    "🌫️",
]


def _hash_date(date: datetime.date) -> int:
    """Create a deterministic integer hash from a date.

    The SHA‑256 digest of the ISO‑format string is interpreted as a hex integer.
    """
    h = hashlib.sha256(date.isoformat().encode()).hexdigest()
    return int(h, 16)


def get_forecast(date: datetime.date | None = None, count: int = 3) -> List[str]:
    """Return a list of `count` emoji forecasts for the given date.

    If `date` is ``None`` the function uses ``datetime.date.today()``.
    The selection is deterministic: the same date always yields the same list.
    """
    if date is None:
        date = datetime.date.today()
    seed = _hash_date(date)
    # Simple deterministic selection based on the seed
    return [EMOJIS[(seed + i) % len(EMOJIS)] for i in range(count)]


def main() -> None:
    forecast = get_forecast()
    print(" ".join(forecast))


if __name__ == "__main__":
    main()
