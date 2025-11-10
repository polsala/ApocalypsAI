import argparse
import random
from typing import List, Optional

# A curated list of Zen‑style quotes.
QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is pure, joy follows like a shadow that never leaves.",
    "Sitting quietly, doing nothing, spring comes, and the grass grows by itself.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "If you understand, things are just as they are; if you do not understand, things are just as they are.",
    "To seek is to suffer; to suffer is to seek.",
    "The quieter you become, the more you can hear.",
    "When you realize nothing is lacking, the whole world belongs to you.",
    "A single moment can change a lifetime."
]


def get_zen_quote(max_length: Optional[int] = None) -> str:
    """Return a random Zen quote.

    Args:
        max_length: If provided, only quotes with length <= max_length are considered.

    Returns:
        A quote string.
    """
    eligible = QUOTES
    if max_length is not None:
        eligible = [q for q in QUOTES if len(q) <= max_length]
        if not eligible:
            raise ValueError(f"No quotes found with length <= {max_length}")
    # Randomly select a quote from the eligible list.
    return random.choice(eligible)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument(
        "--max-length",
        type=int,
        help="Maximum character length of the quote (optional).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        quote = get_zen_quote(max_length=args.max_length)
        print(quote)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
