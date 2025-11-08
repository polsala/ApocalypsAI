import sys
import datetime
import hashlib
from typing import List

# A curated list of short Zen‑style quotes.
_QUOTES: List[str] = [
    "The river never forgets its source.",
    "When the wind blows, the bamboo bends.",
    "A single candle can illuminate a dark room.",
    "Silence is the language of the wise.",
    "The mountain does not rush, yet it stands forever.",
    "A seed knows the tree it will become.",
    "Even the longest journey begins with a single step.",
    "The moon reflects the sun’s light without claiming it.",
    "Patience is the companion of wisdom.",
    "A still lake mirrors the sky perfectly."
]


def _date_to_index(date: datetime.date) -> int:
    """Deterministically map a date to an index in the _QUOTES list.

    The algorithm:
    1. Convert the date to its ISO string (YYYY‑MM‑DD).
    2. Compute an SHA‑256 hash of that string.
    3. Interpret the first 8 hex digits as an integer.
    4. Modulo the length of the quote list.
    """
    iso = date.isoformat()
    digest = hashlib.sha256(iso.encode("utf-8")).hexdigest()
    # Use first 8 characters for a 32‑bit integer – more than enough for our list size.
    num = int(digest[:8], 16)
    return num % len(_QUOTES)


def get_zen_quote(date: datetime.date) -> str:
    """Return the Zen quote associated with *date*.

    Parameters
    ----------
    date: datetime.date
        The date for which to retrieve a quote.

    Returns
    -------
    str
        A deterministic Zen quote.
    """
    idx = _date_to_index(date)
    return _QUOTES[idx]


def _parse_cli_arg(arg: str) -> datetime.date:
    """Parse a CLI argument into a ``datetime.date``.

    Accepts ISO‑format dates (YYYY‑MM‑DD). Raises ``ValueError`` on failure.
    """
    return datetime.date.fromisoformat(arg)


def main(argv: List[str] | None = None) -> int:
    """Entry point for the ``python -m`` CLI.

    Returns an exit code (0 on success, 1 on error).
    """
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m daily_zen_quote_generator <YYYY-MM-DD>")
        return 1
    try:
        target_date = _parse_cli_arg(argv[0])
    except Exception as e:
        print(f"Error parsing date: {e}")
        return 1
    quote = get_zen_quote(target_date)
    print(quote)
    return 0


if __name__ == "__main__":
    sys.exit(main())
