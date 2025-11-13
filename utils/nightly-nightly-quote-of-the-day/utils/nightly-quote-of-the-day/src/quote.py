import argparse
import random
from typing import List, Tuple, Optional

# ---------------------------------------------------------------------------
# Quote data (embedded, no network required)
# ---------------------------------------------------------------------------

_QUOTE_DB: List[Tuple[str, str, str]] = [
    ("The only limit to our realization of tomorrow is our doubts of today.", "Franklin D. Roosevelt", "motivation"),
    ("Life is what happens when you're busy making other plans.", "John Lennon", "humor"),
    ("In the middle of difficulty lies opportunity.", "Albert Einstein", "motivation"),
    ("I am so clever that sometimes I don't understand a single word of what I am saying.", "Oscar Wilde", "humor"),
    ("The purpose of our lives is to be happy.", "Dalai Lama", "philosophy"),
]


def _filter_by_category(category: Optional[str]) -> List[Tuple[str, str, str]]:
    """Return a list of quotes matching *category* (case‑insensitive).

    If *category* is ``None`` or empty, the full database is returned.
    """
    if not category:
        return _QUOTE_DB
    lowered = category.lower()
    return [q for q in _QUOTE_DB if q[2].lower() == lowered]


def get_random_quote(category: Optional[str] = None) -> Tuple[str, str]:
    """Select a random quote (and its author) optionally filtered by *category*.

    Returns:
        (quote, author)
    """
    candidates = _filter_by_category(category)
    if not candidates:
        raise ValueError(f"No quotes found for category '{category}'.")
    quote, author, _ = random.choice(candidates)
    return quote, author


def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print a random inspirational quote.")
    parser.add_argument(
        "--category",
        type=str,
        help="Optional category to filter quotes (e.g., motivation, humor, philosophy).",
    )
    return parser


def main() -> None:
    parser = _build_cli()
    args = parser.parse_args()
    try:
        quote, author = get_random_quote(args.category)
        print(f"\"{quote}\" — {author}")
    except ValueError as exc:
        print(exc)


if __name__ == "__main__":
    main()
