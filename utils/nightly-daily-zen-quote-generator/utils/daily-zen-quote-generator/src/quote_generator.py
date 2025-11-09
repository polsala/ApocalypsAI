import json
import random
import argparse
from pathlib import Path
from typing import List, Dict

# Path to the bundled quotes JSON (relative to this file)
_QUOTES_PATH = Path(__file__).with_name("quotes.json")


def load_quotes() -> List[Dict[str, str]]:
    """Load the list of quotes from the bundled JSON file.

    Returns
    -------
    List[Dict[str, str]]
        Each dict contains ``"quote"`` and ``"author"`` keys.
    """
    with _QUOTES_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_random_quote(quotes: List[Dict[str, str]]) -> Dict[str, str]:
    """Select a random quote from *quotes*.

    Parameters
    ----------
    quotes : List[Dict[str, str]]
        The list returned by :func:`load_quotes`.

    Returns
    -------
    Dict[str, str]
        A single quote dict.
    """
    return random.choice(quotes)


def format_quote(quote: Dict[str, str]) -> str:
    """Return a nicely formatted string for a quote dict."""
    return f"\"{quote['quote']}\" – {quote['author']}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print a random Zen‑style quote from the bundled collection."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional integer seed for reproducible output (useful for demos).",
    )
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    quotes = load_quotes()
    quote = get_random_quote(quotes)
    print(format_quote(quote))


if __name__ == "__main__":
    main()
