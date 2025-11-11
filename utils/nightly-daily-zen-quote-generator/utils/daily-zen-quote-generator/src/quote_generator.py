import argparse
import random
import sys

# A small curated list of Zen‑inspired sayings.
QUOTES = [
    "The journey of a thousand miles begins with one step.",
    "Simplicity is the ultimate sophistication.",
    "When the mind is still, the universe surrenders.",
    "Knowing others is intelligence; knowing yourself is true wisdom.",
    "The obstacle is the path.",
]


def get_random_quote(max_length: int | None = None) -> str:
    """Return a random quote.

    If *max_length* is provided, only quotes whose length is less than or equal to
    that value are considered.  Raises ``ValueError`` when no quote satisfies the
    constraint.
    """
    filtered = [q for q in QUOTES if max_length is None or len(q) <= max_length]
    if not filtered:
        raise ValueError("No quotes match the given max_length criteria.")
    return random.choice(filtered)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print a random Zen quote")
    parser.add_argument(
        "--max-length",
        type=int,
        help="Maximum length of the quote to display",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    try:
        quote = get_random_quote(args.max_length)
        print(quote)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
