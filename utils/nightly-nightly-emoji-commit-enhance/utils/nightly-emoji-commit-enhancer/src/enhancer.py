import sys
import random
import re
from typing import List

TYPE_EMOJI_MAP = {
    "feat": ["🚀", "✨", "🆕"],
    "fix": ["🐛", "🔧", "🩹"],
    "docs": ["📚", "📝"],
    "style": ["💄", "🎨"],
    "refactor": ["♻️", "🔄"],
    "test": ["✅", "🧪"],
    "chore": ["🧹", "🔧"],
}

DEFAULT_EMOJIS = ["✨", "🔧", "🛠️"]


def choose_emoji(commit_type: str) -> str:
    """Return a random emoji appropriate for *commit_type*.

    # Mock rationale: deterministic selection is handled in tests via patching.
    """
    emojis: List[str] = TYPE_EMOJI_MAP.get(commit_type.lower(), DEFAULT_EMOJIS)
    return random.choice(emojis)


def enhance_message(message: str) -> str:
    """Append an appropriate emoji to a conventional commit message.

    The function looks for a leading `<type>` (optionally with a scope) followed by a colon.
    If no type is found, the *default* emoji list is used.
    """
    match = re.match(r"^(?P<type>\w+)(\(.+\))?:", message.strip())
    commit_type = match.group("type") if match else ""
    emoji = choose_emoji(commit_type)
    return f"{message.rstrip()} {emoji}"


def main(argv: List[str] = None) -> int:
    argv = argv or sys.argv[1:]
    if not argv:
        # Read from stdin when no arguments are supplied.
        message = sys.stdin.read().strip()
    else:
        message = " ".join(argv).strip()
    if not message:
        print("No commit message provided.", file=sys.stderr)
        return 1
    enhanced = enhance_message(message)
    print(enhanced)
    return 0


if __name__ == "__main__":
    sys.exit(main())
