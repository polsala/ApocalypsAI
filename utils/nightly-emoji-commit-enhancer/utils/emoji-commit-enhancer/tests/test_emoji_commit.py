import builtins
import sys
from src import emoji_commit

# Mock rationale: we avoid any external I/O; all tests are pure function calls.

def test_enhance_message_adds_correct_emoji():
    assert emoji_commit.enhance_message("Fix bug in parser") == "🐛 Fix bug in parser"
    assert emoji_commit.enhance_message("Add new authentication feature") == "✨ Add new authentication feature"
    assert emoji_commit.enhance_message("Update README documentation") == "📚 Update README documentation"
    assert emoji_commit.enhance_message("Refactor module layout") == "🔧 Refactor module layout"
    assert emoji_commit.enhance_message("Improve performance of query engine") == "⚡ Improve performance of query engine"
    # No keyword match falls back to default emoji
    assert emoji_commit.enhance_message("Miscellaneous tweaks") == "📝 Miscellaneous tweaks"

def test_enhance_message_preserves_existing_emoji():
    # If the message already starts with a known emoji, it should be left untouched.
    assert emoji_commit.enhance_message("🐛 Already has bug emoji") == "🐛 Already has bug emoji"
    assert emoji_commit.enhance_message("   ✨ Leading spaces with emoji") == "   ✨ Leading spaces with emoji"

def test_cli_success(monkeypatch, capsys):
    # Mock sys.argv for CLI invocation
    monkeypatch.setattr(sys, "argv", ["emoji_commit.py", "Add unit tests"])
    exit_code = emoji_commit.main()
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "✨ Add unit tests"

def test_cli_no_arguments(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["emoji_commit.py"])
    exit_code = emoji_commit.main()
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error: No commit message provided" in captured.err
