"""emoji-lookup – map short names to Unicode emojis.

The module is deliberately tiny and has **no external dependencies**. It ships with a curated
subset of common emojis, but you can extend ``EMOJI_MAP`` as needed.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict

# ---------------------------------------------------------------------------
# Emoji dictionary – deterministic, offline, and fully typed.
# ---------------------------------------------------------------------------
EMOJI_MAP: Dict[str, str] = {
    "grinning": "😀",
    "smile": "😄",
    "laugh": "😂",
    "wink": "😉",
    "thumbs_up": "👍",
    "thumbs_down": "👎",
    "heart": "❤️",
    "star": "⭐",
    "fire": "🔥",
    "rocket": "🚀",
    "clap": "👏",
    "party": "🥳",
    "sunglasses": "😎",
    "thinking": "🤔",
    "cry": "😢",
    "poop": "💩",
    "ok_hand": "👌",
    "raised_hands": "🙌",
    "muscle": "💪",
    "rainbow": "🌈",
    "sun": "☀️",
    "moon": "🌙",
    "coffee": "☕",
    "pizza": "🍕",
    "cake": "🍰",
    "beer": "🍺",
    "dog": "🐶",
    "cat": "🐱",
    "unicorn": "🦄",
    "robot": "🤖",
    "alien": "👽",
    "ghost": "👻",
    "skull": "💀",
    "warning": "⚠️",
    "check": "✅",
    "cross": "❌",
    "question": "❓",
    "exclamation": "❗",
}

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def get_emoji(name: str) -> str:
    """Return the Unicode emoji for *name*.

    Parameters
    ----------
    name:
        The short, snake_case identifier (e.g. ``"thumbs_up"``).

    Returns
    -------
    str
        The corresponding emoji character.

    Raises
    ------
    KeyError
        If *name* is not present in :data:`EMOJI_MAP`.
    """
    try:
        return EMOJI_MAP[name]
    except KeyError as exc:
        raise KeyError(f"Emoji name '{name}' not found. Available names: {', '.join(sorted(EMOJI_MAP))}") from exc

# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lookup a Unicode emoji by short name.")
    parser.add_argument(
        "name",
        help="Short name of the emoji (e.g., 'thumbs_up'). Use snake_case as listed in the README.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        emoji = get_emoji(args.name)
        print(emoji)
        return 0
    except KeyError as err:
        print(err, file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
