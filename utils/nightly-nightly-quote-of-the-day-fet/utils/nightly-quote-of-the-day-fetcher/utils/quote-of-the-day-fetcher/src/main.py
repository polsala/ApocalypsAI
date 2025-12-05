import argparse
import random
import sys

# A small, static collection of quotes. Each entry may have one or more tags.
QUOTES = [
    {
        "quote": "The only limit to our realization of tomorrow is our doubts of today.",
        "author": "Franklin D. Roosevelt",
        "tags": ["inspiration"]
    },
    {
        "quote": "Life is what happens when you're busy making other plans.",
        "author": "John Lennon",
        "tags": ["life"]
    },
    {
        "quote": "Be yourself; everyone else is already taken.",
        "author": "Oscar Wilde",
        "tags": ["humor"]
    }
]


def get_quote(tag: str | None = None) -> dict:
    """Return a random quote, optionally filtered by *tag*.

    Args:
        tag: If provided, only quotes containing this tag are considered.

    Raises:
        ValueError: When no quotes match the requested tag.
    """
    filtered = [q for q in QUOTES if tag is None or tag in q["tags"]]
    if not filtered:
        raise ValueError(f"No quotes found for tag '{tag}'")
    return random.choice(filtered)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print a random quote.")
    parser.add_argument("--tag", help="Filter quotes by tag")
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    try:
        quote = get_quote(args.tag)
        print(f'"{quote["quote"]}" — {quote["author"]}')
    except ValueError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
