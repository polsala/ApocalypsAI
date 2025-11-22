# test_mood_analyzer.py
# Deterministic unit tests for the mood analyzer utility.
# No external resources are accessed; all data is in‑memory.

import builtins
import sys
from pathlib import Path

# Ensure the src directory is importable
utils_path = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(utils_path))

from mood_analyzer import analyze_mood

def test_happy_sentence():
    text = "I love sunny days and feel fantastic!"
    assert analyze_mood(text) == "😊"

def test_sad_sentence():
    text = "It was a gloomy, rainy afternoon and I felt very sad."
    assert analyze_mood(text) == "😢"

def test_angry_sentence():
    text = "I am furious and annoyed by this terrible bug."
    assert analyze_mood(text) == "😠"

def test_neutral_when_no_keywords():
    text = "The cat sits on the mat."
    assert analyze_mood(text) == "🤔"

def test_tie_results_in_neutral():
    # Contains one positive and one negative word – tie.
    text = "I love but also feel sad about the news."
    assert analyze_mood(text) == "🤔"

def test_cli_output(capsys):
    # Mock sys.argv for CLI execution
    original_argv = sys.argv
    sys.argv = ["mood_analyzer.py", "I am happy"]
    try:
        # Import the module as a script to trigger __main__
        builtins.__import__("mood_analyzer")
    finally:
        sys.argv = original_argv
    captured = capsys.readouterr()
    assert captured.out.strip() == "😊"
