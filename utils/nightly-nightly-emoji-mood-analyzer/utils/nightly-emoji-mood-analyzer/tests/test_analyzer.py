import sys
from pathlib import Path

# Ensure the src directory is on the import path when running tests directly.
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src"))

from analyzer import get_mood_emoji


def test_happy_keywords():
    assert get_mood_emoji("I am so happy today!") == "😄"
    assert get_mood_emoji("What a wonderful experience.") == "😄"
    assert get_mood_emoji("Love this awesome product.") == "😄"


def test_sad_keywords():
    assert get_mood_emoji("Feeling very sad and blue.") == "😢"
    assert get_mood_emoji("It was a miserable day.") == "😢"


def test_angry_keywords():
    assert get_mood_emoji("I am angry about the delay.") == "😠"
    assert get_mood_emoji("That was a terrible, hateful comment.") == "😠"


def test_surprised_keywords():
    assert get_mood_emoji("Wow, I did not expect that!") == "😲"
    assert get_mood_emoji("She was shocked by the news.") == "😲"


def test_neutral_when_no_match():
    # Mock rationale: No keywords present, should fall back to neutral emoji.
    assert get_mood_emoji("Just an ordinary statement.") == "😐"

# CLI integration test – deterministic because we invoke the module directly.

def test_cli_output(capsys, monkeypatch):
    # Mock sys.argv to simulate command line invocation.
    monkeypatch.setattr(sys, "argv", ["prog", "I love this!"])
    # Import the module as a script.
    import importlib
    import analyzer as mod
    importlib.reload(mod)  # Ensure any top‑level code runs with new argv.
    mod._cli()
    captured = capsys.readouterr()
    assert captured.out.strip() == "😄"
