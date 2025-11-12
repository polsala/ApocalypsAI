import builtins
import io
import sys
from utils.emoji_mood_analyzer.src.analyzer import analyze_mood, main

# Mock rationale: No external services are called; we only need to ensure deterministic behavior.

def test_analyze_happy():
    assert analyze_mood("I love this awesome project!") == "😊"
    assert analyze_mood("Feeling great today") == "😊"

def test_analyze_sad():
    assert analyze_mood("I am so sad and upset") == "😢"
    assert analyze_mood("What a terrible day") == "😢"

def test_analyze_angry():
    assert analyze_mood("I'm angry about the bug") == "😠"
    assert analyze_mood("She is mad at the delay") == "😠"

def test_analyze_neutral():
    assert analyze_mood("Just a regular update") == "🤔"
    assert analyze_mood("No mood keywords here") == "🤔"

def test_cli_with_argument(monkeypatch, capsys):
    # Simulate passing the text as a CLI argument
    monkeypatch.setattr(sys, "argv", ["analyzer.py", "I love it!"])
    exit_code = main()
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "😊"

def test_cli_with_stdin(monkeypatch, capsys):
    # Simulate reading from stdin
    fake_stdin = io.StringIO("I am sad.")
    monkeypatch.setattr(sys, "stdin", fake_stdin)
    monkeypatch.setattr(sys, "argv", ["analyzer.py"])
    exit_code = main()
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "😢"
