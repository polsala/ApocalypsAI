"""Utility to prepend an emoji to a PR title based on conventional‑commit prefixes.

The mapping is:

- feat:   🚀
- fix:    🐛
- docs:   📚
- style:  🎨
- refactor: 🔧
- test:   🧪
- none:   ❓

The function is deterministic and has no external dependencies.
"""

import sys
import re

# Mapping of lower‑case prefixes to emojis
PREFIX_EMOJI_MAP = {
    "feat:": "🚀",
    "fix:": "🐛",
    "docs:": "📚",
    "style:": "🎨",
    "refactor:": "🔧",
    "test:": "🧪",
}

DEFAULT_EMOJI = "❓"


def add_emoji(title: str) -> str:
    """Return *title* with an appropriate emoji prepended.

    The function is case‑insensitive and ignores leading/trailing whitespace.
    If the title starts with a known prefix, the corresponding emoji is used;
    otherwise the default ❓ emoji is added.
    """
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    stripped = title.strip()
    # Extract the first word (prefix) if it ends with a colon
    match = re.match(r"^(\S+):", stripped)
    if match:
        prefix = match.group(1).lower() + ":"
        emoji = PREFIX_EMOJI_MAP.get(prefix, DEFAULT_EMOJI)
    else:
        emoji = DEFAULT_EMOJI
    return f"{emoji} {stripped}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m emoji_adder <PR title>")
        sys.exit(1)
    title = " ".join(sys.argv[1:])
    print(add_emoji(title))
