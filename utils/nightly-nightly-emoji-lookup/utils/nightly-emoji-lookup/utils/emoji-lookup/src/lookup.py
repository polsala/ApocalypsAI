"""
emoji_lookup.lookup

A tiny, self‑contained utility for converting between emoji shortcodes and Unicode
characters. No external data sources – the mapping is hard‑coded for a curated
subset of popular emojis.
"""

from __future__ import annotations
import argparse
import sys
from typing import Dict, Optional

# Minimal emoji mapping
_EMOJI_MAP: Dict[str, str] = {
    "grinning": "😀",
    "smile": "😄",
    "laughing": "😆",
    "wink": "😉",
    "thumbsup": "👍",
    "heart": "❤️",
    "star": "⭐",
    "fire": "🔥",
    "clap": "👏",
    "thinking": "🤔",
}

# Reverse map generated at import time
_REVERSE_MAP: Dict[str, str] = {v: k for k, v in _EMOJI_MAP.items()}


def name_to_emoji(name: str) -> Optional[str]:
    """Return the emoji character for a given shortcode (without colons).

    Args:
        name: Shortcode like ``"smile"`` or ``"smile"`` with surrounding colons.

    Returns:
        The Unicode emoji string or ``None`` if not found.
    """
    clean = name.strip(":")
    return _EMOJI_MAP.get(clean)


def emoji_to_name(emoji: str) -> Optional[str]:
    """Return the shortcode for a given emoji character.

    Args:
        emoji: A single Unicode emoji.

    Returns:
        The shortcode without colons or ``None`` if unknown.
    """
    return _REVERSE_MAP.get(emoji)


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Convert between emoji shortcodes and Unicode characters."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--to-emoji",
        metavar="NAME",
        help="Convert a shortcode (e.g., 'smile') to its emoji.",
    )
    group.add_argument(
        "--to-name",
        metavar="EMOJI",
        help="Convert an emoji character to its shortcode.",
    )
    args = parser.parse_args()

    if args.to_emoji:
        result = name_to_emoji(args.to_emoji)
        if result is None:
            print(f"Unknown shortcode: {args.to_emoji}", file=sys.stderr)
            sys.exit(1)
        print(result)
    else:
        result = emoji_to_name(args.to_name)
        if result is None:
            print(f"Unknown emoji: {args.to_name}", file=sys.stderr)
            sys.exit(1)
        print(result)


if __name__ == "__main__":
    _cli()
