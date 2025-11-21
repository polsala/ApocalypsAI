import tempfile
from pathlib import Path
from collections import Counter

# Mock rationale: we use a temporary file with deterministic content to avoid any external I/O.

from src.mood_tracker import parse_mood_log, emoji_summary, MOOD_EMOJI


def test_parse_mood_log_basic():
    sample_content = """happy\nsad\nhappy\nexcited\nunknown\n\n"""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write(sample_content)
        tmp_path = Path(tmp.name)
    # Ensure the file is flushed and closed before reading
    tmp_path.touch()
    counts = parse_mood_log(tmp_path)
    expected = Counter({"happy": 2, "sad": 1, "excited": 1})
    assert counts == expected


def test_emoji_summary_respects_order_and_counts():
    counts = Counter({"happy": 2, "sad": 1, "excited": 1})
    result = emoji_summary(counts)
    # Order should follow MOOD_EMOJI definition: happy, sad, excited, angry, neutral, tired
    expected = MOOD_EMOJI["happy"] * 2 + MOOD_EMOJI["sad"] + MOOD_EMOJI["excited"]
    assert result == expected


def test_parse_mood_log_ignores_unknown_and_empty_lines():
    sample_content = """angry\n\nfoo\nneutral\n"""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write(sample_content)
        tmp_path = Path(tmp.name)
    counts = parse_mood_log(tmp_path)
    expected = Counter({"angry": 1, "neutral": 1})
    assert counts == expected
