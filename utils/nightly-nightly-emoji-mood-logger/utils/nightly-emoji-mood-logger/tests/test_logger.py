# Tests for the emoji mood logger utility.
# These tests are deterministic and run offline; no network calls are made.
# Mock rationale: not required – the implementation is pure Python.

import pytest
from src.logger import get_mood_emoji

@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("I am so happy today!", "😊"),
        ("Feeling sad about the loss.", "😢"),
        ("He is angry and furious.", "😠"),
        ("I love this project!", "❤️"),
        ("Wow, that was surprising!", "😲"),
        ("Just an ordinary day.", "🤔"),
        ("Great job, team!", "😊"),  # matches 'great'
        ("She felt down and upset.", "😢"),  # matches 'down'/'upset'
    ],
)
def test_get_mood_emoji(input_text, expected):
    assert get_mood_emoji(input_text) == expected

def test_cli_stdout(capsys, monkeypatch):
    # Simulate command‑line invocation with a positional argument.
    test_args = ["someprog", "I love the new feature"]
    monkeypatch.setattr('sys.argv', test_args)
    # Import the module as a script.
    import importlib
    import src.logger as logger_mod
    logger_mod.main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "❤️"
