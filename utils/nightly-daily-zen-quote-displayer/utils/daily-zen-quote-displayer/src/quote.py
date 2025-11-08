import argparse
import datetime
import json
import random
import sys
from typing import List, Optional, Dict

# ---------------------------------------------------------------------------
# Data: a small curated list of Zen quotes. Each entry has a "text" and a list of
# "tags" that can be used for theme filtering.
# ---------------------------------------------------------------------------
_QUOTES: List[Dict[str, List[str]]] = [
    {
        "text": "The journey of a thousand miles begins with one step.",
        "tags": ["beginning", "action"]
    },
    {
        "text": "When the mind is still, the universe surrenders.",
        "tags": ["mindfulness", "stillness"]
    },
    {
        "text": "All things are impermanent; cherish each moment.",
        "tags": ["impermanence", "presence"]
    },
    {
        "text": "Silence is a source of great strength.",
        "tags": ["silence", "strength"]
    },
    {
        "text": "The obstacle is the path.",
        "tags": ["obstacle", "growth"]
    }
]


def _load_quotes() -> List[Dict[str, List[str]]]:
    """Return the internal list of quotes.

    In a real‑world utility this could read from an external JSON/YAML file.
    Keeping it in‑code makes the utility self‑contained.
    """
    return _QUOTES


def _filter_by_theme(quotes: List[Dict[str, List[str]]], theme: Optional[str]) -> List[Dict[str, List[str]]]:
    """Return only quotes that contain *theme* in their tags.

    Matching is case‑insensitive. If *theme* is ``None`` the original list is
    returned unchanged.
    """
    if theme is None:
        return quotes
    theme_lower = theme.lower()
    filtered = [q for q in quotes if any(tag.lower() == theme_lower for tag in q["tags"])]
    return filtered


def _select_quote(quotes: List[Dict[str, List[str]]], today: datetime.date) -> Optional[Dict[str, List[str]]]:
    """Deterministically pick a quote based on *today*.

    The ISO string of *today* seeds a ``random.Random`` instance, guaranteeing
    reproducibility without affecting the global random state.
    """
    if not quotes:
        return None
    seed = today.isoformat()
    rng = random.Random(seed)
    index = rng.randrange(len(quotes))
    return quotes[index]


def get_daily_quote(theme: Optional[str] = None, today: Optional[datetime.date] = None) -> Optional[str]:
    """Public API: return the quote of the day as a string.

    Parameters
    ----------
    theme: optional tag to filter quotes.
    today: optional ``datetime.date`` for testing; defaults to ``datetime.date.today()``.
    """
    if today is None:
        today = datetime.date.today()
    quotes = _load_quotes()
    quotes = _filter_by_theme(quotes, theme)
    selected = _select_quote(quotes, today)
    return selected["text"] if selected else None


def _parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a deterministic Zen quote of the day.")
    parser.add_argument("--theme", type=str, help="Filter quotes by a tag (case‑insensitive)")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = _parse_args(argv or sys.argv[1:])
    quote = get_daily_quote(theme=args.theme)
    if quote:
        print(quote)
        return 0
    else:
        print("No quote found for the given theme.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
