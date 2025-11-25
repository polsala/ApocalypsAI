import builtins
import io
import sys
from pathlib import Path

# Mock rationale: Import the module directly from the relative path without installing the package.
# This keeps the test self‑contained and offline.
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from logger import get_mood_emoji, _detect_mood


def test_detect_mood_happy():
    assert _detect_mood("I am feeling very happy today!") == "happy"
    assert _detect_mood("Joyful moments are the best.") == "happy"


def test_detect_mood_sad():
    assert _detect_mood("It was a sad day.") == "sad"
    assert _detect_mood("I feel down and depressed.") == "sad"


def test_detect_mood_angry():
    assert _detect_mood("He was angry about the delay.") == "angry"
    assert _detect_mood("She is furious!") == "angry"


def test_detect_mood_neutral():
    assert _detect_mood("Just an ordinary statement.") == "neutral"
    assert _detect_mood("") == "neutral"


def test_get_mood_emoji_mapping():
    assert get_mood_emoji("I love this!") == "😊"
    assert get_mood_emoji("Feeling sad.") == "😢"
    assert get_mood_emoji("That makes me mad.") == "😠"
    assert get_mood_emoji("Nothing special.") == "😐"


def test_cli_stdout_capture(monkeypatch, capsys):
    # Mock rationale: Simulate command‑line execution without spawning a subprocess.
    from logger import _cli

    # Provide text via argument
    exit_code = _cli(["I am so excited!"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "😊"

    # Provide text via STDIN
    fake_stdin = io.StringIO("I feel terrible and sad.")
    monkeypatch.setattr(sys, "stdin", fake_stdin)
    exit_code = _cli([])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "😢"
