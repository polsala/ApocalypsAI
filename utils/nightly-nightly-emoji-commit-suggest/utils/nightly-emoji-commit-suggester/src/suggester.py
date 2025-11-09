import sys
import argparse
from typing import List, Dict

EMOJI_MAP: Dict[str, str] = {
    "feat": "✨",       # New feature
    "feature": "✨",    # New feature
    "add": "✨",        # Add something new
    "fix": "🐛",        # Bug fix
    "bug": "🐛",        # Bug fix
    "docs": "📚",       # Documentation
    "doc": "📚",        # Documentation
    "refactor": "♻️",    # Code refactoring
    "rework": "♻️",     # Code refactoring
    "test": "🧪",       # Adding or modifying tests
    "tests": "🧪",      # Adding or modifying tests
    "chore": "⚙️",       # Chores, maintenance, build process
    "config": "⚙️",     # Configuration changes
    "style": "🎨",      # Code style, formatting
    "format": "🎨",     # Code style, formatting
    "perf": "⚡",       # Performance improvements
    "performance": "⚡",# Performance improvements
    "security": "🔒",   # Security fixes/improvements
    "ci": "🚀",         # CI/CD related changes
    "workflow": "🚀",   # Workflow related changes
    "dep": "📦",        # Dependency updates
    "deps": "📦",       # Dependency updates
    "dependency": "📦", # Dependency updates
    "release": "🔖",    # Release new version
    "merge": "🔀",      # Merge branches
    "revert": "⏪",     # Revert previous changes
    "remove": "🗑️",     # Remove code or files
    "delete": "🗑️",     # Delete code or files
    "update": "⬆️",     # Update dependencies or features
    "upgrade": "⬆️",    # Upgrade dependencies or features
    "downgrade": "⬇️",   # Downgrade dependencies
    "hotfix": "🚑",      # Critical hotfix
    "breaking": "💥",   # Introducing breaking changes
    "init": "🎉",       # Initial commit
    "initial": "🎉",    # Initial commit
    "wip": "🚧",        # Work in progress
    "draft": "🚧",      # Draft commit
}

def suggest_emojis(commit_message: str) -> List[str]:
    """
    Suggests relevant emojis based on keywords in the commit message.
    """
    message_lower = commit_message.lower()
    suggested = set()

    for keyword, emoji in EMOJI_MAP.items():
        if keyword in message_lower:
            suggested.add(emoji)

    # Sort for deterministic output, useful for testing and consistent display
    return sorted(list(suggested))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Suggests relevant emojis for a commit message."
    )
    parser.add_argument(
        "message",
        nargs="?",
        help="The commit message to analyze. If not provided, reads from stdin."
    )
    args = parser.parse_args()

    if args.message:
        commit_msg = args.message
    else:
        # Read from stdin if no argument is provided
        commit_msg = sys.stdin.read().strip()

    if commit_msg:
        emojis = suggest_emojis(commit_msg)
        for emoji in emojis:
            print(emoji)
    else:
        # If no message is provided via arg or stdin, print nothing and exit gracefully
        sys.exit(0)
