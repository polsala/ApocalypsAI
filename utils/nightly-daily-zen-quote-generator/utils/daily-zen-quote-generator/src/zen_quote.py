import json
import random
import pathlib
import argparse
from typing import List

_QUOTE_FILE = pathlib.Path(__file__).with_name("quotes.json")


def _load_quotes() -> List[str]:
    """Load the bundled quotes from ``quotes.json``.

    Returns
    -------
    List[str]
        A list of quote strings.
    """
    with _QUOTE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


_QUOTES = _load_quotes()


def get_random_quote(seed: int | None = None) -> str:
    """Return a quote.

    Parameters
    ----------
    seed: int | None, optional
        If provided, the quote is selected deterministically using ``seed % len(quotes)``.
        If ``None`` a true random choice is made.

    Returns
    -------
    str
        The selected quote.
    """
    if seed is not None:
        index = seed % len(_QUOTES)
        return _QUOTES[index]
    return random.choice(_QUOTES)


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument("--seed", type=int, help="Optional integer seed for deterministic output")
    args = parser.parse_args()
    quote = get_random_quote(seed=args.seed)
    print(quote)


if __name__ == "__main__":
    _cli()
