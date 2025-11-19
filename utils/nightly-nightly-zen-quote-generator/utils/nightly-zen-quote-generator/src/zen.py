import sys
import hashlib
from datetime import datetime, date
from typing import List

# A curated list of whimsical Zen‑style quotes.
QUOTES: List[str] = [
    "Simplicity is the ultimate sophistication.",
    "When the code is clear, the bugs are shy.",
    "A function that does one thing does it well.",
    "Refactor early, refactor often, refactor wisely.",
    "Debugging is like being the detective in a crime movie where you are also the murderer.",
    "Write code as if the next developer is a violent psychopath who knows where you live.",
    "Premature optimization is the root of all evil.",
    "In the face of complexity, choose the simplest path.",
    "Tests are the safety net for your imagination.",
    "Version control is the diary of your project's soul."
]


def _date_to_key(d: date) -> str:
    """Convert a date to a deterministic string key used for hashing.

    Args:
        d: The date to convert.
    Returns:
        A string representation in ISO format (YYYY‑MM‑DD).
    """
    return d.isoformat()


def _select_quote(d: date) -> str:
    """Select a quote deterministically based on the given date.

    The selection uses SHA‑256 of the ISO date string, then maps the digest to an index.
    """
    key = _date_to_key(d)
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    # Convert a portion of the hex digest to an integer.
    idx = int(digest[:8], 16) % len(QUOTES)
    return QUOTES[idx]


def get_zen_quote(target_date: str | None = None) -> str:
    """Return today's (or a specified) Zen quote.

    Args:
        target_date: Optional ISO‑format date string (YYYY‑MM‑DD). If ``None`` the current
            system date is used.
    Returns:
        A quote string.
    """
    if target_date:
        try:
            d = datetime.strptime(target_date, "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValueError("target_date must be in YYYY-MM-DD format") from exc
    else:
        d = date.today()
    return _select_quote(d)


def _cli() -> None:
    """Simple command‑line interface.

    Usage:
        python -m src.zen            # prints today's quote
        python -m src.zen 2025-12-01 # prints quote for the given date
    """
    args = sys.argv[1:]
    if len(args) > 1:
        print("Usage: python -m src.zen [YYYY-MM-DD]", file=sys.stderr)
        sys.exit(1)
    target = args[0] if args else None
    try:
        quote = get_zen_quote(target)
        print(quote)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
