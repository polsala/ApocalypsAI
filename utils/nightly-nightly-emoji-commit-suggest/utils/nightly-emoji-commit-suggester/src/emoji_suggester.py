import sys
from typing import List, Dict

EMOJI_MAP: Dict[str, str] = {
    "feat": "✨", "feature": "✨", "new": "✨",
    "fix": "🐛", "bug": "🐛", "error": "🐛", "hotfix": "🚑",
    "docs": "📚", "doc": "📚",
    "style": "🎨", "format": "🎨",
    "refactor": "♻️", "clean": "♻️",
    "test": "🧪", "tests": "🧪",
    "chore": "⚙️", "config": "⚙️", "ci": "⚙️",
    "perf": "⚡", "performance": "⚡",
    "security": "🔒", "vulnerability": "🔒",
    "dep": "📦", "dependencies": "📦", "deps": "📦",
    "release": "🚀",
    "merge": "🔀",
    "revert": "⏪",
    "build": "🏗️",
    "remove": "🗑️", "delete": "🗑️",
    "update": "⬆️", "upgrade": "⬆️",
    "downgrade": "⬇️",
    "wip": "🚧",
    "initial": "🎉",
    "breaking": "💥"
}

def suggest_emojis(commit_message: str) -> List[str]:
    """
    Analyzes a commit message and suggests relevant emojis based on keywords.
    """
    message_lower = commit_message.lower()
    suggested = set()

    # Prioritize conventional commit types if they appear at the start
    if message_lower.startswith("feat:") or message_lower.startswith("feature:"):
        suggested.add(EMOJI_MAP["feat"])
    elif message_lower.startswith("fix:"):
        suggested.add(EMOJI_MAP["fix"])
    elif message_lower.startswith("docs:"):
        suggested.add(EMOJI_MAP["docs"])
    elif message_lower.startswith("style:"):
        suggested.add(EMOJI_MAP["style"])
    elif message_lower.startswith("refactor:"):
        suggested.add(EMOJI_MAP["refactor"])
    elif message_lower.startswith("test:"):
        suggested.add(EMOJI_MAP["test"])
    elif message_lower.startswith("chore:"):
        suggested.add(EMOJI_MAP["chore"])
    elif message_lower.startswith("perf:"):
        suggested.add(EMOJI_MAP["perf"])
    elif message_lower.startswith("build:"):
        suggested.add(EMOJI_MAP["build"])
    elif message_lower.startswith("ci:"):
        suggested.add(EMOJI_MAP["ci"])
    elif message_lower.startswith("revert:"):
        suggested.add(EMOJI_MAP["revert"])
    elif message_lower.startswith("security:"):
        suggested.add(EMOJI_MAP["security"])
    elif message_lower.startswith("dep:") or message_lower.startswith("deps:"):
        suggested.add(EMOJI_MAP["dep"])
    elif message_lower.startswith("release:"):
        suggested.add(EMOJI_MAP["release"])
    elif message_lower.startswith("merge:"):
        suggested.add(EMOJI_MAP["merge"])
    elif message_lower.startswith("remove:") or message_lower.startswith("delete:"):
        suggested.add(EMOJI_MAP["remove"])
    elif message_lower.startswith("update:") or message_lower.startswith("upgrade:"):
        suggested.add(EMOJI_MAP["update"])
    elif message_lower.startswith("downgrade:"):
        suggested.add(EMOJI_MAP["downgrade"])
    elif message_lower.startswith("hotfix:"):
        suggested.add(EMOJI_MAP["hotfix"])
    elif message_lower.startswith("wip:"):
        suggested.add(EMOJI_MAP["wip"])
    elif message_lower.startswith("initial:"):
        suggested.add(EMOJI_MAP["initial"])
    elif message_lower.startswith("breaking:"):
        suggested.add(EMOJI_MAP["breaking"])

    # Check for other keywords throughout the message for additional suggestions
    for keyword, emoji in EMOJI_MAP.items():
        # Avoid re-adding if already added by conventional prefix
        if emoji not in suggested and keyword in message_lower:
            suggested.add(emoji)

    # Sort for deterministic output
    return sorted(list(suggested))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/emoji_suggester.py \"<commit message>\"", file=sys.stderr)
        sys.exit(1)

    commit_msg = sys.argv[1]
    emojis = suggest_emojis(commit_msg)
    if emojis:
        print(" ".join(emojis))
