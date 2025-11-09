import argparse
import random
from typing import List, Optional, Dict

# A small curated list of Zen‑style quotes.
_QUOTES: List[Dict[str, List[str]]] = [
    {"text": "The journey of a thousand miles begins with one step.", "tags": ["mindfulness", "action"]},
    {"text": "When the mind is still, the universe surrenders.", "tags": ["stillness", "peace"]},
    {"text": "Let go of the past, and the future will take care of itself.", "tags": ["release", "future"]},
    {"text": "Silence is a source of great strength.", "tags": ["silence", "strength"]},
    {"text": "Observe the clouds; they come and go without a trace.", "tags": ["observation", "impermanence"]},
]


def _filter_by_tag(tag: Optional[str]) -> List[Dict[str, List[str]]]:
    """Return quotes that contain *tag* in their tag list.

    If *tag* is ``None`` or empty, the full list is returned.
    """
    if not tag:
        return _QUOTES
    return [q for q in _QUOTES if tag.lower() in (t.lower() for t in q["tags"])]


def get_random_quote(tag: Optional[str] = None) -> str:
    """Return a random quote, optionally filtered by *tag*.

    Raises:
        ValueError: If no quotes match the supplied tag.
    """
    candidates = _filter_by_tag(tag)
    if not candidates:
        raise ValueError(f"No quotes found for tag '{tag}'.")
    # ``random.choice`` is isolated for easy mocking in tests.
    quote = random.choice(candidates)
    return quote["text"]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a random Zen‑style quote.")
    parser.add_argument(
        "--tag",
        type=str,
        help="Filter quotes by tag (e.g., 'mindfulness').",
        default=None)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        print(get_random_quote(args.tag))
    except ValueError as exc:
        # Friendly error message for CLI users.
        print(exc)


if __name__ == "__main__":
    main()
