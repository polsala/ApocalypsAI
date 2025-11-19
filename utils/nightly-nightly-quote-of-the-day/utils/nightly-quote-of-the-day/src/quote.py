import argparse
import random
from typing import List, Dict

# Built‑in quote database
_QUOTES: List[Dict[str, str]] = [
    {"text": "The only limit to our realization of tomorrow is our doubts of today.", "tag": "wisdom"},
    {"text": "Life is what happens when you're busy making other plans.", "tag": "wisdom"},
    {"text": "I have not failed. I've just found 10,000 ways that won't work.", "tag": "humor"},
    {"text": "If at first you don’t succeed, then skydiving definitely isn’t for you.", "tag": "humor"},
    {"text": "Talk is cheap. Show me the code.", "tag": "tech"},
    {"text": "In order to be irreplaceable, one must always be different.", "tag": "tech"},
]


def _filter_quotes(tag: str | None) -> List[Dict[str, str]]:
    """Return quotes matching *tag* (or all if *tag* is None)."""
    if tag is None:
        return _QUOTES
    return [q for q in _QUOTES if q["tag"].lower() == tag.lower()]


def get_random_quote(tag: str | None = None) -> str:
    """Select a random quote, optionally limited to a *tag*.

    Raises:
        ValueError: If *tag* is provided but no quotes match.
    """
    candidates = _filter_quotes(tag)
    if not candidates:
        raise ValueError(f"No quotes found for tag '{tag}'.")
    # Mock rationale: random.choice is deterministic when patched in tests.
    quote = random.choice(candidates)
    return quote["text"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a random inspirational quote.")
    parser.add_argument(
        "--tag",
        type=str,
        help="Optional tag to filter quotes (e.g., wisdom, humor, tech).",
    )
    args = parser.parse_args()
    try:
        print(get_random_quote(args.tag))
    except ValueError as exc:
        print(exc)


if __name__ == "__main__":
    main()
