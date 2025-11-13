"""
quote.py – Random Quote of the Day utility.

Provides a small collection of inspirational quotes and a CLI to print a random one.
"""

import argparse
import random
from typing import List, Optional, Dict

# Built‑in quote collection
QUOTES: List[Dict[str, List[str]]] = [
    {
        "text": "The only limit to our realization of tomorrow is our doubts today.",
        "tags": ["inspiration", "future"]
    },
    {
        "text": "Life is what happens when you're busy making other plans.",
        "tags": ["life", "wisdom"]
    },
    {
        "text": "In the middle of difficulty lies opportunity.",
        "tags": ["wisdom", "motivation"]
    },
    {
        "text": "Stay hungry, stay foolish.",
        "tags": ["inspiration", "tech"]
    },
]

def get_random_quote(tag: Optional[str] = None) -> str:
    """
    Return a random quote. If ``tag`` is supplied, only quotes containing that tag are considered.
    Raises ``ValueError`` if no quotes match the tag.
    """
    if tag:
        filtered = [q for q in QUOTES if tag.lower() in (t.lower() for t in q["tags"])]
        if not filtered:
            raise ValueError(f"No quotes found for tag '{tag}'.")
        pool = filtered
    else:
        pool = QUOTES
    choice = random.choice(pool)
    return choice["text"]

def main() -> None:
    parser = argparse.ArgumentParser(description="Print a random inspirational quote.")
    parser.add_argument(
        "--tag",
        type=str,
        help="Optional tag to filter quotes (e.g., 'wisdom').",
    )
    args = parser.parse_args()
    try:
        quote = get_random_quote(tag=args.tag)
        print(quote)
    except ValueError as exc:
        print(exc)

if __name__ == "__main__":
    main()
