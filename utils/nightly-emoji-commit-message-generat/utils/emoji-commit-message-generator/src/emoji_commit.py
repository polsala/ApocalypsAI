"""emoji_commit.py

Utility to generate an emoji‑prefixed commit message from a short description.

The implementation is deliberately lightweight and offline – it uses a static
mapping of keywords to emojis. This makes the utility deterministic and safe for
use in the ApocalypsAI self‑healing workflow.
"""

from __future__ import annotations

import argparse
import sys
from typing import Dict

# Mock rationale: a static, deterministic mapping ensures offline operation and
# reproducible test results.
_EMOJI_MAP: Dict[str, str] = {
    "fix": "🛠️",
    "bug": "🐛",
    "add": "✨",
    "remove": "🗑️",
    "refactor": "🔧",
    "docs": "📚",
    "test": "✅",
    "performance": "⚡",
    "security": "🔒",
    "ci": "🤖",
}

_DEFAULT_EMOJI = "📦"


def _find_emoji(description: str) -> str:
    """Return the first matching emoji for a keyword in *description*.

    The search is case‑insensitive and looks for whole‑word matches.
    """
    words = description.lower().split()
    for word in words:
        if word in _EMOJI_MAP:
            return _EMOJI_MAP[word]
    return _DEFAULT_EMOJI


def generate_commit_message(description: str) -> str:
    """Generate an emoji‑prefixed commit message.

    Parameters
    ----------
    description: str
        Short, human‑readable description of the change.

    Returns
    -------
    str
        Emoji followed by a space and the original description.
    """
    if not description:
        raise ValueError("Description must be a non‑empty string")
    emoji = _find_emoji(description)
    return f"{emoji} {description.strip()}"


def _cli() -> None:
    parser = argparse.ArgumentParser(
        prog="emoji_commit",
        description="Generate an emoji‑prefixed commit message from a description.",
    )
    parser.add_argument("description", help="Short commit description")
    args = parser.parse_args()
    try:
        result = generate_commit_message(args.description)
        print(result)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _cli()
