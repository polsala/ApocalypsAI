"""
Daily Zen Quote Generator

Provides a deterministic Zen quote for a given date.
"""

import hashlib
from datetime import date, datetime
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "Silence is a source of great strength.",
    "The only constant is change.",
    "Know the rules so you can break them.",
    "A smooth sea never made a skilled sailor.",
    "Be present, not perfect.",
    "The quieter you become, the more you can hear.",
    "All that you seek is already within you.",
    "Patience is bitter, but its fruit is sweet.",
    "The mind is everything. What you think, you become.",
    "Do not seek to follow in the footsteps of the wise. Seek what they sought.",
    "When you realize nothing is lacking, the whole world belongs to you.",
    "The greatest wealth is to live content with little.",
    "In the middle of difficulty lies opportunity.",
    "Your work is your love made visible.",
    "The only way to do great work is to love what you do."
]


def _hash_date(d: date) -> int:
    """Return an integer hash for the given date."""
    iso = d.isoformat()
    h = hashlib.sha256(iso.encode("utf-8")).hexdigest()
    return int(h, 16)


def get_quote_of_day(d: date) -> str:
    """Return a deterministic quote for the given date."""
    idx = _hash_date(d) % len(_QUOTES)
    return _QUOTES[idx]


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Print a Zen quote for a given date.")
    parser.add_argument(
        "date",
        nargs="?",
        default=datetime.utcnow().date().isoformat(),
        help="Date in YYYY-MM-DD format (default: today UTC)",
    )
    args = parser.parse_args()
    try:
        d = datetime.strptime(args.date, "%Y-%m-%d").date()
    except ValueError as e:
        raise SystemExit(f"Invalid date format: {e}")
    print(get_quote_of_day(d))


if __name__ == "__main__":
    main()
