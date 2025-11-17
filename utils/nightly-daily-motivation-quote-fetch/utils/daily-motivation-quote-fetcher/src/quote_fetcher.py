import argparse
import random
from typing import List, Dict, Optional

# ---------------------------------------------------------------------------
# Quote database (static, offline)
# ---------------------------------------------------------------------------
_QUOTES: List[Dict[str, str]] = [
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "theme": "creativity"},
    {"text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius", "theme": "perseverance"},
    {"text": "Dream big and dare to fail.", "author": "Norman Vaughan", "theme": "ambition"},
    {"text": "Life is 10% what happens to us and 90% how we react to it.", "author": "Charles R. Swindoll", "theme": "mindset"},
    {"text": "The best way to predict the future is to invent it.", "author": "Alan Kay", "theme": "innovation"},
]


def _filter_by_theme(quotes: List[Dict[str, str]], theme: Optional[str]) -> List[Dict[str, str]]:
    """Return only quotes matching *theme* (case‑insensitive)."""
    if not theme:
        return quotes
    theme_lower = theme.lower()
    return [q for q in quotes if q["theme"].lower() == theme_lower]


def get_random_quote(theme: Optional[str] = None) -> Dict[str, str]:
    """Return a random quote dict optionally filtered by *theme*.

    The function is deliberately pure apart from the random.choice call, making it easy to mock in tests.
    """
    eligible = _filter_by_theme(_QUOTES, theme)
    if not eligible:
        raise ValueError(f"No quotes found for theme '{theme}'.")
    # Random selection – deterministic when seed is set (tests do this).
    return random.choice(eligible)


def _format_quote(quote: Dict[str, str]) -> str:
    return f"\"{quote['text']}\" — {quote['author']}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a random motivational quote.")
    parser.add_argument(
        "--theme",
        type=str,
        help="Optional theme to filter quotes (e.g., perseverance, creativity).",
    )
    args = parser.parse_args()
    try:
        quote = get_random_quote(args.theme)
        print(_format_quote(quote))
    except ValueError as exc:
        print(exc)


if __name__ == "__main__":
    main()
