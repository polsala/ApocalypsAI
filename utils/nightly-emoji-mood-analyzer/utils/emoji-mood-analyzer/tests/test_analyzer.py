import pytest
from src.analyzer import analyze_mood

@pytest.mark.parametrize(
    "text,expected",
    [
        ("I love this!", "😄"),
        ("Feeling sad about the bug", "😢"),
        ("What a great day", "👍"),
        ("I'm so confused", "🤔"),
        ("Nothing special here", "😐"),
        ("Excited and happy", "🤩"),  # first match 'excited'
    ],
)
def test_analyze_mood(text, expected):
    assert analyze_mood(text) == expected
