"""Quote module for Daily Zen Quote utility."""

import random
from typing import List, Optional, Dict

# Static list of quotes with optional theme tags.
_QUOTES: List[Dict[str, str]] = [
    {"text": "The journey of a thousand miles begins with one step.", "theme": "mindfulness"},
    {"text": "When the wind blows, bend like a reed.", "theme": "nature"},
    {"text": "If you cannot find the answer, ask a duck.", "theme": "humor"},
    {"text": "Silence is a source of great strength.", "theme": "mindfulness"},
    {"text": "Even the tallest tree was once a seed.", "theme": "nature"},
    {"text": "A laugh is a short distance between two people.", "theme": "humor"},
]


def get_random_quote(theme: Optional[str] = None) -> str:
    """
    Return a random quote. If ``theme`` is provided, only quotes matching that theme are considered.
    Raises ``ValueError`` if no quotes match the given theme.
    """
    if theme:
        filtered = [q for q in _QUOTES if q["theme"] == theme]
        if not filtered:
            raise ValueError(f"No quotes found for theme '{theme}'.")
        choice_pool = filtered
    else:
        choice_pool = _QUOTES

    # Randomly select a quote dict and return its text.
    selected = random.choice(choice_pool)  # Mock rationale: deterministic in tests via patch.
    return selected["text"]
