import pytest

# Mock rationale: No external services are called; all logic is pure and deterministic.

from emoji_commit_message_generator.generator import generate_message, _EMOJI_MAP, _DEFAULT_EMOJI


def test_generate_message_basic_fix():
    desc = "fix crash on empty input"
    result = generate_message(desc)
    assert result.startswith("🐛 ")
    assert result == "🐛 Fix crash on empty input"


def test_generate_message_feature_add():
    # Should pick the first matching keyword ("feature" before "add")
    desc = "add new authentication feature"
    result = generate_message(desc)
    assert result.startswith("✨ ")
    assert result == "✨ Add new authentication feature"


def test_generate_message_docs():
    desc = "update README and docs"
    result = generate_message(desc)
    assert result.startswith("📝 ")
    assert result == "📝 Update README and docs"


def test_generate_message_no_match_uses_default():
    desc = "reorganize project structure"
    result = generate_message(desc)
    assert result.startswith(_DEFAULT_EMOJI + " ")
    assert result == f"{_DEFAULT_EMOJI} Reorganize project structure"


def test_generate_message_preserves_internal_capitalisation():
    desc = "fix issue with APIKey handling"
    result = generate_message(desc)
    # Only first character is forced to upper case; internal caps stay
    assert result == "🐛 Fix issue with APIKey handling"


def test_generate_message_raises_on_empty():
    with pytest.raises(ValueError):
        generate_message("   ")
