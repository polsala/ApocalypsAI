"""
Quote of the Day utility.

Provides a deterministic quote based on the current date.
"""

import datetime
import hashlib
from typing import List

# Built‑in list of zen quotes.
QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "What you think, you become.",
    "The only constant is change.",
    "Be yourself; everyone else is already taken.",
    "In the middle of difficulty lies opportunity.",
    "Knowledge speaks, but wisdom listens.",
    "The quieter you become, the more you can hear.",
    "Do not seek to follow in the footsteps of the wise; seek what they sought.",
    "When the mind is still, the universe surrenders."
]

def _date_string(date: datetime.date) -> str:
    """Return ISO format string for the given date."""
    return date.isoformat()

def _select_index(date_str: str) -> int:
    """Deterministically select an index based on a hash of the date string."""
    # Use SHA256 for stable hashing across Python versions.
    digest = hashlib.sha256(date_str.encode('utf-8')).hexdigest()
    # Convert a portion of the hex digest to int.
    num = int(digest[:8], 16)
    return num % len(QUOTES)

def get_quote(date: datetime.date | None = None) -> str:
    """
    Return the quote for the given date (or today if None).

    Args:
        date: Optional date object. If omitted, uses today's date.

    Returns:
        A quote string.
    """
    if date is None:
        date = datetime.date.today()
    date_str = _date_string(date)
    idx = _select_index(date_str)
    return QUOTES[idx]
