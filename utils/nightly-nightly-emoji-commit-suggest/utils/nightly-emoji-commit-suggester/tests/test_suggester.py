import sys
import io
import pytest
from unittest.mock import patch
from src.suggester import suggest_emojis

# Mock rationale: The utility's core logic is in `suggest_emojis`. 
# We mock `sys.stdin` and `sys.stdout` for testing the command-line interface 
# without actual file I/O or user input, ensuring deterministic and offline tests.

def test_suggest_emojis_feature():
    message = "feat: Add new user authentication module"
    expected = ["✨"]
    assert suggest_emojis(message) == expected

def test_suggest_emojis_fix_and_docs():
    message = "fix(auth): Resolve critical bug in payment processing and update docs"
    expected = ["📚", "🐛"]
    assert suggest_emojis(message) == expected

def test_suggest_emojis_chore_and_config():
    message = "chore: Update build config for CI pipeline"
    expected = ["⚙️", "🚀"]
    assert suggest_emojis(message) == expected

def test_suggest_emojis_refactor_and_perf():
    message = "refactor: Rework database queries for performance improvement"
    expected = ["⚡", "♻️"]
    assert suggest_emojis(message) == expected

def test_suggest_emojis_no_match():
    message = "Initial commit of the project structure"
    expected = []
    assert suggest_emojis(message) == expected

def test_suggest_emojis_case_insensitivity():
    message = "FeAt: Implement new API endpoint"
    expected = ["✨"]
    assert suggest_emojis(message) == expected

def test_suggest_emojis_multiple_keywords_same_emoji():
    message = "add new feature"
    expected = ["✨"]
    assert suggest_emojis(message) == expected

def test_suggest_emojis_mixed_case_keywords():
    message = "Fix: a bug, and Add: a feature"
    expected = ["✨", "🐛"]
    assert suggest_emojis(message) == expected

def test_suggest_emojis_with_init():
    message = "init: Initial project setup"
    expected = ["🎉"]
    assert suggest_emojis(message) == expected

def test_suggest_emojis_with_remove():
    message = "remove: old unused files"
    expected = ["🗑️"]
    assert suggest_emojis(message) == expected

def test_suggest_emojis_with_update_and_upgrade():
    message = "update: dependencies and upgrade framework"
    expected = ["⬆️", "📦"]
    assert suggest_emojis(message) == expected

def test_suggest_emojis_with_hotfix():
    message = "hotfix: critical production issue"
    expected = ["🚑"]
    assert suggest_emojis(message) == expected

def test_suggest_emojis_with_breaking():
    message = "feat!: breaking change for API"
    expected = ["💥", "✨"]
    assert suggest_emojis(message) == expected

def test_suggest_emojis_with_wip():
    message = "wip: working on new feature"
    expected = ["🚧", "✨"]
    assert suggest_emojis(message) == expected

# --- CLI Tests ---

@patch('sys.stdout', new_callable=io.StringIO)
@patch('sys.stdin', new_callable=io.StringIO)
def test_cli_from_stdin(mock_stdin, mock_stdout):
    # Mock rationale: Simulate user piping input to the script.
    mock_stdin.write("feat: Implement user profiles")
    mock_stdin.seek(0) # Rewind the mock stdin to the beginning

    # Import the main script to trigger its execution
    # We need to clear sys.argv to prevent argparse from trying to parse pytest arguments
    original_argv = sys.argv
    sys.argv = ['src/suggester.py']
    try:
        import src.suggester
        # Reload the module to re-run the `if __name__ == "__main__":` block
        # This is a common pattern for testing CLI scripts that don't have a main() function to call directly
        import importlib
        importlib.reload(src.suggester)
    finally:
        sys.argv = original_argv # Restore sys.argv

    output = mock_stdout.getvalue().strip().split('\n')
    assert sorted(output) == sorted(["✨"])

@patch('sys.stdout', new_callable=io.StringIO)
def test_cli_from_argument(mock_stdout):
    # Mock rationale: Simulate user passing an argument to the script.
    original_argv = sys.argv
    sys.argv = ['src/suggester.py', 'fix: Correct typo in README']
    try:
        import src.suggester
        import importlib
        importlib.reload(src.suggester)
    finally:
        sys.argv = original_argv

    output = mock_stdout.getvalue().strip().split('\n')
    assert sorted(output) == sorted(["🐛"])

@patch('sys.stdout', new_callable=io.StringIO)
def test_cli_no_match_from_argument(mock_stdout):
    # Mock rationale: Simulate a commit message with no matching keywords.
    original_argv = sys.argv
    sys.argv = ['src/suggester.py', 'random message without keywords']
    try:
        import src.suggester
        import importlib
        importlib.reload(src.suggester)
    finally:
        sys.argv = original_argv

    output = mock_stdout.getvalue().strip()
    assert output == ""

@patch('sys.stdout', new_callable=io.StringIO)
@patch('sys.stdin', new_callable=io.StringIO)
def test_cli_empty_input(mock_stdin, mock_stdout):
    # Mock rationale: Simulate empty input from stdin or argument.
    mock_stdin.write("")
    mock_stdin.seek(0)

    original_argv = sys.argv
    sys.argv = ['src/suggester.py'] # No argument, so it will read from stdin
    try:
        import src.suggester
        import importlib
        importlib.reload(src.suggester)
    finally:
        sys.argv = original_argv

    output = mock_stdout.getvalue().strip()
    assert output == ""
