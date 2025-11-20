import builtins
import types

# Mock rationale: we replace the internal emoji extraction to ensure the
# function behaves correctly even if the mapping changes. This keeps the test
# deterministic and independent of the exact EMOJI_MOOD_MAP contents.

from utils.nightly-emoji-mood-analyzer.src import emoji_analyzer


def test_happy_mood(monkeypatch):
    # Mock _extract_emojis to return two positive emojis regardless of input.
    def mock_extract(_):
        return ["😀", "😂"]  # both map to +1
    monkeypatch.setattr(emoji_analyzer, "_extract_emojis", mock_extract)
    assert emoji_analyzer.analyze_mood("any text") == "happy"


def test_sad_mood(monkeypatch):
    # Mock to return two negative emojis.
    def mock_extract(_):
        return ["😢", "💔"]  # both map to -1
    monkeypatch.setattr(emoji_analyzer, "_extract_emojis", mock_extract)
    assert emoji_analyzer.analyze_mood("any text") == "sad"


def test_neutral_mood_no_emojis(monkeypatch):
    # Mock to return empty list – no emojis found.
    monkeypatch.setattr(emoji_analyzer, "_extract_emojis", lambda _: [])
    assert emoji_analyzer.analyze_mood("plain text") == "neutral"


def test_neutral_mood_equal_score(monkeypatch):
    # One positive and one negative emoji → score 0.
    def mock_extract(_):
        return ["😀", "😢"]
    monkeypatch.setattr(emoji_analyzer, "_extract_emojis", mock_extract)
    assert emoji_analyzer.analyze_mood("balanced") == "neutral"
