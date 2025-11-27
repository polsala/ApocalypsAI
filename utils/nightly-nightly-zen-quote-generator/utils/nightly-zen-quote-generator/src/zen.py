"""zen.py

Utility to provide a deterministic daily Zen quote.

Public API:
    get_zen_quote(date: Optional[datetime.date] = None) -> str
"""

from __future__ import annotations

import datetime
import random
from typing import List, Optional

# A modest collection of Zen‑style sayings.
_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the middle of difficulty lies opportunity.",
    "A single moment can change a lifetime.",
    "The moon does not fight the night; it simply shines.",
    "Patience is the companion of wisdom.",
    "When you realize nothing is lacking, the whole world belongs to you.",
    "The sound of one hand clapping is the echo of your own heart.",
    "Empty your cup so it may be filled anew.",
    "The river that forgets its source will dry up.",
    "A calm mind brings inner strength and self‑confidence.",
    "The softest thing in the universe overcomes the hardest thing in the universe.",
    "When you are content to be simply yourself, you are an original masterpiece.",
    "The present moment is the only time that truly exists.",
    "A wise man knows that he knows nothing.",
    "The wind does not know where it is going, yet it arrives.",
    "Simplicity is the ultimate sophistication."
]


def _seed_from_date(date: datetime.date) -> int:
    """Convert a date to an integer seed (YYYYMMDD)."""
    return int(date.strftime("%Y%m%d"))


def get_zen_quote(date: Optional[datetime.date] = None) -> str:
    """Return a deterministic Zen quote for *date*.

    If *date* is ``None`` the current local date is used.
    The same date always yields the same quote.
    """
    if date is None:
        date = datetime.date.today()
    seed = _seed_from_date(date)
    rng = random.Random(seed)
    # Mock rationale: deterministic selection via seeded RNG ensures reproducibility.
    return rng.choice(_QUOTES)


def _main() -> None:
    """CLI entry point – prints today's quote to stdout."""
    quote = get_zen_quote()
    print(quote)


if __name__ == "__main__":
    _main()
