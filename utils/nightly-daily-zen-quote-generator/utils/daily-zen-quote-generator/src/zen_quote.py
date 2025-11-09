import argparse
import json
import random
import sys
from pathlib import Path
from typing import List, Dict

# Path to the bundled quotes JSON (relative to this file)
_QUOTES_PATH = Path(__file__).with_name("quotes.json")


def load_quotes() -> List[Dict[str, str]]:
    """Load the list of quotes from the bundled JSON file.

    Returns
    -------
    List[Dict[str, str]]
        Each dict has keys ``'text'`` and ``'author'``.
    """
    try:
        with _QUOTES_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        sys.stderr.write(f"Failed to load quotes: {exc}\n")
        sys.exit(1)


def pick_quote(quotes: List[Dict[str, str]], max_length: int | None = None) -> Dict[str, str]:
    """Select a random quote, optionally respecting a maximum length.

    Parameters
    ----------
    quotes: List[Dict[str, str]]
        The pool of available quotes.
    max_length: int | None
        If provided, filter out quotes whose ``text`` exceeds this length.

    Returns
    -------
    Dict[str, str]
        The chosen quote.
    """
    if max_length is not None:
        filtered = [q for q in quotes if len(q["text"]) <= max_length]
        if not filtered:
            sys.stderr.write("No quotes match the length constraint.\n")
            sys.exit(1)
        quotes = filtered
    # Random selection – deterministic in tests via mocking
    return random.choice(quotes)


def format_quote(quote: Dict[str, str]) -> str:
    """Return a pretty‑printed string for a quote.
    """
    return f"\"{quote['text']}\" — {quote['author']}"


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument(
        "--max-length",
        type=int,
        help="Maximum number of characters for the quote text.",
    )
    args = parser.parse_args(argv)

    quotes = load_quotes()
    chosen = pick_quote(quotes, max_length=args.max_length)
    print(format_quote(chosen))


if __name__ == "__main__":
    main()
