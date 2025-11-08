import argparse
import sys
from typing import Dict

# Mapping of keywords to emojis
KEYWORD_EMOJI_MAP: Dict[str, str] = {
    "fix": "🐛",
    "bug": "🐛",
    "add": "✨",
    "feature": "🚀",
    "remove": "🗑️",
    "delete": "🗑️",
    "docs": "📚",
    "doc": "📚",
    "refactor": "🔧",
    "test": "✅",
    "performance": "⚡",
    "security": "🔒",
}

DEFAULT_EMOJI = "🎉"

def _select_emoji(message: str) -> str:
    """Return the first matching emoji based on keyword presence.

    The search is case‑insensitive and looks for whole‑word matches.
    """
    lowered = message.lower()
    for keyword, emoji in KEYWORD_EMOJI_MAP.items():
        if f"{keyword}" in lowered:
            return emoji
    return DEFAULT_EMOJI

def enhance_message(message: str) -> str:
    """Prepend an appropriate emoji to *message*.

    If the message already starts with an emoji (detected via Unicode range), it is returned unchanged.
    """
    if not message:
        return message
    first_char = message[0]
    if "\U0001F300" <= first_char <= "\U0001FAFF":
        # Already starts with an emoji
        return message
    emoji = _select_emoji(message)
    return f"{emoji} {message}"

def _parse_args(argv):
    parser = argparse.ArgumentParser(description="Enhance a git commit message with an emoji.")
    parser.add_argument("message", help="The original commit message (enclose in quotes if it contains spaces).")
    return parser.parse_args(argv)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = _parse_args(argv)
    enhanced = enhance_message(args.message)
    print(enhanced)

if __name__ == "__main__":
    main()
