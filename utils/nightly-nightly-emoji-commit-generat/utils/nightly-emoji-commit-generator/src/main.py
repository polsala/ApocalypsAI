import argparse
import sys
from typing import Dict

# Mapping of keywords to emojis
EMOJI_MAP: Dict[str, str] = {
    "fix": "🐛",
    "add": "✨",
    "remove": "🗑️",
    "refactor": "🔧",
    "docs": "📚",
    "test": "✅",
    "perf": "⚡",
    "ci": "🤖",
    "style": "🎨",
    "chore": "🧹",
}


def get_emoji_for_message(message: str) -> str:
    """Return an emoji based on the first matching keyword in *message*.

    The search is case‑insensitive and looks at word boundaries.
    If no keyword matches, the default 🎉 is returned.
    """
    lowered = message.lower()
    words = lowered.split()
    for word in words:
        if word in EMOJI_MAP:
            return EMOJI_MAP[word]
    return "🎉"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Suggest an emoji prefix for a git commit message."
    )
    parser.add_argument(
        "message",
        help="The commit message to analyse.",
    )
    args = parser.parse_args(argv)
    emoji = get_emoji_for_message(args.message)
    print(f"{emoji} {args.message}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
