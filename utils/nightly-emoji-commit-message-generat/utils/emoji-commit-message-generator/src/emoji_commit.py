import argparse
import sys
from typing import Dict

# Mapping of keywords to emojis
EMOJI_MAP: Dict[str, str] = {
    "fix": "🐛",
    "bug": "🐛",
    "add": "➕",
    "create": "➕",
    "remove": "➖",
    "delete": "➖",
    "docs": "📚",
    "doc": "📚",
    "refactor": "♻️",
    "test": "✅",
    "tests": "✅",
    "ci": "⚙️",
    "chore": "⚙️",
}

DEFAULT_EMOJI = "✨"

def select_emoji(message: str) -> str:
    """Return the first matching emoji for a given commit message.

    The function lower‑cases the message and looks for any keyword present in
    ``EMOJI_MAP``. If none are found, ``DEFAULT_EMOJI`` is returned.
    """
    lowered = message.lower()
    for keyword, emoji in EMOJI_MAP.items():
        if keyword in lowered:
            return emoji
    return DEFAULT_EMOJI

def format_commit(message: str) -> str:
    """Return the commit message prefixed with the selected emoji."""
    emoji = select_emoji(message)
    return f"{emoji} {message.strip()}"

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="emoji-commit",
        description="Generate a commit message prefixed with an appropriate emoji.",
    )
    parser.add_argument("message", nargs="+", help="Commit description (will be joined with spaces)")
    args = parser.parse_args(argv)
    raw_message = " ".join(args.message)
    formatted = format_commit(raw_message)
    print(formatted)
    return 0

if __name__ == "__main__":
    sys.exit(main())
