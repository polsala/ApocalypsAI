import argparse
import random
import sys
from pathlib import Path
from typing import List, Optional

# A curated list of Zen‑style quotes (public domain)
QUOTES: List[str] = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged.",
    "In the middle of difficulty lies opportunity.",
    "A single word can change a life.",
    "Nature does not hurry, yet everything is accomplished.",
]


def get_random_quote(max_length: Optional[int] = None) -> Optional[str]:
    """Return a random quote, optionally respecting a maximum character length.

    If *max_length* is provided and the randomly selected quote exceeds it,
    the function returns ``None`` to signal that no suitable quote was found.
    """
    quote = random.choice(QUOTES)
    if max_length is not None and len(quote) > max_length:
        return None
    return quote


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Print a random Zen quote (offline)."
    )
    parser.add_argument(
        "--max-length",
        type=int,
        help="Maximum number of characters for the quote.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write the quote to the given file instead of stdout.",
    )
    args = parser.parse_args(argv)

    quote = get_random_quote(max_length=args.max_length)
    if quote is None:
        sys.stderr.write("No quote fits the length constraint.\n")
        return 1

    if args.output:
        try:
            args.output.write_text(quote + "\n", encoding="utf-8")
        except OSError as exc:
            sys.stderr.write(f"Failed to write to {args.output}: {exc}\n")
            return 1
    else:
        print(quote)
    return 0


if __name__ == "__main__":
    sys.exit(main())
