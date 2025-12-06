import json
import random
import argparse
from pathlib import Path
from typing import List, Dict

# Path to the bundled quotes JSON (located in the same package directory)
_QUOTE_FILE = Path(__file__).with_name("quotes.json")


def load_quotes() -> List[Dict[str, str]]:
    """Load the list of quotes from the bundled JSON file.

    Returns
    -------
    List[Dict[str, str]]
        Each dict contains ``"text"`` and optional ``"author"`` fields.
    """
    with _QUOTE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def pick_quote(quotes: List[Dict[str, str]], seed: int | None = None) -> Dict[str, str]:
    """Select a quote, optionally using a deterministic seed.

    Parameters
    ----------
    quotes: List[Dict[str, str]]
        The list of available quotes.
    seed: int | None
        If provided, ``random`` is seeded before selection to make the output repeatable.

    Returns
    -------
    Dict[str, str]
        The chosen quote dictionary.
    """
    rng = random.Random(seed)
    return rng.choice(quotes)


def format_quote(quote: Dict[str, str]) -> str:
    """Return a pretty‑printed string for a quote.
    """
    text = quote.get("text", "")
    author = quote.get("author")
    if author:
        return f"\"{text}\" — {author}"
    return f"\"{text}\""


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional integer seed for deterministic output.",
    )
    args = parser.parse_args()

    quotes = load_quotes()
    quote = pick_quote(quotes, seed=args.seed)
    print(format_quote(quote))


if __name__ == "__main__":
    main()
