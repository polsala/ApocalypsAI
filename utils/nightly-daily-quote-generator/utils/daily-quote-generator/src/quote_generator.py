import argparse
import datetime
import random
import sys
from typing import List, Optional, Dict

# ---------------------------------------------------------------------------
# Quote data (static, offline)
# ---------------------------------------------------------------------------
_QUOTES: List[Dict[str, str]] = [
    {
        "text": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs",
        "category": "inspiration",
    },
    {
        "text": "I have not failed. I've just found 10,000 ways that won't work.",
        "author": "Thomas A. Edison",
        "category": "wisdom",
    },
    {
        "text": "I'm not arguing, I'm just explaining why I'm right.",
        "author": "Anonymous",
        "category": "humor",
    },
    {
        "text": "Life is what happens when you're busy making other plans.",
        "author": "John Lennon",
        "category": "inspiration",
    },
    {
        "text": "If you think you are too small to make a difference, try sleeping with a mosquito.",
        "author": "Dalai Lama",
        "category": "humor",
    },
]

# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def _filter_quotes(category: Optional[str] = None) -> List[Dict[str, str]]:
    """Return quotes matching *category* (if given)."""
    if category is None:
        return _QUOTES.copy()
    return [q for q in _QUOTES if q["category"].lower() == category.lower()]


def get_random_quote(seed: Optional[int] = None, category: Optional[str] = None) -> Dict[str, str]:
    """Return a random quote.

    *seed* makes the selection deterministic – useful for testing.
    *category* limits the pool to a specific theme.
    """
    if seed is not None:
        random.seed(seed)
    pool = _filter_quotes(category)
    if not pool:
        raise ValueError(f"No quotes found for category '{category}'.")
    return random.choice(pool)


def get_quote_of_the_day(date: Optional[datetime.date] = None) -> Dict[str, str]:
    """Return a reproducible "quote of the day".

    The quote is selected by hashing the ISO‑format date and using it as a seed.
    *date* can be injected for testing; defaults to ``datetime.date.today()``.
    """
    if date is None:
        date = datetime.date.today()
    # Deterministic seed based on the date string
    seed = int(date.strftime("%Y%m%d"))
    return get_random_quote(seed=seed)

# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _format_quote(q: Dict[str, str]) -> str:
    return f"\"{q['text']}\" — {q['author']}"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Daily Quote Generator")
    parser.add_argument("--seed", type=int, help="Seed for deterministic random quote")
    parser.add_argument(
        "--category",
        type=str,
        choices=["inspiration", "humor", "wisdom"],
        help="Filter quotes by category",
    )
    parser.add_argument(
        "--today",
        action="store_true",
        help="Show the quote of the day (ignores --seed and --category)",
    )
    args = parser.parse_args(argv)

    try:
        if args.today:
            quote = get_quote_of_the_day()
        else:
            quote = get_random_quote(seed=args.seed, category=args.category)
        print(_format_quote(quote))
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
