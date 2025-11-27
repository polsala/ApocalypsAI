#!/usr/bin/env python3
"""
Nightly Quirky Quote Generator

Selects a random quote from a built‑in list and prints it with the current date.
"""

import random
import datetime
import sys
from typing import List

_QUOTES: List[str] = [
    "The early bird gets the worm, but the second mouse gets the cheese.",
    "I’m not lazy, I’m on energy‑saving mode.",
    "If at first you don’t succeed, skydiving is not for you.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Life is short – smile while you still have teeth."
]

def get_random_quote() -> str:
    """Return a random quote from the internal list."""
    return random.choice(_QUOTES)

def format_quote(quote: str) -> str:
    """Return the quote prefixed with ISO‑8601 date."""
    today = datetime.date.today().isoformat()
    return f"{today}: {quote}"

def main() -> None:
    """CLI entry point."""
    quote = get_random_quote()
    print(format_quote(quote))

if __name__ == "__main__":
    # Allow deterministic output when a seed is provided via env var (useful for tests)
    seed = sys.argv[1] if len(sys.argv) > 1 else None
    if seed is not None:
        random.seed(seed)
    main()
