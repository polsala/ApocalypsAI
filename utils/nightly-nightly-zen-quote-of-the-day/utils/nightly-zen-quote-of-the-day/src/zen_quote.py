'''\
zen_quote.py – deterministic Zen quote selector.

Provides `get_quote(date: datetime.date | None = None) -> str`.
If `date` is None, uses today's date.
Selection is deterministic: same date always yields same quote.
'''\

from __future__ import annotations
import datetime
import hashlib
from typing import List

_QUOTES: List[str] = [
    "The obstacle is the path.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The journey of a thousand miles begins with one step.",
    "Let go or be dragged.",
    "In the middle of difficulty lies opportunity.",
    "The only constant is change.",
    "Be like water.",
    "All that you seek is already within you.",
    "Patience is the companion of wisdom."
]


def _pick_index(seed: str) -> int:
    """Hash the seed and map it into the quote list size."""
    h = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return int(h, 16) % len(_QUOTES)


def get_quote(date: datetime.date | None = None) -> str:
    """Return a deterministic Zen quote for the given date.

    If *date* is ``None`` the current local date is used.
    """
    if date is None:
        date = datetime.date.today()
    seed = date.isoformat()
    idx = _pick_index(seed)
    return _QUOTES[idx]


if __name__ == "__main__":
    print(get_quote())
