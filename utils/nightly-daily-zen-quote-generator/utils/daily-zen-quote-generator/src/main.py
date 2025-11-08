import argparse
import random
from typing import List, Dict

# ---------------------------------------------------------------------------
# Quote database (static, offline)
# ---------------------------------------------------------------------------
_QUOTES: List[Dict[str, object]] = [
    {"text": "The journey of a thousand miles begins with one step.", "tags": ["growth", "mindfulness"]},
    {"text": "When you realize nothing is lacking, the whole world belongs to you.", "tags": ["simplicity", "mindfulness"]},
    {"text": "Silence is a source of great strength.", "tags": ["mindfulness", "focus"]},
    {"text": "A jug fills drop by drop.", "tags": ["patience", "growth"]},
    {"text": "The obstacle is the path.", "tags": ["growth", "resilience"]},
    {"text": "Let go or be dragged.", "tags": ["simplicity", "freedom"]},
    {"text": "When the mind is still, the universe surrenders.", "tags": ["mindfulness", "peace"]},
    {"text": "A single arrow is easily broken; a bundle is unbreakable.", "tags": ["teamwork", "growth"]},
    {"text": "To know the road ahead, ask those who have traveled it.", "tags": ["wisdom", "learning"]},
    {"text": "The softest thing in the world beats the hardest.", "tags": ["flexibility", "strength"]},
    # ... more quotes could be added here ...
]


def filter_quotes(theme: str | None) -> List[Dict[str, object]]:
    """Return quotes that contain the given theme tag.

    If *theme* is ``None`` or empty, the full list is returned.
    """
    if not theme:
        return _QUOTES
    lowered = theme.lower()
    return [q for q in _QUOTES if lowered in (tag.lower() for tag in q["tags"])]


def pick_random_quote(quotes: List[Dict[str, object]]) -> Dict[str, object]:
    """Select a random quote from *quotes*.

    This function is isolated for easier testing/mocking.
    """
    return random.choice(quotes)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument(
        "--theme",
        type=str,
        help="Filter quotes by a theme tag (e.g., mindfulness, growth).",
    )
    args = parser.parse_args()

    eligible = filter_quotes(args.theme)
    if not eligible:
        print(f"No quotes found for theme '{args.theme}'.")
        return

    quote = pick_random_quote(eligible)
    print(quote["text"])


if __name__ == "__main__":
    main()
