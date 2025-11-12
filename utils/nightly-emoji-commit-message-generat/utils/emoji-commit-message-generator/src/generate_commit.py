"""
emoji_commit_message_generator

Provides a function to generate a git commit message prefixed with an emoji
based on simple keyword matching.
"""

import sys
from typing import Dict

# Simple keyword to emoji mapping.
EMOJI_MAP: Dict[str, str] = {
    "add": "✨",
    "create": "✨",
    "remove": "🗑️",
    "delete": "🗑️",
    "fix": "🐛",
    "bug": "🐛",
    "refactor": "🔧",
    "update": "🔄",
    "upgrade": "⬆️",
    "downgrade": "⬇️",
    "security": "🔐",
    "auth": "🔐",
    "test": "✅",
    "docs": "📝",
    "performance": "⚡",
    "ci": "🤖",
    "merge": "🔀",
}


def _find_emoji(description: str) -> str:
    """Return the first matching emoji for a word in the description."""
    words = description.lower().split()
    for word in words:
        if word in EMOJI_MAP:
            return EMOJI_MAP[word]
    # Default emoji if no keyword matches.
    return "💡"


def generate_commit_message(description: str) -> str:
    """
    Generate a commit message prefixed with an appropriate emoji.

    Parameters
    ----------
    description: str
        Short description of the change.

    Returns
    -------
    str
        Emoji‑prefixed commit message.
    """
    emoji = _find_emoji(description)
    return f"{emoji} {description.strip()}"


def _cli():
    if len(sys.argv) != 2:
        print("Usage: python -m utils.emoji-commit-message-generator.src.generate_commit \"<description>\"")
        sys.exit(1)
    description = sys.argv[1]
    print(generate_commit_message(description))

if __name__ == "__main__":
    _cli()
