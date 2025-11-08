import argparse
import random
from typing import List, Optional

# ---------------------------------------------------------------------------
# Quote data – a small curated collection. In a real project this could be a
# separate JSON/YAML file, but keeping it inline makes the utility fully
# self‑contained.
# ---------------------------------------------------------------------------

_QUOTE_DB = {
    "mindfulness": [
        "The mind is everything. What you think you become.",
        "Feel the breath, feel the present.",
        "When you realize nothing is lacking, the whole world belongs to you."
    ],
    "humor": [
        "If you think you are too small to make a difference, try sleeping with a mosquito.",
        "The journey of a thousand miles begins with a single step… onto the couch.",
        "When the going gets tough, the tough get a coffee."
    ],
    "wisdom": [
        "Knowing others is intelligence; knowing yourself is true wisdom.",
        "The obstacle is the path.",
        "A wise man once said nothing at all."
    ]
}


def _flatten_quotes() -> List[str]:
    """Return a flat list of all quotes across categories."""
    return [quote for cat in _QUOTE_DB.values() for quote in cat]


def get_quote(category: Optional[str] = None) -> str:
    """Return a random quote.

    Args:
        category: Optional category name. If provided, must be one of the keys in
            ``_QUOTE_DB``. If ``None`` or unknown, a quote is chosen from the full
            collection.
    """
    if category and category in _QUOTE_DB:
        pool = _QUOTE_DB[category]
    else:
        pool = _flatten_quotes()
    return random.choice(pool)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a random Zen‑style quote."
    )
    parser.add_argument(
        "--category",
        type=str,
        help="Quote category (mindfulness, humor, wisdom)."
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    quote = get_quote(category=args.category)
    print(quote)


if __name__ == "__main__":
    main()
