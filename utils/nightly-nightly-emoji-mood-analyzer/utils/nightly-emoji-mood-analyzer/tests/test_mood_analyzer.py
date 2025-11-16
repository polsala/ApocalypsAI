import pathlib
import sys

# Mock rationale: adjust import path to locate src module
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mood_analyzer import analyze_file, categorize_emojis, extract_emojis


def test_extract_emojis():
    text = "Hello 😃 world 😂!"
    emojis = extract_emojis(text)
    assert emojis == ["😃", "😂"]


def test_categorize_emojis_happy():
    emojis = ["😀", "😃", "😂"]
    assert categorize_emojis(emojis) == "happy"


def test_categorize_emojis_love():
    emojis = ["😍", "❤️", "🥰"]
    assert categorize_emojis(emojis) == "love"


def test_categorize_emojis_neutral_no_emojis():
    assert categorize_emojis([]) == "neutral"


def test_analyze_file(tmp_path: pathlib.Path):
    # Mock rationale: create a temporary file with known emojis
    content = "Good morning 😃! I love this 😍."
    file_path = tmp_path / "sample.txt"
    file_path.write_text(content, encoding="utf-8")
    mood = analyze_file(str(file_path))
    # Expected dominant mood is happy (1 happy vs 1 love, tie -> first encountered)
    # Counter.most_common returns the first inserted in a tie, which is happy.
    assert mood == "happy"


def test_analyze_file_no_emojis(tmp_path: pathlib.Path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("Just plain text.", encoding="utf-8")
    mood = analyze_file(str(file_path))
    assert mood == "neutral"
