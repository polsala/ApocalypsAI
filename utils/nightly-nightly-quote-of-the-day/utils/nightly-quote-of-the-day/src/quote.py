"""quote.py – deterministic quote‑of‑the‑day utility.

Provides:
- ``get_quote(date: Optional[datetime.date] = None) -> str`` – returns a quote.
- ``main()`` – CLI entry point.
"""

import argparse
import datetime
import hashlib
from typing import List, Optional

# A modest collection of motivational quotes.
_QUOTES: List[str] = [
    "The only way to do great work is to love what you do. – Steve Jobs",
    "Life is what happens when you're busy making other plans. – John Lennon",
    "The purpose of our lives is to be happy. – Dalai Lama",
    "Get busy living or get busy dying. – Stephen King",
    "You have within you right now, everything you need to deal with whatever the world can throw at you. – Brian Tracy",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt",
    "Do not wait to strike till the iron is hot; but make it hot by striking. – William Butler Yeats",
    "What we think, we become. – Buddha",
    "The best revenge is massive success. – Frank Sinatra",
]


def _seed_from_date(date: datetime.date) -> int:
    """Create an integer seed from a date using SHA‑256.

    The function is deterministic and platform‑independent.
    """
    iso = date.isoformat().encode("utf-8")
    digest = hashlib.sha256(iso).hexdigest()
    # Use the first 8 hex digits to form a 32‑bit integer.
    return int(digest[:8], 16)


def get_quote(date: Optional[datetime.date] = None) -> str:
    """Return a quote for *date*.

    If *date* is ``None`` the current local date is used.
    The selection is deterministic: the same date always yields the same quote.
    """
    if date is None:
        date = datetime.date.today()
    seed = _seed_from_date(date)
    index = seed % len(_QUOTES)
    return _QUOTES[index]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a deterministic quote of the day.")
    parser.add_argument(
        "--date",
        type=str,
        help="ISO‑format date (YYYY‑MM‑DD). If omitted, uses today.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError as exc:
            raise SystemExit(f"Invalid date format: {args.date}. Expected YYYY‑MM‑DD") from exc
    else:
        target_date = None
    quote = get_quote(target_date)
    print(quote)


if __name__ == "__main__":
    main()
