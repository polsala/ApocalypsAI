import builtins
import types
from typing import Any

# Import the module under test
from utils.nightly-emoji-mood-analyzer.src import emoji_mood_analyzer

def test_analyze_mood_happy():
    text = "I love this! 😄😊"
    assert emoji_mood_analyzer.analyze_mood(text) == "happy"

def test_analyze_mood_sad():
    text = "Feeling down 😢😞"
    assert emoji_mood_analyzer.analyze_mood(text) == "sad"

def test_analyze_mood_angry():
    text = "That bug broke everything 😡🤬"
    assert emoji_mood_analyzer.analyze_mood(text) == "angry"

def test_analyze_mood_neutral_when_no_known_emojis():
    text = "Just plain text, no emojis."
    assert emoji_mood_analyzer.analyze_mood(text) == "neutral"

def test_analyze_mood_tie_breaker_alphabetical():
    # Two happy and two sad emojis – tie should resolve to "happy" (alphabetically first)
    text = "Mixed feelings 😄😢😊😞"
    assert emoji_mood_analyzer.analyze_mood(text) == "happy"

# ---------------------------------------------------------------------------
# Test the CLI path that reads from a file. We mock _read_file to avoid disk I/O.
# ---------------------------------------------------------------------------

def test_cli_file_input(monkeypatch: Any, capsys: Any):
    # Mock the internal _read_file function to return a controlled string.
    def mock_read_file(path: str) -> str:
        # Mock rationale: return a string containing angry emojis regardless of path.
        return "System failure! 😡🤬"

    monkeypatch.setattr(emoji_mood_analyzer, "_read_file", mock_read_file)

    # Simulate CLI arguments: program name omitted, we pass the flag directly.
    exit_code = emoji_mood_analyzer.main(["--file", "dummy.txt"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "angry"
