import pytest

# Import the function from the sibling src directory.
# The test runner adds the repository root to PYTHONPATH, so we can import directly.
from logger import get_mood_emoji


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("I am so happy about the release!", "😊"),
        ("What a terrible bug, I hate it.", "😢"),
        ("Refactored the module.", "😐"),
        ("Great job, but the test failed.", "😊"),  # happy overrides sad
        ("The build error is bad.", "😢"),
        ("Love the new UI, but the performance is bad.", "😊"),
    ],
)
def test_get_mood_emoji(input_text, expected):
    assert get_mood_emoji(input_text) == expected


def test_non_string_input_raises():
    with pytest.raises(TypeError):
        get_mood_emoji(123)  # type: ignore[arg-type]

# Mock rationale: No external services are called; the function is pure.
# Therefore, tests are fully deterministic and can run offline.
