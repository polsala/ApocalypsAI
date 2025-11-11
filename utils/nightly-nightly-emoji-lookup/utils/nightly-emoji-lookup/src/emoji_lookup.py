#!/usr/bin/env python3
"""
emoji_lookup utility
Provides bidirectional mapping between shortcodes and Unicode emojis.
"""

import argparse
import sys
from typing import Dict, Optional

# Minimal built‑in mapping; can be extended.
_EMOJI_MAP: Dict[str, str] = {
    ":smile:": "😄",
    ":thumbsup:": "👍",
    ":heart:": "❤️",
    ":fire:": "🔥",
    ":rocket:": "🚀",
    ":coffee:": "☕",
    ":thinking:": "🤔",
    ":sunglasses:": "😎",
    ":poop:": "💩",
    ":cat:": "🐱",
}

# Reverse mapping generated at import time.
_SHORTCODE_MAP: Dict[str, str] = {v: k for k, v in _EMOJI_MAP.items()}


def shortcode_to_emoji(shortcode: str) -> Optional[str]:
    """Return the emoji for a given shortcode, or ``None`` if unknown."""
    return _EMOJI_MAP.get(shortcode)


def emoji_to_shortcode(emoji: str) -> Optional[str]:
    """Return the shortcode for a given emoji, or ``None`` if unknown."""
    return _SHORTCODE_MAP.get(emoji)


def _parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Convert between emoji shortcodes and Unicode characters."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--to-emoji",
        metavar="SHORTCODE",
        help="Convert a shortcode (e.g., :smile:) to its emoji.",
    )
    group.add_argument(
        "--to-shortcode",
        metavar="EMOJI",
        help="Convert an emoji character to its shortcode.",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    args = _parse_args(argv)

    if args.to_emoji:
        result = shortcode_to_emoji(args.to_emoji)
        if result is None:
            print(f"Unknown shortcode: {args.to_emoji}", file=sys.stderr)
            return 1
        print(result)
    else:
        result = emoji_to_shortcode(args.to_shortcode)
        if result is None:
            print(f"Unknown emoji: {args.to_shortcode}", file=sys.stderr)
            return 1
        print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
