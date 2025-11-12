import pytest
from src.emoji_encoder import encode, decode, LETTER_TO_EMOJI, EMOJI_TO_LETTER

# Mock rationale: All tests are deterministic and run offline; no external resources are accessed.

def test_encode_basic():
    assert encode("HELLO") == LETTER_TO_EMOJI["H"] + LETTER_TO_EMOJI["E"] + LETTER_TO_EMOJI["L"] * 2 + LETTER_TO_EMOJI["O"]

def test_decode_basic():
    emoji_seq = LETTER_TO_EMOJI["W"] + LETTER_TO_EMOJI["O"] + LETTER_TO_EMOJI["R"] + LETTER_TO_EMOJI["L"] + LETTER_TO_EMOJI["D"]
    assert decode(emoji_seq) == "WORLD"

def test_encode_invalid_character():
    with pytest.raises(ValueError) as excinfo:
        encode("Hello")  # contains lowercase letters
    assert "Unsupported character" in str(excinfo.value)

def test_decode_invalid_emoji():
    # Using an emoji not present in the mapping
    invalid_emoji = "🚀"
    with pytest.raises(ValueError) as excinfo:
        decode(invalid_emoji)
    assert "Unsupported emoji" in str(excinfo.value)

def test_round_trip():
    original = "PYTHON"
    encoded = encode(original)
    decoded = decode(encoded)
    assert decoded == original
