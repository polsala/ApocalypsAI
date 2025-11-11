"""
Daily Zen Quote Generator
"""

import datetime
from typing import List

_QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "What you think, you become.",
    "The only constant is change.",
    "Be yourself; everyone else is already taken."
]


def get_quote_of_the_day(target_date: datetime.date | None = None) -> str:
    """Return a quote deterministically based on the given date.

    If *target_date* is ``None`` the function uses ``datetime.date.today()``.
    The selection uses the number of days since the Unix epoch, ensuring the
    same date always yields the same quote across Python versions.
    """
    if target_date is None:
        target_date = datetime.date.today()
    # Days since 1970‑01‑01 provides a stable integer across environments
    days_since_epoch = (target_date - datetime.date(1970, 1, 1)).days
    index = days_since_epoch % len(_QUOTES)
    return _QUOTES[index]


def main() -> None:
    """CLI entry point – prints the quote for today."""
    print(get_quote_of_the_day())


if __name__ == "__main__":
    main()
