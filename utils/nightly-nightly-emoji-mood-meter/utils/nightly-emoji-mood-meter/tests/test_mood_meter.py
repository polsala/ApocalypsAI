import pytest

# Mock rationale: The tests are deterministic and do not require any external resources.

from src.mood_meter import get_mood_emoji

@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("I am so happy today!", "😊"),
        ("This is terrible, I am sad.", "😢"),
        ("Why are you so angry?", "😠"),
        ("Wow, that was unexpected!", "😲"),
        ("I'm not sure what to think.", "🤔"),
        ("Just a neutral statement.", "🤔"),
    ],
)
def test_get_mood_emoji(input_text, expected):
    assert get_mood_emoji(input_text) == expected
