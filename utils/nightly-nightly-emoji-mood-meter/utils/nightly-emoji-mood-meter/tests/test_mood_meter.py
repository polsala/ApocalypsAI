import pytest
from src.mood_meter import get_mood_emoji

@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("I love this new feature!", "😄"),
        ("The build failed again.", "💥"),
        ("I'm sad about the regression.", "😞"),
        ("Warning: low disk space.", "⚠️"),
        ("Can we maybe try a different approach?", "🤔"),
        ("Just a neutral statement.", "🤖"),
    ],
)
def test_get_mood_emoji(input_text, expected):
    assert get_mood_emoji(input_text) == expected
