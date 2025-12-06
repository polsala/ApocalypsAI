import argparse
import random
import sys

# Mock rationale: a static list of inspirational Zen quotes; no external I/O.
QUOTES = [
    "The journey of a thousand miles begins with one step.",
    "When the mind is still, the universe surrenders.",
    "Simplicity is the ultimate sophistication.",
    "Let go of the past, embrace the present.",
    "Silence is a source of great strength."
]

def get_random_quote() -> str:
    """Return a random quote from the static list.

    The function is deliberately simple to keep the utility self‑contained.
    """
    return random.choice(QUOTES)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Print a random Zen quote to stdout."
    )
    parser.add_argument(
        "-n",
        "--no-newline",
        action="store_true",
        help="Do not append a trailing newline."
    )
    return parser

def main(argv: list | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    quote = get_random_quote()
    end = "" if args.no_newline else "\n"
    sys.stdout.write(quote + end)

if __name__ == "__main__":
    main()
