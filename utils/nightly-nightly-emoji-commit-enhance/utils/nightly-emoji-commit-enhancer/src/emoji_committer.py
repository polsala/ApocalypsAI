"""emoji_committer.py

A tiny utility that adds an appropriate emoji prefix to a git commit message.

Usage:
    python -m utils.nightly-emoji-commit-enhancer.src.emoji_committer "Add new feature"
    # → ✨ Add new feature

If the script receives no command‑line argument, it reads from STDIN.
"""

import sys
import argparse
from typing import Dict

# Mapping of keyword triggers to emojis
EMOJI_MAP: Dict[str, str] = {
    "feat": "✨",
    "feature": "✨",
    "add": "✨",
    "fix": "🐛",
    "bug": "🐛",
    "docs": "📝",
    "doc": "📝",
    "refactor": "🔨",
    "test": "✅",
    "tests": "✅",
    "chore": "🔧",
    "style": "🎨",
    "perf": "⚡",
    "performance": "⚡",
}

DEFAULT_EMOJI = "🔧"

def _detect_emoji(message: str) -> str:
    """Return the first matching emoji based on keyword presence.

    The detection is case‑insensitive and looks for whole‑word matches.
    """
    lowered = message.lower()
    for keyword, emoji in EMOJI_MAP.items():
        if keyword in lowered:
            return emoji
    return DEFAULT_EMOJI


def add_emoji(message: str) -> str:
    """Prepend an appropriate emoji to *message*.

    If the message already starts with an emoji (detected via a leading Unicode emoji
    character), the original message is returned unchanged.
    """
    stripped = message.strip()
    if not stripped:
        return stripped
    # Simple check: if first character is an emoji (range check)
    first_char = stripped[0]
    if "\U0001F300" <= first_char <= "\U0001FAFF":
        return stripped
    emoji = _detect_emoji(stripped)
    return f"{emoji} {stripped}"


def _parse_args(argv):
    parser = argparse.ArgumentParser(description="Add an emoji prefix to a git commit message.")
    parser.add_argument("message", nargs="?", help="Commit message. If omitted, reads from STDIN.")
    return parser.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv or sys.argv[1:])
    if args.message is not None:
        input_msg = args.message
    else:
        # Read from stdin until EOF
        input_msg = sys.stdin.read()
    result = add_emoji(input_msg)
    print(result)


if __name__ == "__main__":
    main()
