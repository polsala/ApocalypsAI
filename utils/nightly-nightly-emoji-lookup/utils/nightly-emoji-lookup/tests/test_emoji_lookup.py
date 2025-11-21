import pytest

# Mock rationale: No external resources are required; the lookup is purely in‑memory.
# The tests therefore remain deterministic and offline.

from utils.nightly-emoji-lookup.src.emoji_lookup import get_emoji


def test_known_emoji_exact_match():
    assert get_emoji("rocket") == "🚀"
    assert get_emoji("coffee") == "☕"


def test_known_emoji_case_insensitive():
    assert get_emoji("RoCkEt") == "🚀"
    assert get_emoji("  coffee  ") == "☕"  # leading/trailing whitespace ignored


def test_unknown_emoji_returns_none():
    assert get_emoji("unicorn") is None
    assert get_emoji("") is None


def test_multi_word_keyword():
    assert get_emoji("thumbs up") == "👍"
    assert get_emoji("LIGHT BULB") == "💡"

# Additional sanity check: the internal map should not be mutated by the function
def test_emoji_map_immutable():
    original = get_emoji("star")
    # Attempt to modify the returned value (strings are immutable, but we check no side‑effects)
    _ = original + "!"
    assert get_emoji("star") == original
