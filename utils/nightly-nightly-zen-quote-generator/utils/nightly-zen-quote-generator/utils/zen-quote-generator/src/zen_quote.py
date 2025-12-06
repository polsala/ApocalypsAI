import argparse
import random
import sys

# A small curated list of Zen‑style quotes.
QUOTES = [
    {"quote": "The journey of a thousand miles begins with one step.", "theme": "motivation"},
    {"quote": "When the mind is still, the universe surrenders.", "theme": "mindfulness"},
    {"quote": "Simplicity is the ultimate sophistication.", "theme": "simplicity"},
    {"quote": "Let go of the past, embrace the present.", "theme": "mindfulness"},
]


def get_random_quote(theme: str | None = None) -> str:
    """Return a random quote, optionally filtered by *theme*.

    Args:
        theme: If provided, only quotes matching this theme are considered.
    Returns:
        A randomly selected quote string.
    Raises:
        ValueError: If no quotes match the requested theme.
    """
    filtered = [q["quote"] for q in QUOTES if theme is None or q["theme"] == theme]
    if not filtered:
        raise ValueError(f"No quotes found for theme '{theme}'")
    return random.choice(filtered)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument("--theme", help="Filter quotes by theme")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    try:
        quote = get_random_quote(args.theme)
        print(quote)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
