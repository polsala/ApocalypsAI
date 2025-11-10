import argparse
import json
import random
import sys

# Internal quote database
QUOTES = [
    {
        "text": "The early bird gets the worm, but the second mouse gets the cheese.",
        "tags": ["humor", "wisdom"]
    },
    {
        "text": "When life gives you lemons, make lemonade. Then find someone whose life gave them vodka.",
        "tags": ["humor"]
    },
    {
        "text": "Dreams are the seedlings of reality.",
        "tags": ["inspiration", "wisdom"]
    },
    {
        "text": "Even a stopped clock is right twice a day.",
        "tags": ["humor", "wisdom"]
    },
    {
        "text": "Stars can't shine without darkness.",
        "tags": ["inspiration"]
    },
]


def get_random_quote(tag: str | None = None) -> dict:
    """Return a random quote optionally filtered by *tag*.

    Raises:
        ValueError: If no quotes match the supplied tag.
    """
    filtered = [q for q in QUOTES if tag is None or tag in q["tags"]]
    if not filtered:
        raise ValueError(f"No quotes found for tag '{tag}'")
    return random.choice(filtered)


def format_quote(quote: dict, fmt: str = "text") -> str:
    """Format *quote* according to *fmt*.

    * ``text`` – plain‑text string (default)
    * ``json`` – JSON representation
    """
    if fmt == "json":
        return json.dumps(quote)
    return quote["text"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Random Quote Generator")
    parser.add_argument("--tag", help="Filter quotes by tag")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )
    args = parser.parse_args()

    try:
        quote = get_random_quote(args.tag)
        output = format_quote(quote, args.format)
        print(output)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
