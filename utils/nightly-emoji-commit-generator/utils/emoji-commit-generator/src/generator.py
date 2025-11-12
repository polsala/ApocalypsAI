import sys
from typing import Dict

# Mapping of keywords to emojis. Order matters – first match wins.
EMOJI_MAP: Dict[str, str] = {
    "add": "✨",
    "fix": "🐛",
    "remove": "🗑️",
    "update": "🔄",
    "refactor": "🛠️",
    "docs": "📚",
    "test": "✅",
    "ci": "🤖",
    "performance": "⚡",
    "security": "🔒",
}


def add_emoji(message: str) -> str:
    """Return *message* prefixed with the first matching emoji.

    The function performs a case‑insensitive search for each keyword in the
    order defined in ``EMOJI_MAP``. If a keyword is found, its emoji is prepended
    to the original message separated by a space. If no keyword matches, the
    original message is returned unchanged.
    """
    lowered = message.lower()
    for keyword, emoji in EMOJI_MAP.items():
        if keyword in lowered:
            return f"{emoji} {message}"
    return message


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m src.generator \"<commit message>\"")
        sys.exit(1)
    msg = sys.argv[1]
    print(add_emoji(msg))


if __name__ == "__main__":
    main()
