import sys
import re

# Define emojis as constants for easier reference and testing
EMOJI_SPARKLES = "✨"
EMOJI_BUG = "🐛"
EMOJI_BOOKS = "📚"
EMOJI_ART = "🎨"
EMOJI_RECYCLE = "♻️"
EMOJI_LIGHTNING = "⚡"
EMOJI_TEST_TUBE = "🧪"
EMOJI_ROCKET = "🚀"
EMOJI_BROOM = "🧹"
EMOJI_LOCK = "🔒"
EMOJI_PACKAGE = "📦"
EMOJI_REWIND = "⏪"
EMOJI_PARTY_POPPER = "🎉"

EMOJI_MAP = {
    r"\bfeat\b": EMOJI_SPARKLES,        # New feature
    r"\bfeature\b": EMOJI_SPARKLES,     # New feature
    r"\badd\b": EMOJI_SPARKLES,         # New feature (e.g., "add new feature")
    r"\bfix\b": EMOJI_BUG,             # Bug fix
    r"\bbug\b": EMOJI_BUG,             # Bug fix
    r"\berror\b": EMOJI_BUG,           # Error fix
    r"\bdocs\b": EMOJI_BOOKS,          # Documentation
    r"\bdocumentation\b": EMOJI_BOOKS, # Documentation
    r"\bstyle\b": EMOJI_ART,           # Code style, formatting
    r"\bformat\b": EMOJI_ART,          # Code style, formatting
    r"\brefactor\b": EMOJI_RECYCLE,    # Code refactoring
    r"\brestructure\b": EMOJI_RECYCLE, # Code refactoring
    r"\bperf\b": EMOJI_LIGHTNING,        # Performance improvement
    r"\bperformance\b": EMOJI_LIGHTNING, # Performance improvement
    r"\btest\b": EMOJI_TEST_TUBE,        # Adding tests
    r"\btests\b": EMOJI_TEST_TUBE,       # Adding tests
    r"\bbuild\b": EMOJI_ROCKET,         # Build system, CI/CD
    r"\bci\b": EMOJI_ROCKET,           # Build system, CI/CD
    r"\bworkflow\b": EMOJI_ROCKET,     # Build system, CI/CD
    r"\bchore\b": EMOJI_BROOM,         # Chores, maintenance
    r"\bmisc\b": EMOJI_BROOM,          # Miscellaneous tasks
    r"\bsecurity\b": EMOJI_LOCK,       # Security fixes
    r"\bdep\b": EMOJI_PACKAGE,         # Dependency updates
    r"\bdependencies\b": EMOJI_PACKAGE,# Dependency updates
    r"\brevert\b": EMOJI_REWIND,       # Reverting changes
    r"\binitial commit\b": EMOJI_PARTY_POPPER # Initial commit (full phrase)
}

def suggest_emoji(commit_message: str) -> list[str]:
    """
    Suggests relevant emojis for a given commit message based on keywords.
    Keywords are matched case-insensitively using whole word regex matching.
    """
    message_lower = commit_message.lower()
    suggested = set()

    for keyword_pattern, emoji in EMOJI_MAP.items():
        # Use re.search for pattern matching
        if re.search(keyword_pattern, message_lower):
            suggested.add(emoji)

    # Sort for deterministic output
    return sorted(list(suggested))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python emoji_suggester.py \"<commit message>\"")
        sys.exit(1)

    commit_msg = sys.argv[1]
    emojis = suggest_emoji(commit_msg)
    if emojis:
        print(" ".join(emojis))
