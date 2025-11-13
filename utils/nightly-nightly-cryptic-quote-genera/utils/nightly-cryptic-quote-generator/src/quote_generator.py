import argparse
import random
from typing import List, Optional, Dict

# ---------------------------------------------------------------------------
# Built‑in quote collection
# ---------------------------------------------------------------------------

QUOTES: List[Dict[str, List[str]]] = [
    {"text": "The moon whispers secrets to those who listen.", "tags": ["mystery", "nature"]},
    {"text": "When the clock strikes thirteen, reality bends.", "tags": ["fantasy", "time"]},
    {"text": "Silence is the loudest answer.", "tags": ["wisdom", "philosophy"]},
    {"text": "Stars are the scars of the night sky.", "tags": ["poetry", "nature"]},
    {"text": "Dreams are the drafts of tomorrow's reality.", "tags": ["inspiration", "wisdom"]},
    {"text": "A river never forgets the path it carved.", "tags": ["nature", "philosophy"]},
    {"text": "The echo of a thought lingers longer than its voice.", "tags": ["mystery", "philosophy"]},
    {"text": "Shadows dance when the sun sleeps.", "tags": ["fantasy", "nature"]},
    {"text": "Every ending is a hidden beginning.", "tags": ["wisdom", "inspiration"]},
    {"text": "Silhouettes are memories of light.", "tags": ["poetry", "mystery"]},
]

# ---------------------------------------------------------------------------
# Core functionality
# ---------------------------------------------------------------------------

def get_random_quote(tag: Optional[str] = None) -> str:
    """Return a random quote.

    If *tag* is provided, only quotes containing that tag are considered.
    Raises ``ValueError`` when no quotes match the tag.
    """
    if tag:
        filtered = [q for q in QUOTES if tag.lower() in (t.lower() for t in q["tags"])]
        if not filtered:
            raise ValueError(f"No quotes found for tag '{tag}'.")
        chosen = random.choice(filtered)
    else:
        chosen = random.choice(QUOTES)
    return chosen["text"]

# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a random cryptic quote (optionally filtered by tag)."
    )
    parser.add_argument(
        "--tag",
        type=str,
        help="Filter quotes by a tag (e.g., 'wisdom', 'mystery').",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        quote = get_random_quote(tag=args.tag)
        print(quote)
    except ValueError as exc:
        print(exc)


if __name__ == "__main__":
    main()
