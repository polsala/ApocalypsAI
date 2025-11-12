import sys
from pathlib import Path

# Mock rationale: Import the module from the relative src directory without installing the package.
# This keeps the test deterministic and offline.
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from emoji_commit import select_emoji, format_commit

def test_select_emoji_known_keywords():
    assert select_emoji("Fix the login bug") == "🐛"
    assert select_emoji("Add new endpoint") == "➕"
    assert select_emoji("Remove deprecated flag") == "➖"
    assert select_emoji("Update docs for API") == "📚"
    assert select_emoji("Refactor authentication flow") == "♻️"
    assert select_emoji("Write tests for utils") == "✅"
    assert select_emoji("CI: update workflow") == "⚙️"

def test_select_emoji_fallback():
    # No known keyword – should return the default sparkle emoji.
    assert select_emoji("Improve performance of cache") == "✨"

def test_format_commit_preserves_message_and_emoji():
    msg = "Add user profile page"
    formatted = format_commit(msg)
    assert formatted.startswith("➕ ")
    assert formatted == "➕ Add user profile page"

def test_format_commit_strips_whitespace():
    msg = "   fix typo in README   "
    formatted = format_commit(msg)
    assert formatted == "🐛 fix typo in README"
