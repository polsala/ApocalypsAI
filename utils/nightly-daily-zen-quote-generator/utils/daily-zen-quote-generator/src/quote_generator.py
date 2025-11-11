import hashlib
import datetime
import sys
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "Silence is a source of great strength.",
    "The only constant is change.",
    "Know yourself, know the world.",
    "Patience is the companion of wisdom.",
    "In the middle of difficulty lies opportunity."
]


def _date_string(date: datetime.date) -> str:
    """Return ISO date string for hashing."""
    return date.isoformat()


def _select_quote(date: datetime.date) -> str:
    """Deterministically select a quote based on the given date."""
    date_str = _date_string(date)
    digest = hashlib.sha256(date_str.encode()).hexdigest()
    index = int(digest, 16) % len(_QUOTES)
    return _QUOTES[index]


def main() -> None:
    today = datetime.date.today()
    quote = _select_quote(today)
    print(quote)


if __name__ == "__main__":
    main()
