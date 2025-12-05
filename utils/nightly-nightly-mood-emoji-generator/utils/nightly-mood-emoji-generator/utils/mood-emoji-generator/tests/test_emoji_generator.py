import pytest
from src.emoji_generator import get_emoji, DEFAULT_EMOJI

# Mock rationale: No external calls, deterministic mapping.

@pytest.mark.parametrize(
    "input_mood,expected",
    [
        ("happy", "😄"),
        ("HAPPY", "😄"),
        ("  sad  ", "😢"),
        ("Excited", "🤩"),
        ("unknown", DEFAULT_EMOJI),
        ("", DEFAULT_EMOJI),
    ],
)
def test_get_emoji_known_and_unknown(input_mood, expected):
    assert get_emoji(input_mood) == expected


def test_get_emoji_type_error():
    with pytest.raises(TypeError):
        get_emoji(123)
