import json
import sys
from pathlib import Path

# Mock rationale: All external interactions are avoided; we only test pure functions.

# Import the module under test. Adjust sys.path to locate the src package.
sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))
from mood_tracker import mood_to_emoji, load_custom_mapping, merge_mappings, DEFAULT_MAPPING

def test_default_mappings():
    assert mood_to_emoji("happy") == "😊"
    assert mood_to_emoji("HAPPY") == "😊"  # case‑insensitive
    assert mood_to_emoji("  productive  ") == "🚀"
    assert mood_to_emoji("unknown mood") == "❓"

def test_custom_mapping_loading(tmp_path):
    # Create a temporary JSON file with a custom mapping.
    custom_data = {"ecstatic": "🤗", "sad": "😭"}
    custom_file = tmp_path / "custom.json"
    custom_file.write_text(json.dumps(custom_data), encoding="utf-8")

    loaded = load_custom_mapping(custom_file)
    # Keys should be lower‑cased.
    assert loaded == {"ecstatic": "🤗", "sad": "😭"}

def test_merge_mappings_overrides():
    custom = {"happy": "😁", "new": "🆕"}
    merged = merge_mappings(DEFAULT_MAPPING, custom)
    # Custom entry overrides default.
    assert merged["happy"] == "😁"
    # New entry is added.
    assert merged["new"] == "🆕"
    # Unchanged entries remain.
    assert merged["sad"] == "😢"

def test_mood_to_emoji_with_custom(tmp_path):
    custom_data = {"tired": "🥱", "focused": "🎯"}
    custom_file = tmp_path / "custom.json"
    custom_file.write_text(json.dumps(custom_data), encoding="utf-8")
    custom_mapping = load_custom_mapping(custom_file)
    merged = merge_mappings(DEFAULT_MAPPING, custom_mapping)

    # Custom override works.
    assert mood_to_emoji("tired", merged) == "🥱"
    # New custom mood works.
    assert mood_to_emoji("focused", merged) == "🎯"
    # Fallback to default for untouched moods.
    assert mood_to_emoji("happy", merged) == "😊"
