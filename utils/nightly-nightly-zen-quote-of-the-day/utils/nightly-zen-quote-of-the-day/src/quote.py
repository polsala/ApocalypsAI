#!/usr/bin/env python3
"""Utility to print a random Zen quote.

The module provides three public helpers:
- ``load_quotes`` reads a JSON file containing a list of strings.
- ``get_random_quote`` returns a random element from that list.
- ``main`` ties everything together and prints the selected quote.
"""

import json
import random
import pathlib
import sys


def load_quotes(path: pathlib.Path) -> list[str]:
    """Load quotes from a JSON file.

    Args:
        path: Path to a JSON file that contains a list of strings.
    Returns:
        List of quote strings.
    """
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    # Ensure we always return a list of strings
    if not isinstance(data, list) or not all(isinstance(item, str) for item in data):
        raise ValueError("Invalid quotes format – expected a list of strings")
    return data


def get_random_quote(quotes: list[str]) -> str:
    """Return a random quote from *quotes*.

    Raises:
        ValueError: If *quotes* is empty.
    """
    if not quotes:
        raise ValueError("Quote list is empty")
    return random.choice(quotes)


def main() -> None:
    """Entry‑point for the CLI.

    It resolves the location of ``quotes.json`` relative to this file,
    loads the quotes, picks one at random, and prints it.  Errors are
    reported on ``stderr`` and cause a non‑zero exit status.
    """
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    quotes_path = base_dir / "data" / "quotes.json"
    try:
        quotes = load_quotes(quotes_path)
        quote = get_random_quote(quotes)
        print(quote)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
