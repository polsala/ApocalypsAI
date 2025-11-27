import pytest
from src.analyzer import analyze_mood

# Mock rationale: No external services are used; the function is deterministic.

@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("I am so happy and joyful!", "😄"),
        ("This is terrible, I feel sad.", "😢"),
        ("Why are you so angry?", "😠"),
        ("Just an ordinary statement.", "😐"),
        ("I love this awesome day", "😄"),
        ("I hate the bad weather", "😠"),
        ("Feeling down but hopeful", "😢"),
    ],
)
def test_analyze_mood(input_text, expected):
    assert analyze_mood(input_text) == expected
