import builtins
import sys
from types import SimpleNamespace

# Mock rationale: No external dependencies are used, but we include a mock
# to illustrate how one would replace a heavy component if needed.

from src.mood_caster import get_mood_emoji, main


def test_basic_happy():
    assert get_mood_emoji("I am so happy today!") == "😊"


def test_basic_sad():
    assert get_mood_emoji("Feeling sad about the news.") == "😢"


def test_anger_with_mixed_case():
    assert get_mood_emoji("Why is this so Angry???") == "😠"


def test_love_keyword():
    assert get_mood_emoji("I love open source.") == "❤️"


def test_surprise_keyword():
    assert get_mood_emoji("Wow, that was unexpected!") == "😲"


def test_no_keyword_returns_default():
    assert get_mood_emoji("Just a regular sentence.") == "🤔"


def test_cli_output(monkeypatch, capsys):
    # Simulate command‑line arguments
    monkeypatch.setattr(sys, "argv", ["mood_caster", "I am happy"])
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "😊"

# Additional deterministic test using a mocked tokeniser to ensure isolation

def test_tokeniser_mock(monkeypatch):
    # Replace the internal _tokenize function with a deterministic mock
    mock_tokens = ["mocked", "happy"]
    monkeypatch.setattr('src.mood_caster._tokenize', lambda _: mock_tokens)
    # The mock includes the keyword "happy", so we expect the happy emoji
    assert get_mood_emoji("anything") == "😊"
