import argparse
import random
from typing import List, Dict, Optional

# ---------------------------------------------------------------------------
# Quote data – a small curated collection of Zen‑style sayings.
# Each entry is a dict with 'text' and a list of 'tags'.
# ---------------------------------------------------------------------------
QUOTES: List[Dict[str, List[str]]] = [
    {
        "text": "The journey of a thousand miles begins with one step.",
        "tags": ["mindfulness", "motivation"]
    },
    {
        "text": "When the mind is still, the universe surrenders.",
        "tags": ["philosophy", "peace"]
    },
    {
        "text": "A cup of tea is a cup of peace.",
        "tags": ["humor", "mindfulness"]
    },
    {
        "text": "If you cannot find the truth within yourself, you will never find it elsewhere.",
        "tags": ["philosophy", "self"]
    },
    {
        "text": "The sound of one hand clapping is the echo of your own thoughts.",
        "tags": ["humor", "philosophy"]
    }
]


def get_random_quote(tag: Optional[str] = None) -> str:
    """Return a random quote.

    If *tag* is provided, only quotes containing that tag are considered.
    Raises ``ValueError`` when no quotes match the filter.
    """
    if tag:
        filtered = [q for q in QUOTES if tag.lower() in (t.lower() for t in q["tags"])]
    else:
        filtered = QUOTES

    if not filtered:
        raise ValueError(f"No quotes found for tag '{tag}'.")

    chosen = random.choice(filtered)
    return chosen["text"]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument(
        "--tag",
        type=str,
        help="Filter quotes by tag (e.g., 'mindfulness')."
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        quote = get_random_quote(tag=args.tag)
        print(quote)
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
