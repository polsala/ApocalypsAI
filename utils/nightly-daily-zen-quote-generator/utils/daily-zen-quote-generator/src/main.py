import argparse
import random
from typing import List, Optional, Dict

# ---------------------------------------------------------------------------
# Built‑in quote database (offline, no network required)
# ---------------------------------------------------------------------------
_QUOTES: List[Dict[str, List[str]]] = [
    {
        "text": "The journey of a thousand miles begins with one step.",
        "tags": ["mindfulness", "action"]
    },
    {
        "text": "When the mind is still, the universe surrenders.",
        "tags": ["mindfulness", "peace"]
    },
    {
        "text": "A flower does not think of competing with the flower next to it. It just blooms.",
        "tags": ["nature", "self"]
    },
    {
        "text": "The river does not drink its own water; it flows on.",
        "tags": ["nature", "flow"]
    },
    {
        "text": "Silence is a source of great strength.",
        "tags": ["mindfulness", "silence"]
    },
]


def _filter_by_theme(quotes: List[Dict[str, List[str]]], theme: Optional[str]) -> List[Dict[str, List[str]]]:
    """Return only quotes that contain the given theme tag.

    Args:
        quotes: List of quote dictionaries.
        theme:   Tag to filter by (case‑insensitive). ``None`` returns the original list.
    """
    if theme is None:
        return quotes
    theme_lower = theme.lower()
    return [q for q in quotes if theme_lower in (t.lower() for t in q["tags"])]


def get_random_quote(theme: Optional[str] = None) -> str:
    """Select a random quote, optionally filtered by *theme*.

    Args:
        theme: Optional tag to limit the quote pool.
    Returns:
        The selected quote text.
    Raises:
        ValueError: If no quotes match the requested theme.
    """
    eligible = _filter_by_theme(_QUOTES, theme)
    if not eligible:
        raise ValueError(f"No quotes found for theme '{theme}'.")
    chosen = random.choice(eligible)
    return chosen["text"]


def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="daily-zen-quote-generator",
        description="Print a random Zen‑style quote, optionally filtered by theme."
    )
    parser.add_argument(
        "--theme",
        type=str,
        help="Filter quotes by a theme tag (e.g., 'mindfulness', 'nature')."
    )
    return parser


def main() -> None:
    parser = _build_cli()
    args = parser.parse_args()
    try:
        quote = get_random_quote(args.theme)
        print(quote)
    except ValueError as exc:
        print(exc)


if __name__ == "__main__":
    main()
