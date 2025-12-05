import pytest
from src.emoji_encoder import encode, decode, LETTER_TO_EMOJI


def test_encode_basic():
    assert encode("abc") == LETTER_TO_EMOJI['a'] + LETTER_TO_EMOJI['b'] + LETTER_TO_EMOJI['c']


def test_decode_basic():
    seq = LETTER_TO_EMOJI['x'] + LETTER_TO_EMOJI['y'] + LETTER_TO_EMOJI['z']
    assert decode(seq) == "xyz"


def test_roundtrip():
    original = "helloworld"
    encoded = encode(original)
    decoded = decode(encoded)
    assert decoded == original


def test_encode_invalid_character():
    with pytest.raises(ValueError):
        encode("Hello")  # uppercase H not allowed


def test_decode_invalid_sequence():
    with pytest.raises(ValueError):
        decode("🚀")  # emoji not in mapping
