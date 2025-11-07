import argparse
import random
from typing import List, Optional

# ---------------------------------------------------------------------------
# Built‑in quote database (tiny but illustrative)
# ---------------------------------------------------------------------------
_QUOTES = {
    "mindfulness": [
        "When you realize nothing is lacking, the whole world belongs to you.",
        "Walk as if you are kissing the Earth with your feet.",
    ],
    "impermanence": [
        "All things are dust in the wind; cherish the breath you have now.",
        "The river never drinks the same water twice.",
    ],
    "general": [
        "The obstacle is the path.",
        "Silence is a source of great strength.",
        "When the mind is still, the universe surrenders.",
    ],
}


def _flatten_quotes() -> List[str]:
    """Return a flat list of all quotes across tags."""
    return [quote for quotes in _QUOTES.values() for quote in quotes]


def get_quote(tag: Optional[str] = None) -> str:
    """Return a random quote.

    Args:
        tag: Optional tag to filter quotes. If the tag does not exist, falls back
            to the "general" collection.
    Returns:
        A randomly selected quote string.
    """
    if tag and tag in _QUOTES:
        pool = _QUOTES[tag]
    else:
        # Use general if tag missing or None
        pool = _QUOTES.get(tag, _QUOTES["general"]) if tag else _QUOTES["general"]
    # Random choice – deterministic in tests via mocking
    return random.choice(pool)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a random Zen‑style quote."
    )
    parser.add_argument(
        "--tag",
        type=str,
        help="Optional tag to filter quotes (mindfulness, impermanence, ...).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    quote = get_quote(tag=args.tag)
    print(quote)


if __name__ == "__main__":
    main()
