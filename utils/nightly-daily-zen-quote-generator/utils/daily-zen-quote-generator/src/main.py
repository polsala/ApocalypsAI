"""daily_zen_quote_generator – deterministic Zen quotes per date.

The module provides a single public function ``get_zen_quote(date_str)`` which
accepts an ISO‑8601 date string (``YYYY-MM-DD``) and returns a quote selected
from a static list. The selection is deterministic: it hashes the date and
maps the result to an index in the quote list.

Running the module as a script prints the quote for the supplied date or for
today if no argument is given.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
from typing import List

# A modest collection of Zen‑style sayings.
_QUOTES: List[str] = [
    "The river flows, but the stones remain.",
    "When the wind stops, the leaves still whisper.",
    "Silence is the canvas of the mind.",
    "A single step is still a journey.",
    "The moon watches, even when hidden.",
    "Patience is the art of quiet strength.",
    "Even shadows need light to exist.",
    "The mountain does not rush, yet it stands forever.",
    "Listen to the rain; it tells stories of clouds.",
    "A calm mind sees the path clearly."
]

def _hash_date(date_str: str) -> int:
    """Return a stable integer hash for *date_str*.

    The hash is derived from SHA‑256 to guarantee consistency across Python
    versions and platforms.
    """
    digest = hashlib.sha256(date_str.encode("utf-8")).hexdigest()
    # Convert a slice of the hex digest to an int – enough entropy for our list.
    return int(digest[:8], 16)

def get_zen_quote(date_str: str | None = None) -> str:
    """Return a deterministic Zen quote for *date_str*.

    Parameters
    ----------
    date_str: str | None
        ISO‑8601 date (``YYYY-MM-DD``). If ``None`` the current local date is used.

    Returns
    -------
    str
        A quote selected from ``_QUOTES``.
    """
    if date_str is None:
        date_obj = datetime.date.today()
    else:
        try:
            date_obj = datetime.date.fromisoformat(date_str)
        except ValueError as exc:
            raise ValueError(
                f"Invalid date format '{date_str}'. Expected YYYY-MM-DD."
            ) from exc
    canonical = date_obj.isoformat()
    idx = _hash_date(canonical) % len(_QUOTES)
    return _QUOTES[idx]

def _cli() -> None:
    parser = argparse.ArgumentParser(
        prog="daily-zen-quote-generator",
        description="Print a deterministic Zen quote for a given date."
    )
    parser.add_argument(
        "date",
        nargs="?",
        help="Date in YYYY-MM-DD format (defaults to today)."
    )
    args = parser.parse_args()
    try:
        quote = get_zen_quote(args.date)
    except ValueError as e:
        parser.error(str(e))
    print(quote)

if __name__ == "__main__":
    _cli()
