import argparse
import datetime
import random
from typing import List, Dict, Optional

# ---------------------------------------------------------------------------
# Internal data – a small curated list of Zen‑style quotes.
# Each entry is a dict with "text" and "theme" keys.
# ---------------------------------------------------------------------------
_QUOTES: List[Dict[str, str]] = [
    {"text": "The journey of a thousand miles begins with one step.", "theme": "mindfulness"},
    {"text": "When the mind is still, the universe surrenders.", "theme": "meditation"},
    {"text": "Nature does not hurry, yet everything is accomplished.", "theme": "nature"},
    {"text": "Silence is a source of great strength.", "theme": "silence"},
]


def _select_quote(date: datetime.date, theme: Optional[str] = None) -> str:
    """Return a deterministic quote for *date*.

    The selection is based on a pseudo‑random generator seeded with the
    ordinal value of *date*. If *theme* is provided, only quotes matching that
    theme are considered; otherwise all quotes are eligible.
    """
    eligible = [q for q in _QUOTES if theme is None or q["theme"] == theme]
    if not eligible:
        raise ValueError(f"No quotes found for theme '{theme}'.")
    seed = date.toordinal()
    rnd = random.Random(seed)
    chosen = rnd.choice(eligible)
    return chosen["text"]


def get_quote(theme: Optional[str] = None) -> str:
    """Public API – fetch the quote for *today* (or a filtered theme)."""
    today = datetime.date.today()
    return _select_quote(today, theme)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Display a deterministic Zen quote for today.")
    parser.add_argument(
        "--theme",
        type=str,
        help="Optional theme to filter quotes (e.g., mindfulness, nature).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        quote = get_quote(args.theme)
        print(quote)
    except ValueError as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
