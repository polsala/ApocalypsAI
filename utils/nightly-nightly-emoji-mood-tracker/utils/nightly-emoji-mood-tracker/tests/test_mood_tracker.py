import builtins
import sys
from types import SimpleNamespace

# Mock rationale: No external resources are accessed; we only need to import the module.
# The import itself is deterministic, so no additional mocking is required.

from src.mood_tracker import mood_to_emoji, normalize_mood


def test_normalize_mood():
    assert normalize_mood(" Happy ") == "happy"
    assert normalize_mood("Feeling Excited") == "feeling_excited"
    assert normalize_mood("  FRUSTRATED  ") == "frustrated"


def test_exact_matches():
    assert mood_to_emoji("happy") == "😄"
    assert mood_to_emoji("Sad") == "😢"
    assert mood_to_emoji("  excited  ") == "🤩"


def test_substring_fallback():
    # "super happy" contains "happy"
    assert mood_to_emoji("super happy") == "😄"
    # "I am very frustrated today" contains "frustrated"
    assert mood_to_emoji("I am very frustrated today") == "😤"


def test_unknown_mood_returns_shrug():
    assert mood_to_emoji("quantum bliss") == "🤷"

# CLI integration test – capture stdout
def test_cli_output(monkeypatch, capsys):
    # Simulate command‑line arguments
    monkeypatch.setattr(sys, "argv", ["mood_tracker.py", "celebrate"])
    # Import the module as a script to trigger __main__ block
    import importlib
    import src.mood_tracker as mt
    importlib.reload(mt)
    captured = capsys.readouterr()
    assert captured.out.strip() == "🎉"
