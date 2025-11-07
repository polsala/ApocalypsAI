"""Quote generator utility.

Provides a single public function :func:`get_random_quote` that returns a
random Zen‑inspired quote, optionally limited to a specific theme.
"""

import random
from typing import List, Optional

# Internal quote database – feel free to extend.
_QUOTES = {
    "mindfulness": [
        "The mind is everything. What you think you become. – Buddha",
        "Be present in all things and thankful for all things. – Maya Angelou",
    ],
    "impermanence": [
        "The only constant is change. – Heraclitus",
        "All that we are is the result of what we have thought. – Buddha",
    ],
    "simplicity": [
        "Simplicity is the ultimate sophistication. – Leonardo da Vinci",
        "Nature does not hurry, yet everything is accomplished. – Lao Tzu",
    ],
}


def _flatten(quotes_dict: dict) -> List[str]:
    """Flatten all quotes into a single list.

    Args:
        quotes_dict: Mapping of theme → list of quotes.
    Returns:
        A flat list containing every quote.
    """
    return [quote for quotes in quotes_dict.values() for quote in quotes]


def get_random_quote(theme: Optional[str] = None) -> str:
    """Return a random quote.

    Args:
        theme: Optional theme to filter quotes. Must match one of the keys in
               the internal quote dictionary. If ``None`` or an unknown theme
               is supplied, quotes from *all* themes are considered.

    Returns:
        A randomly selected quote string.
    """
    if theme and theme in _QUOTES:
        pool = _QUOTES[theme]
    else:
        pool = _flatten(_QUOTES)
    return random.choice(pool)
