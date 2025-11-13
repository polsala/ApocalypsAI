#!/usr/bin/env python3
"""
Daily Quote Fetcher utility.

Provides `get_random_quote()` to retrieve a random quote from the bundled
`quotes.json` file. When executed as a script, prints the quote to stdout.
"""

import json
import random
import pathlib
from typing import Dict, List

# Path to the bundled quotes JSON file (relative to this file)
_QUOTES_PATH = pathlib.Path(__file__).with_name("quotes.json")


def _load_quotes() -> List[Dict[str, str]]:
    """Load quotes from the JSON file.

    Returns:
        List of quote dictionaries with keys 'text' and optional 'author'.
    """
    # Mock rationale: In tests we mock open/read to avoid file I/O.
    with _QUOTES_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def get_random_quote() -> Dict[str, str]:
    """Return a random quote from the bundled collection.

    Returns:
        A dict with at least a 'text' field and optionally 'author'.
    """
    quotes = _load_quotes()
    if not quotes:
        raise ValueError("No quotes available.")
    return random.choice(quotes)


def format_quote(quote: Dict[str, str]) -> str:
    """Format a quote dict into a printable string."""
    text = quote.get("text", "")
    author = quote.get("author")
    return f"\"{text}\"" + (f" — {author}" if author else "")


def main() -> None:
    """CLI entry point."""
    quote = get_random_quote()
    print(format_quote(quote))


if __name__ == "__main__":
    main()
