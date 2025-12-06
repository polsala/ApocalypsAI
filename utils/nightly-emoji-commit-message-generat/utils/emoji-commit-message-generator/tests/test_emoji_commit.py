import pytest

# Mock rationale: tests are pure unit tests, no external I/O.
from src.emoji_commit import emoji_commit_message

@pytest.mark.parametrize(
    "description,expected",
    [
        ("Add new login endpoint", "✨ Add new login endpoint"),
        ("Fix typo in README", "🐛 Fix typo in README"),
        ("Update documentation for API", "📝 Update documentation for API"),
        ("Improve performance of query", "⚡ Improve performance of query"),
        ("Merge feature branch", "🔀 Merge feature branch"),
        ("Random change with no keyword", "📦 Random change with no keyword"),
    ],
)
def test_emoji_commit_message(description, expected):
    assert emoji_commit_message(description) == expected

def test_empty_description_raises():
    with pytest.raises(ValueError):
        emoji_commit_message("")
