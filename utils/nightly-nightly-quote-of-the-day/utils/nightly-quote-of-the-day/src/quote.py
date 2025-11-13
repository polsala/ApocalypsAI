import argparse
import random
from typing import List, Optional, Tuple

# Built‑in quote database: (quote, author, tags)
_QUOTES: List[Tuple[str, str, List[str]]] = [
    ("The only way to do great work is to love what you do.", "Steve Jobs", ["inspiration"]),
    ("Life is what happens when you're busy making other plans.", "John Lennon", ["philosophy"]),
    ("I have not failed. I've just found 10,000 ways that won't work.", "Thomas A. Edison", ["perseverance", "humor"]),
    ("Talk is cheap. Show me the code.", "Linus Torvalds", ["programming", "humor"]),
    ("When you have a dream, you've got to grab it and never let go.", "Carol Burnett", ["inspiration"]),
]


def _filter_by_tag(tag: Optional[str]) -> List[Tuple[str, str, List[str]]]:
    """Return a list of quotes that contain *tag* (case‑insensitive).

    If *tag* is ``None`` or empty, the full list is returned.
    """
    if not tag:
        return _QUOTES
    tag_lower = tag.lower()
    return [q for q in _QUOTES if tag_lower in (t.lower() for t in q[2])]


def get_random_quote(tag: Optional[str] = None) -> Tuple[str, str]:
    """Select a random quote (optionally filtered by *tag*).

    Returns a ``(quote, author)`` tuple.
    """
    candidates = _filter_by_tag(tag)
    if not candidates:
        raise ValueError(f"No quotes found for tag: {tag!r}")
    quote, author, _ = random.choice(candidates)
    return quote, author


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Print a random motivational quote.")
    parser.add_argument(
        "--tag",
        type=str,
        help="Optional tag to filter quotes (e.g., inspiration, humor).",
    )
    args = parser.parse_args()
    try:
        quote, author = get_random_quote(args.tag)
        print(f"\"{quote}\" — {author}")
    except ValueError as exc:
        print(exc)


if __name__ == "__main__":
    _cli()
