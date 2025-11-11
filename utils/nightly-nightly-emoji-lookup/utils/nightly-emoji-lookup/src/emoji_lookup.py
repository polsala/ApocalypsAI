#!/usr/bin/env python3
"""
emoji_lookup.py – tiny utility to map between emoji shortcodes and Unicode characters.

Supported mappings are defined in `_EMOJI_MAP`. The module provides:
- `name_to_emoji(name: str) -> str | None`
- `emoji_to_name(emoji: str) -> str | None`
- `list_all() -> dict[str, str]`
- CLI interface.
"""

from __future__ import annotations
import argparse
import sys
from typing import Dict, Optional

# ---------------------------------------------------------------------------
# Mapping definitions (hard‑coded, deterministic, offline)
# ---------------------------------------------------------------------------
_EMOJI_MAP: Dict[str, str] = {
    ":smile:": "😄",
    ":thumbs_up:": "👍",
    ":heart:": "❤️",
    ":fire:": "🔥",
    ":star:": "⭐",
    ":thinking:": "🤔",
    ":sunglasses:": "😎",
    ":cry:": "😢",
    ":laughing:": "😂",
    ":clap:": "👏",
}

# Reverse lookup generated at import time
_EMOJI_REVERSE: Dict[str, str] = {v: k for k, v in _EMOJI_MAP.items()}


def name_to_emoji(name: str) -> Optional[str]:
    """Return the Unicode emoji for a given shortcode, or ``None`` if unknown."""
    return _EMOJI_MAP.get(name)


def emoji_to_name(emoji: str) -> Optional[str]:
    """Return the shortcode for a given Unicode emoji, or ``None`` if unknown."""
    return _EMOJI_REVERSE.get(emoji)


def list_all() -> Dict[str, str]:
    """Return a copy of the full shortcode‑to‑emoji mapping."""
    return dict(_EMOJI_MAP)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert between emoji shortcodes and Unicode characters."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--to-emoji",
        metavar="SHORTCODE",
        help="Convert a shortcode like ':smile:' to its emoji.",
    )
    group.add_argument(
        "--to-name",
        metavar="EMOJI",
        help="Convert an emoji character to its shortcode.",
    )
    group.add_argument(
        "--list",
        action="store_true",
        help="Print all supported mappings as 'shortcode => emoji'.",
    )
    return parser.parse_args(argv)


def _main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    if args.to_emoji:
        result = name_to_emoji(args.to_emoji)
        if result is None:
            print(f"Unknown shortcode: {args.to_emoji}", file=sys.stderr)
            return 1
        print(result)
    elif args.to_name:
        result = emoji_to_name(args.to_name)
        if result is None:
            print(f"Unknown emoji: {args.to_name}", file=sys.stderr)
            return 1
        print(result)
    elif args.list:
        for name, emoji in sorted(_EMOJI_MAP.items()):
            print(f"{name} => {emoji}")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
