"""emoji_lookup.py

A tiny offline emoji lookup utility.

Provides:
- `EMOJI_DB`: a mapping of keywords to lists of emojis.
- `search(keyword: str) -> List[str]`: returns all emojis whose keyword contains the query.
- CLI entry point using `argparse`.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Dict

# A small curated emoji database. Keys are lower‑case keywords.
EMOJI_DB: Dict[str, List[str]] = {
    "smile": ["😄", "😊", "😁"],
    "laugh": ["😂", "🤣"],
    "heart": ["❤️", "💖", "💘"],
    "thumbs": ["👍", "👎", "👌"],
    "fire": ["🔥", "♨️"],
    "star": ["⭐", "🌟", "✨"],
    "cat": ["🐱", "😺", "😸"],
    "dog": ["🐶", "🐕", "🐩"],
    "party": ["🥳", "🎉", "🎊"],
    "coffee": ["☕", "🧋"],
}


def search(keyword: str) -> List[str]:
    """Return a flat list of emojis whose keyword contains the query.

    The search is case‑insensitive and matches if the query is a substring
    of any keyword in the database.
    """
    query = keyword.lower().strip()
    if not query:
        return []
    matches: List[str] = []
    for key, emojis in EMOJI_DB.items():
        if query in key:
            matches.extend(emojis)
    return matches


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="emoji_lookup",
        description="Search for emojis by keyword (offline).",
    )
    parser.add_argument(
        "keyword",
        nargs="?",
        help="Keyword to search for. If omitted, reads from stdin.",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.keyword:
        keywords = [args.keyword]
    else:
        # Read lines from stdin, ignore empty lines
        keywords = [line.strip() for line in sys.stdin if line.strip()]
    all_results: List[str] = []
    for kw in keywords:
        all_results.extend(search(kw))
    if all_results:
        print(" ".join(all_results))
    else:
        # No matches – exit with code 1 to signal "nothing found"
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
