import argparse
import random
from typing import List, Optional, Dict

# ---------------------------------------------------------------------------
# Quote database (static, offline)
# ---------------------------------------------------------------------------

_QUOTES: List[Dict[str, str]] = [
    {"text": "Believe you can and you're halfway there.", "category": "inspiration"},
    {"text": "The only way to do great work is to love what you do.", "category": "inspiration"},
    {"text": "I am not lazy, I am on energy‑saving mode.", "category": "humor"},
    {"text": "Why do programmers prefer dark mode? Because light attracts bugs!", "category": "humor"},
    {"text": "Dream big. Start small. Act now.", "category": "productivity"},
    {"text": "Focus on the step you’re on, not the whole staircase.", "category": "productivity"},
]


def _filter_quotes(category: Optional[str]) -> List[Dict[str, str]]:
    """Return quotes matching *category* (case‑insensitive). If *category* is ``None``
    all quotes are returned.
    """
    if category is None:
        return _QUOTES
    lowered = category.lower()
    return [q for q in _QUOTES if q["category"].lower() == lowered]


def get_random_quote(category: Optional[str] = None) -> str:
    """Pick a random quote optionally limited to *category*.

    Raises:
        ValueError: If the filtered list is empty.
    """
    candidates = _filter_quotes(category)
    if not candidates:
        raise ValueError(f"No quotes found for category '{category}'.")
    # ``random.choice`` is isolated for easy mocking in tests.
    quote = random.choice(candidates)
    return quote["text"]


def _build_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="daily-motivation-quote",
        description="Print a random motivational quote.",
    )
    parser.add_argument(
        "--category",
        type=str,
        help="Filter quotes by category (e.g., inspiration, humor, productivity).",
    )
    return parser


def main() -> None:
    parser = _build_cli()
    args = parser.parse_args()
    try:
        quote = get_random_quote(args.category)
        print(quote)
    except ValueError as exc:
        # Friendly error message for CLI users.
        print(exc)


if __name__ == "__main__":
    main()
