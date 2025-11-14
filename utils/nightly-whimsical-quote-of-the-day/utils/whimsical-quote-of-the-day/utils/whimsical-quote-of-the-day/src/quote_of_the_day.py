"""
whimsical_quote_of_the_day

Provides a deterministic "Quote of the Day" based on the current date.
"""

import datetime
from typing import List

_QUOTES: List[str] = [
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "I intend to live forever. So far, so good.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "If at first you don’t succeed, call it version 1.0.",
    "Life is short. Smile while you still have teeth.",
    "To err is human; to really mess things up you need a computer.",
    "I’m not lazy, I’m on energy‑saving mode.",
    "Debugging: Being the detective in a crime movie where you are also the murderer.",
]


def get_quote(date: datetime.date | None = None) -> str:
    """Return a quote deterministic for the given date.

    Args:
        date: The date to base the quote on. Defaults to today.

    Returns:
        A quote string.
    """
    if date is None:
        date = datetime.date.today()
    index = date.toordinal() % len(_QUOTES)  # deterministic selection
    return _QUOTES[index]


def main() -> None:
    """CLI entry point."""
    print(get_quote())


if __name__ == "__main__":
    main()
