import pytest
from src.generator import generate_password

# Mock rationale: deterministic algorithm uses only the inputs; no external state.

def test_alnum_output_is_deterministic():
    phrase = "openai"
    salt = "apocalypse"
    length = 12
    expected = "openaiapocal"  # first 12 chars of "openaiapocalypse"
    result = generate_password(phrase=phrase, salt=salt, length=length, charset="alnum")
    assert result == expected


def test_alpha_charset_filters_non_letters():
    phrase = "1234"
    salt = "ABCD"
    length = 8
    # combined = "1234ABCD" -> repeated = "1234ABCD"
    # after alpha filter -> "ABCD"
    # padded with 'x' to reach length 8 -> "ABCDxxxx"
    expected = "ABCDxxxx"
    result = generate_password(phrase=phrase, salt=salt, length=length, charset="alpha")
    assert result == expected


def test_numeric_charset_filters_non_digits():
    phrase = "openai"
    salt = "apocalypse"
    length = 6
    # combined has no digits, so result should be padded with 'x'
    expected = "xxxxxx"
    result = generate_password(phrase=phrase, salt=salt, length=length, charset="numeric")
    assert result == expected


def test_invalid_charset_raises():
    with pytest.raises(ValueError, match="Unsupported charset"):
        generate_password("a", "b", length=4, charset="emoji")  # type: ignore[arg-type]
