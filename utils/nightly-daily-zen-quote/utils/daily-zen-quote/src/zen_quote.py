"""daily_zen_quote – deterministic daily Zen quote generator.

Provides:
- `get_today_quote()` – returns the quote for the current local date.
- CLI entry point when executed as a module.
"""

from __future__ import annotations

import datetime
from typing import List

# A modest collection of Zen‑style sayings.
QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "Silence is a source of great strength.",
    "In the middle of difficulty lies opportunity.",
    "Know the rules well, so you can break them wisely.",
    "A single spark can start a great fire.",
    "Patience is the companion of wisdom.",
]


def _quote_index_for_date(date: datetime.date) -> int:
    """Return a deterministic index into ``QUOTES`` for *date*.

    The algorithm is deliberately simple and deterministic:
    ``index = (date.toordinal() % len(QUOTES))``.
    """
    return date.toordinal() % len(QUOTES)


def get_today_quote(today: datetime.date | None = None) -> str:
    """Return the Zen quote for *today*.

    Parameters
    ----------
    today:
        Optional override for the current date (useful for testing).
        If ``None`` the system's local date is used.
    """
    if today is None:
        today = datetime.date.today()
    idx = _quote_index_for_date(today)
    return QUOTES[idx]


def _main() -> None:
    """CLI entry point – prints the quote for the current day."""
    print(get_today_quote())


if __name__ == "__main__":
    _main()
