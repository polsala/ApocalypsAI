import sys
import datetime
import hashlib
from typing import List

# A curated list of weather‑related emojis ordered by “intensity”.
EMOJI_POOL: List[str] = [
    "☀️",   # sunny
    "🌤️",   # partly sunny
    "⛅",    # partly cloudy
    "🌥️",   # mostly cloudy
    "☁️",   # cloudy
    "🌦️",   # rain sun
    "🌧️",   # rain
    "⛈️",   # thunderstorm
    "🌨️",   # snow
    "❄️",   # snowflake
    "🌈",   # rainbow (good vibes)
    "🌪️",   # tornado (just for fun)
]

def _seed_from_date(date: datetime.date) -> int:
    """Create a reproducible integer seed from a date.

    The seed is derived from an SHA‑256 hash of the ISO‑format date string.
    """
    iso = date.isoformat().encode("utf-8")
    digest = hashlib.sha256(iso).hexdigest()
    # Use the first 8 hex chars → 32‑bit integer
    return int(digest[:8], 16)

def _select_emojis(seed: int, count: int = 3) -> List[str]:
    """Deterministically pick *count* emojis from EMOJI_POOL using *seed*.

    The selection is order‑preserving based on the shuffled pool.
    """
    # Simple deterministic shuffle using Fisher‑Yates with the seed
    pool = EMOJI_POOL.copy()
    rng = seed
    for i in range(len(pool) - 1, 0, -1):
        # Derive a pseudo‑random index from the rng
        rng = (rng * 1664525 + 1013904223) & 0xFFFFFFFF  # LCG step
        j = rng % (i + 1)
        pool[i], pool[j] = pool[j], pool[i]
    return pool[:count]

def get_forecast(date: datetime.date | None = None) -> str:
    """Return a space‑separated string of emojis representing the forecast.

    If *date* is ``None`` the current local date is used.
    """
    if date is None:
        date = datetime.date.today()
    seed = _seed_from_date(date)
    emojis = _select_emojis(seed)
    return " ".join(emojis)

def _cli() -> None:
    """Command‑line entry point.

    Optional argument: a date in ``YYYY-MM-DD`` format.
    """
    if len(sys.argv) > 2:
        print("Usage: python -m src.forecast [YYYY-MM-DD]", file=sys.stderr)
        sys.exit(1)
    if len(sys.argv) == 2:
        try:
            date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
    else:
        date = None
    print(get_forecast(date))

if __name__ == "__main__":
    _cli()
