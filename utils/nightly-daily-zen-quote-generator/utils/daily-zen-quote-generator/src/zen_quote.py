import argparse
import random
from typing import List, Optional, Dict

# ---------------------------------------------------------------------------
# Built‑in collection of Zen‑style quotes. Each entry has a ``text`` and a list
# of ``tags`` that describe its theme. The collection is deliberately small
# for the example but can be expanded without changing any logic.
# ---------------------------------------------------------------------------
_QUOTES: List[Dict[str, List[str]]] = [
    {
        "text": "The journey of a thousand miles begins with a single step.",
        "tags": ["mindfulness", "motivation"]
    },
    {
        "text": "When you realize nothing is lacking, the whole world belongs to you.",
        "tags": ["mindfulness", "philosophy"]
    },
    {
        "text": "If you cannot find the truth within yourself, look at the coffee.",
        "tags": ["humor", "daily"]
    },
    {
        "text": "A calm mind is like a still lake – it reflects the sky clearly.",
        "tags": ["mindfulness", "nature"]
    },
]


def _filter_by_tag(tag: str) -> List[Dict[str, List[str]]]:
    """Return a list of quotes that contain *tag* in their ``tags`` field.

    Args:
        tag: Tag to filter by (case‑insensitive).
    Returns:
        List of matching quote dictionaries. Empty list if none match.
    """
    lower_tag = tag.lower()
    return [q for q in _QUOTES if lower_tag in (t.lower() for t in q["tags"])]


def get_random_quote(tag: Optional[str] = None) -> str:
    """Select a random quote, optionally filtered by *tag*.

    If *tag* is provided but no quotes match, a ``ValueError`` is raised.
    """
    pool = _filter_by_tag(tag) if tag else _QUOTES
    if not pool:
        raise ValueError(f"No quotes found for tag '{tag}'.")
    chosen = random.choice(pool)
    return chosen["text"]


def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument(
        "--tag",
        type=str,
        help="Optional tag to filter quotes (e.g., 'mindfulness', 'humor')."
    )
    return parser


def main() -> None:
    parser = _build_cli()
    args = parser.parse_args()
    try:
        quote = get_random_quote(tag=args.tag)
        print(quote)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
