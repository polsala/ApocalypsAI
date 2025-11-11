import argparse
import random
import sys

# Mock rationale: a small, static collection keeps the utility self‑contained and offline.
QUOTES = [
    {"text": "The journey of a thousand miles begins with one step.", "theme": "motivation"},
    {"text": "When the mind is still, the universe surrenders.", "theme": "mindfulness"},
    {"text": "Simplicity is the ultimate sophistication.", "theme": "simplicity"},
    {"text": "Let go of what you cannot change.", "theme": "acceptance"},
]


def get_random_quote(theme: str | None = None) -> dict:
    """Return a random quote, optionally filtered by *theme*.

    Raises:
        ValueError: If no quotes match the requested theme.
    """
    filtered = [q for q in QUOTES if theme is None or q["theme"] == theme]
    if not filtered:
        raise ValueError(f"No quotes found for theme '{theme}'")
    # Mock rationale: `random.choice` is patched in tests for determinism.
    return random.choice(filtered)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a random Zen‑inspired quote.")
    parser.add_argument("--theme", help="Filter quotes by theme (e.g., motivation, mindfulness).")
    args = parser.parse_args()
    try:
        quote = get_random_quote(args.theme)
        print(f'"{quote["text"]}" — {quote["theme"].title()}')
    except ValueError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
