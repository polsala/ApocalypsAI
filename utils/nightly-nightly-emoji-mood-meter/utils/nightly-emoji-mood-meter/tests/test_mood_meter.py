import sys
from pathlib import Path

# Ensure the src directory is on the import path
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "src"))

from mood_meter import get_mood_emoji

def test_happy_keywords():
    assert get_mood_emoji("I am so happy today!") == "😊"
    assert get_mood_emoji("What a fantastic day.") == "😊"

def test_sad_keywords():
    assert get_mood_emoji("Feeling sad and down.") == "😢"
    assert get_mood_emoji("It was a terrible experience.") == "😢"

def test_angry_keywords():
    assert get_mood_emoji("I am angry about the delay.") == "😠"
    assert get_mood_emoji("That makes me mad!") == "😠"

def test_love_keywords():
    assert get_mood_emoji("I love this project.") == "❤️"
    assert get_mood_emoji("Adore the new feature.") == "❤️"

def test_surprise_keywords():
    assert get_mood_emoji("Wow, that was unexpected!") == "😲"
    assert get_mood_emoji("I am shocked by the results.") == "😲"

def test_default_neutral():
    # No matching keywords → neutral face
    assert get_mood_emoji("Just an ordinary statement.") == "😐"

# Mock rationale comments (no external calls are made, but we keep the pattern for consistency)
# Mock rationale: The utility is fully deterministic and does not perform network I/O, so no external mocks are required.
