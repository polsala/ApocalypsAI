"""
 daily_emoji.py

Deterministic daily emoji generator.
"""

import hashlib
from typing import List

_EMOJIS: List[str] = [
    "😀","😂","🥰","😎","🤓","🧐","🤖","👻","🎃","🤡",
    "🐶","🐱","🦊","🐼","🐨","🐸","🐵","🦁","🐔","🐧",
    "🌞","🌜","⭐","⚡","🔥","💧","🍀","🌈","☔","🌟"
]

def _hash_date(date_str: str) -> int:
    """Return an integer hash of the date string.
    
    Mock rationale: using SHA-256 ensures deterministic mapping.
    """
    digest = hashlib.sha256(date_str.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)  # use first 8 hex chars

def get_daily_emoji(date_str: str) -> str:
    """Return a deterministic emoji for the given ISO‑8601 date string.

    Parameters
    ----------
    date_str: str
        Date in ``YYYY-MM-DD`` format.

    Returns
    -------
    str
        An emoji from the curated list.
    """
    idx = _hash_date(date_str) % len(_EMOJIS)
    return _EMOJIS[idx]

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m daily_emoji <YYYY-MM-DD>")
        sys.exit(1)
    print(get_daily_emoji(sys.argv[1]))
