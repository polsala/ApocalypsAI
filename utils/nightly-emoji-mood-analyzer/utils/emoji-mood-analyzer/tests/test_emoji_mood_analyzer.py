import pytest

# Import the function under test.
from emoji_mood_analyzer import analyze

# Mock rationale: No external services are called; the function is pure.
# The tests are deterministic and cover typical, edge‑case, and tie‑breaking scenarios.

@pytest.mark.parametrize(
    "text,expected",
    [
        ("I am so happy! 😄", "happy"),
        ("Feeling sad today 😢", "sad"),
        ("This makes me angry 😡", "angry"),
        ("I love this! ❤️😍", "love"),
        ("Just a regular comment with no emojis.", "neutral"),
        # Tie‑breaking: equal happy and love emojis – happy wins by precedence.
        ("Great job! 😄❤️", "happy"),
        # Multiple emojis of same mood – still that mood.
        ("Party time! 🥳🥳🥳", "happy"),
        # Mixed but sad dominates.
        ("Mixed feelings 😄😢😢", "sad"),
        # Tie between love and sad – love wins by precedence.
        ("Mixed love and sadness ❤️😢", "love"),
        # Emoji not in mapping – should be ignored, fallback to neutral.
        ("Unknown emoji 🤖", "neutral"),
    ],
)
def test_analyze(text, expected):
    assert analyze(text) == expected
