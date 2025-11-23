import pytest
from src.logger import get_mood_emoji

# Mock rationale: No external dependencies; deterministic keyword matching.

@pytest.mark.parametrize(
    "text,expected",
    [
        ("I am feeling happy and wonderful today!", "😊"),
        ("This is a terrible, sad day.", "😢"),
        ("Just another ordinary commit.", "😐"),
        ("I love this but also a bit frustrated", "😐"),  # tie → neutral
        ("I hate bugs", "😢"),
    ],
)
def test_get_mood_emoji(text, expected):
    assert get_mood_emoji(text) == expected
