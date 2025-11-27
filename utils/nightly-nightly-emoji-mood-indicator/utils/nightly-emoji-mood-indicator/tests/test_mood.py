import pytest

# Mock rationale: No external resources are used; the module is pure Python.
# Therefore we can import it directly without network or file I/O.
from src.mood import get_mood_emoji, DEFAULT_EMOJI

@pytest.mark.parametrize(
    "input_mood,expected",
    [
        ("happy", "😊"),
        ("HAPPY", "😊"),  # case‑insensitivity
        ("  happy  ", "😊"),  # whitespace trimming
        ("excited", "🤩"),
        ("sad", "😢"),
        ("angry", "😠"),
        ("confused", "🤔"),
        ("love", "❤️"),
        ("tired", "😴"),
        ("bored", "😐"),
        ("unknown_mood", DEFAULT_EMOJI),  # fallback
        ("", DEFAULT_EMOJI),  # empty string fallback
    ],
)
def test_get_mood_emoji_known_and_unknown(input_mood, expected):
    assert get_mood_emoji(input_mood) == expected

def test_default_emoji_constant():
    # Ensure the default emoji is the expected fallback symbol.
    assert DEFAULT_EMOJI == "❓"
