"""CLI entry point for Daily Zen Quote."""

import argparse
import sys

from .quote import get_random_quote


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="daily-zen-quote",
        description="Print a random Zen‑inspired quote."
    )
    parser.add_argument(
        "--theme",
        type=str,
        help="Optional theme to filter quotes (e.g., nature, mindfulness, humor)."
    )
    args = parser.parse_args(argv)

    try:
        quote = get_random_quote(theme=args.theme)
        print(quote)
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
