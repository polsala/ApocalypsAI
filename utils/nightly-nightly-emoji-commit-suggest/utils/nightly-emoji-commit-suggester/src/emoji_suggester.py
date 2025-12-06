import sys

EMOJI_MAP = {
    "feat": "✨",        # New feature
    "feature": "✨",
    "add": "✨",
    "new": "✨",
    "fix": "🐛",         # Bug fix
    "bug": "🐛",
    "patch": "🐛",
    "docs": "📚",        # Documentation
    "doc": "📚",
    "documentation": "📚",
    "refactor": "♻️",     # Code refactoring
    "revert": "⏪",      # Revert changes
    "test": "🧪",        # Tests
    "tests": "🧪",
    "testing": "🧪",
    "chore": "⚙️",        # Chore, maintenance
    "config": "⚙️",
    "build": "🏗️",        # Build system, CI/CD
    "ci": "🏗️",
    "cd": "🏗️",
    "style": "🎨",       # Code style, formatting
    "format": "🎨",
    "perf": "⚡",        # Performance improvements
    "performance": "⚡",
    "security": "🔒",    # Security
    "dep": "📦",         # Dependency updates
    "deps": "📦",
    "dependency": "📦",
    "remove": "🗑️",      # Remove files or code
    "delete": "🗑️",
    "initial": "🎉",     # Initial commit
    "init": "🎉",
    "release": "🚀",     # Release
    "deploy": "🚀",
    "hotfix": "🚑",     # Hotfix
    "merge": "🔀",      # Merge branches
    "wip": "🚧",         # Work in progress
    "breaking": "💥",    # Breaking changes
    "data": "📊",        # Data related changes
    "db": "🗄️",          # Database related changes
    "ux": "💡",          # UX/UI improvements
    "ui": "💡",
    "accessibility": "♿", # Accessibility
    "a11y": "♿",
}

def suggest_emoji(commit_message: str) -> str:
    """
    Suggests an emoji based on keywords found in the commit message.

    Args:
        commit_message: The full commit message string.

    Returns:
        A relevant emoji string, or an empty string if no keyword is matched.
    """
    message_lower = commit_message.lower()

    # Prioritize exact matches for common prefixes like "feat:", "fix:", etc.
    # This handles cases where "feat" might appear later in the message but
    # "fix" is the actual type.
    for keyword, emoji in EMOJI_MAP.items():
        if message_lower.startswith(f"{keyword}:") or message_lower.startswith(f"{keyword} "):
            return emoji

    # Fallback to checking if any keyword is present anywhere in the message
    for keyword, emoji in EMOJI_MAP.items():
        if keyword in message_lower:
            return emoji
            
    return ""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python emoji_suggester.py \"Your commit message here\"")
        sys.exit(1)

    commit_msg = sys.argv[1]
    emoji = suggest_emoji(commit_msg)
    print(emoji)
