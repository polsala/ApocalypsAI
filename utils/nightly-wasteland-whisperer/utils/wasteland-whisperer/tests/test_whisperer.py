import pytest
from src.whisperer import WastelandWhisperer

@pytest.fixture
def whisperer():
    return WastelandWhisperer()

# Mock rationale: No external dependencies to mock. All operations are pure functions
# based on input strings and internal, deterministic logic. Tests directly verify
# the correctness of these internal algorithms.

class TestSubstitutionCipher:
    def test_encode_decode_simple_message(self, whisperer):
        original = "Hello World 123!"
        encoded = whisperer.encode_substitution(original)
        decoded = whisperer.decode_substitution(encoded)
        assert encoded == "KHOOR ZRUOG 456!"
        assert decoded == original

    def test_encode_decode_all_caps(self, whisperer):
        original = "APOCALYPSE NOW"
        encoded = whisperer.encode_substitution(original)
        decoded = whisperer.decode_substitution(encoded)
        assert encoded == "DSLFDOBSVH QRZ"
        assert decoded == original

    def test_encode_decode_all_lowercase(self, whisperer):
        original = "survival guide"
        encoded = whisperer.encode_substitution(original)
        decoded = whisperer.decode_substitution(encoded)
        assert encoded == "vxuylydo jxlgh"
        assert decoded == original

    def test_encode_decode_numbers_only(self, whisperer):
        original = "0123456789"
        encoded = whisperer.encode_substitution(original)
        decoded = whisperer.decode_substitution(encoded)
        assert encoded == "3456789012"
        assert decoded == original

    def test_encode_decode_mixed_characters(self, whisperer):
        original = "Zebra-007!"
        encoded = whisperer.encode_substitution(original)
        decoded = whisperer.decode_substitution(encoded)
        assert encoded == "Cheud-330!"
        assert decoded == original

    def test_empty_string(self, whisperer):
        original = ""
        encoded = whisperer.encode_substitution(original)
        decoded = whisperer.decode_substitution(encoded)
        assert encoded == ""
        assert decoded == original

    def test_special_characters_preserved(self, whisperer):
        original = "!@#$%^&*()_+-=[]{}\|;:'\",.<>/?`~"
        encoded = whisperer.encode_substitution(original)
        decoded = whisperer.decode_substitution(encoded)
        assert encoded == original
        assert decoded == original

class TestMorseCode:
    def test_encode_decode_simple_message(self, whisperer):
        original = "SOS"
        encoded = whisperer.encode_morse(original)
        decoded = whisperer.decode_morse(encoded)
        assert encoded == "... --- ..."
        assert decoded == original

    def test_encode_decode_hello_world(self, whisperer):
        original = "Hello World"
        encoded = whisperer.encode_morse(original)
        decoded = whisperer.decode_morse(encoded)
        assert encoded == ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
        assert decoded == "HELLO WORLD" # Morse decodes to uppercase

    def test_encode_decode_numbers_and_punctuation(self, whisperer):
        original = "Alert 123!"
        encoded = whisperer.encode_morse(original)
        decoded = whisperer.decode_morse(encoded)
        assert encoded == ".- .-.. . .-. - / .---- ..--- ...-- .-.-.-"
        assert decoded == "ALERT 123."

    def test_empty_string(self, whisperer):
        original = ""
        encoded = whisperer.encode_morse(original)
        decoded = whisperer.decode_morse(encoded)
        assert encoded == ""
        assert decoded == original

    def test_unmappable_characters_ignored(self, whisperer):
        original_with_unmapped = "Hello ` World"
        encoded = whisperer.encode_morse(original_with_unmapped)
        # The '`' character should be ignored during encoding as it's not in the map
        assert encoded == ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
        decoded = whisperer.decode_morse(encoded)
        assert decoded == "HELLO WORLD"

    def test_decode_with_extra_spaces_in_morse_chars(self, whisperer):
        encoded = "...   ---   ..."
        decoded = whisperer.decode_morse(encoded)
        assert decoded == "SOS"

    def test_decode_with_malformed_morse_sequences(self, whisperer):
        # 'XYZ' and 'ABC' are not valid Morse sequences and should be ignored
        encoded_unknown = "... --- XYZ / ABC"
        decoded_unknown = whisperer.decode_morse(encoded_unknown)
        assert decoded_unknown == "SO"

    def test_decode_with_multiple_word_separators(self, whisperer):
        encoded = "... --- ... / / .-- --- .-. .-.. -.."
        decoded = whisperer.decode_morse(encoded)
        assert decoded == "SOS WORLD"
