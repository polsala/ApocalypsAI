"""emoji_commit.py

Utility to prepend an appropriate emoji to a git commit message based on simple keyword heuristics.

The mapping is deliberately small and deterministic, making the tool fast and offline.
"""

import sys
from typing import Dict, List

# Simple keyword‑to‑emoji mapping. Order matters – first match wins.
KEYWORD_EMOJI_MAP: List[Dict[str, str]] = [
    {"keywords": ["fix", "bug", "patch"], "emoji": "🐛"},
    {"keywords": ["add", "feature", "implement"], "emoji": "✨"},
    {"keywords": ["remove", "delete", "rm"], "emoji": "🗑️"},
    {"keywords": ["refactor", "restructure"], "emoji": "🔧"},
    {"keywords": ["docs", "documentation", "readme"], "emoji": "📚"},
    {"keywords": ["test", "tests", "coverage"], "emoji": "✅"},
    {"keywords": ["ci", "pipeline", "github actions"], "emoji": "🤖"},
    {"keywords": ["performance", "speed", "optimize"], "emoji": "⚡"},
]

DEFAULT_EMOJI = "📝"


def _find_emoji(message: str) -> str:
    """Return the first matching emoji for *message* or the default.

    Matching is case‑insensitive and looks for any keyword as a whole word.
    """
    lowered = message.lower()
    for entry in KEYWORD_EMOJI_MAP:
        for kw in entry["keywords"]:
            if f"{kw}" in lowered:
                return entry["emoji"]
    return DEFAULT_EMOJI


def enhance_message(message: str) -> str:
    """Prepend an emoji to *message* if it does not already start with one.

    Parameters
    ----------
    message: str
        The original commit message.

    Returns
    -------
    str
        The enhanced commit message.
    """
    stripped = message.lstrip()
    if stripped and stripped[0] in {"🐛", "✨", "🗑️", "🔧", "📚", "✅", "🤖", "⚡", "📝"}:
        # Already has an emoji – leave untouched.
        return message.rstrip()
    emoji = _find_emoji(message)
    return f"{emoji} {message.strip()}"


def main(argv: List[str] | None = None) -> int:
    """CLI entry point.

    Usage: ``python -m src.emoji_commit "Your commit message"``
    """
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Error: No commit message provided.", file=sys.stderr)
        return 1
    original = " ".join(argv)
    enhanced = enhance_message(original)
    print(enhanced)
    return 0


if __name__ == "__main__":
    sys.exit(main())
