import sys
import re

def suggest_emojis(diff_content: str) -> list[str]:
    """
    Analyzes Git diff content and suggests relevant emojis for a commit message.
    """
    emoji_map = {
        # Features and Additions
        r'^(?:\+\+\+ b/|\+).*?(?:feat|feature|add|new|implement|initial|create)': '✨', # Sparkles for new features
        r'^(?:\+\+\+ b/|\+).*?(?:init|setup|config|env)': '⚙️', # Gear for initial setup/config
        r'^(?:\+\+\+ b/|\+).*?(?:deps|dependency|package)': '📦', # Package for dependencies

        # Fixes and Bugs
        r'^(?:\+\+\+ b/|\+).*?(?:fix|bug|error|issue|resolve|patch)': '🐛', # Bug for fixes
        r'^(?:\+\+\+ b/|\+).*?(?:security|vulnerability)': '🔒', # Lock for security

        # Documentation
        r'^(?:\+\+\+ b/|\+).*?(?:doc|docs|documentation|readme|wiki)': '📚', # Books for documentation

        # Refactoring and Code Structure
        r'^(?:\+\+\+ b/|\+).*?(?:refactor|restructure|rename|move|extract|simplify)': '♻️', # Recycle for refactoring
        r'^(?:\+\+\+ b/|\+).*?(?:style|format|lint)': '🎨', # Art for styling

        # Performance
        r'^(?:\+\+\+ b/|\+).*?(?:perf|performance|speed|optimize)': '⚡', # High voltage for performance

        # Tests
        r'^(?:\+\+\+ b/|\+).*?(?:test|tests|testing|spec|e2e|unit|integration)': '🧪', # Test tube for tests

        # Build and CI
        r'^(?:\+\+\+ b/|\+).*?(?:build|ci|workflow|pipeline|docker|compose)': '🏗️', # Building for build/CI

        # Chores and Maintenance
        r'^(?:\+\+\+ b/|\+).*?(?:chore|clean|cleanup|remove|delete|update|upgrade|maintenance)': '🧹', # Broom for chores
        r'^(?:\-\-\- a/|\-).*?(?:remove|delete|deprecate)': '🗑️', # Wastebasket for removal

        # UI/UX
        r'^(?:\+\+\+ b/|\+).*?(?:ui|ux|design|interface|layout)': '🖼️', # Picture frame for UI/UX
    }

    suggested_emojis = set()
    lines = diff_content.splitlines()

    for line in lines:
        # Only consider added/modified lines for suggestions, or removed lines for deletion emoji
        if line.startswith('+') or line.startswith('-'):
            for pattern, emoji in emoji_map.items():
                if re.search(pattern, line, re.IGNORECASE):
                    suggested_emojis.add(emoji)

    # Default emoji if nothing specific is found, but changes exist
    if not suggested_emojis and diff_content.strip():
        suggested_emojis.add('📝') # Memo for general changes

    return sorted(list(suggested_emojis))

def main():
    """
    Main function to read diff from stdin, suggest emojis, and print to stdout.
    """
    diff_input = sys.stdin.read()
    emojis = suggest_emojis(diff_input)
    print(' '.join(emojis))

if __name__ == '__main__':
    main()
