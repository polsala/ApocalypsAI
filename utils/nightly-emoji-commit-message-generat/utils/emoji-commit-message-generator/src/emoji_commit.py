"""emoji_commit.py

Utility to generate an emoji‑prefixed git commit message.

Public API:
    emoji_commit_message(description: str) -> str
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict

# Mock rationale: a deterministic, lightweight keyword‑to‑emoji map.
_EMOJI_MAP: Dict[str, str] = {
    "add": "✨",
    "create": "✨",
    "init": "🚀",
    "remove": "🗑️",
    "delete": "🗑️",
    "fix": "🐛",
    "bug": "🐛",
    "refactor": "🔧",
    "update": "🔄",
    "upgrade": "⬆️",
    "downgrade": "⬇️",
    "merge": "🔀",
    "revert": "⏪",
    "test": "✅",
    "docs": "📝",
    "documentation": "📝",
    "security": "🔐",
    "auth": "🔐",
    "performance": "⚡",
    "ci": "🤖",
    "build": "🏗️",
}

_DEFAULT_EMOJI = "📦"


def _select_emoji(description: str) -> str:
    """Return the first matching emoji for a description.

    Matching is case‑insensitive and looks for keyword substrings.
    """
    lowered = description.lower()
    for keyword, emoji in _EMOJI_MAP.items():
        if keyword in lowered:
            return emoji
    return _DEFAULT_EMOJI


def emoji_commit_message(description: str) -> str:
    """Return an emoji‑prefixed commit message.

    Parameters
    ----------
    description: str
        Short description of the change.

    Returns
    -------
    str
        Emoji followed by a space and the original description.
    """
    if not description:
        raise ValueError("Description must be a non‑empty string")
    emoji = _select_emoji(description)
    return f"{emoji} {description.strip()}"


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Generate an emoji‑prefixed git commit message"
    )
    parser.add_argument("description", help="Short description of the change")
    args = parser.parse_args()
    try:
        result = emoji_commit_message(args.description)
        print(result)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
