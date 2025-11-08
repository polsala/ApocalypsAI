"""emoji_commit.py

Utility to generate an emoji‑prefixed commit message based on supplied keywords.

The mapping is deliberately simple and deterministic – perfect for a lightweight
CLI tool that adds a dash of personality to your Git history.
"""

from __future__ import annotations

import argparse
import sys
from typing import List, Dict

# Simple keyword → emoji mapping. Extend as needed.
EMOJI_MAP: Dict[str, str] = {
    "fix": "🐛",
    "bug": "🐛",
    "add": "✨",
    "feature": "✨",
    "refactor": "♻️",
    "remove": "🗑️",
    "docs": "📝",
    "test": "✅",
    "performance": "⚡",
    "security": "🔒",
}

def _pick_emoji(keywords: List[str]) -> str:
    """Return the first matching emoji for the given keywords.

    If none match, a default "🔧" (tool) emoji is used.
    """
    for word in keywords:
        lowered = word.lower()
        if lowered in EMOJI_MAP:
            return EMOJI_MAP[lowered]
    return "🔧"

def generate_message(keywords: List[str]) -> str:
    """Generate a commit message with an emoji prefix.

    Parameters
    ----------
    keywords: List[str]
        List of words describing the change (e.g., ["fix", "login"]).

    Returns
    -------
    str
        Emoji‑prefixed commit message.
    """
    if not keywords:
        raise ValueError("At least one keyword must be provided")
    emoji = _pick_emoji(keywords)
    # Join the original keywords preserving order for readability.
    message_body = " ".join(keywords)
    return f"{emoji} {message_body}"

def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="emoji-commit",
        description="Generate an emoji‑prefixed git commit message.",
    )
    parser.add_argument(
        "keywords",
        nargs="+",
        help="Words describing the change (e.g., fix bug)",
    )
    return parser.parse_args(argv)

def main() -> None:
    args = _parse_args()
    try:
        result = generate_message(args.keywords)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
