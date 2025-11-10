import sys
from pathlib import Path

# Ensure the src directory is importable
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src"))

from emoji_commit_helper import suggest_emoji


def test_emoji_feature():
    msg = "Add new authentication flow"
    assert suggest_emoji(msg) == "🚀 Add new authentication flow"


def test_emoji_bugfix():
    msg = "Fix typo in README"
    assert suggest_emoji(msg) == "🐛 Fix typo in README"


def test_emoji_docs():
    msg = "Update documentation for API endpoints"
    assert suggest_emoji(msg) == "📚 Update documentation for API endpoints"


def test_emoji_refactor():
    msg = "Refactor user service module"
    assert suggest_emoji(msg) == "🛠️ Refactor user service module"


def test_emoji_test():
    msg = "Add tests for payment processor"
    assert suggest_emoji(msg) == "✅ Add tests for payment processor"


def test_emoji_default():
    msg = "Improve performance of cache layer"
    # No explicit keyword matches; falls back to default.
    assert suggest_emoji(msg) == "✨ Improve performance of cache layer"

# Mock rationale comments (no external calls are made in this utility)
# Mock rationale: The utility is deterministic and offline; tests rely solely on pure functions.
