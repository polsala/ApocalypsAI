import argparse
import random
import sys
from typing import List, Tuple

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

_QUOTE_BANK: List[Tuple[str, str]] = [
    ("The early bird gets the worm, but the second mouse gets the cheese.", "humor"),
    ("When life gives you lemons, make lemonade. Then find someone whose life gave them vodka, and have a party.", "humor"),
    ("Dreams are the seedlings of reality.", "inspiration"),
    ("The only limit to our realization of tomorrow is our doubts of today.", "inspiration"),
    ("Know thyself, or at least know where you left your keys.", "philosophy"),
    ("The unexamined life is like a software without tests – it may work, but you’ll never know why.", "philosophy"),
]

# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def _filter_quotes(category: str | None) -> List[str]:
    """Return a list of quote strings matching *category*.

    If *category* is ``None`` all quotes are returned.
    """
    if category is None:
        return [q for q, _ in _QUOTE_BANK]
    return [q for q, cat in _QUOTE_BANK if cat.lower() == category.lower()]


def get_random_quote(category: str | None = None, seed: int | None = None) -> str:
    """Return a deterministic random quote.

    * ``category`` – optional filter (e.g., ``"humor"``).
    * ``seed`` – optional integer seed for reproducibility (used by tests).
    """
    if seed is not None:
        random.seed(seed)
    candidates = _filter_quotes(category)
    if not candidates:
        raise ValueError(f"No quotes found for category '{category}'.")
    return random.choice(candidates)

# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random whimsical quote.")
    parser.add_argument(
        "--category",
        type=str,
        help="Filter quotes by category (e.g., inspiration, humor, philosophy).",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = _parse_args()
    try:
        quote = get_random_quote(category=args.category)
        print(quote)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
