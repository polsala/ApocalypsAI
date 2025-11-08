import unittest
from src.encoder import encode_message, decode_message, ENCODE_DICT, DECODE_DICT

class TestWastelandWhispererEncoder(unittest.TestCase):

    def test_encode_simple_message(self):
        # Test a basic message with dictionary terms
        message = "DANGER! Enemy spotted near the WATER source."
        expected = "DGR ENY SPOTTED NEAR THE WTR SOURCE"
        self.assertEqual(encode_message(message), expected)

    def test_decode_simple_message(self):
        # Test decoding a basic message with dictionary codes
        message = "DGR ENY SPOTTED NEAR THE WTR SOURCE"
        expected = "DANGER ENEMY SPOTTED NEAR THE WATER SOURCE"
        self.assertEqual(decode_message(message), expected)

    def test_encode_decode_roundtrip(self):
        # Test that encoding then decoding returns the original (normalized) message
        original = "HELP! FRIENDLY SIGNAL UNKNOWN LOCATION. OVER."
        encoded = encode_message(original)
        decoded = decode_message(encoded)
        # The decoded message will be normalized (uppercase, no punctuation)
        self.assertEqual(decoded, "HELP FRIENDLY SIGNAL UNKNOWN LOCATION OVER")
        # And re-encoding the decoded message should yield the same encoded message
        self.assertEqual(encode_message(decoded), encoded)

    def test_empty_message(self):
        # Test with an empty string
        self.assertEqual(encode_message(""), "")
        self.assertEqual(decode_message(""), "")
        self.assertEqual(encode_message("   "), "") # Only spaces
        self.assertEqual(decode_message("   "), "")

    def test_message_with_no_dictionary_terms(self):
        # Test a message that contains no terms from the dictionary
        message = "HELLO WORLD THIS IS A TEST MESSAGE"
        expected = "HELLO WORLD THIS IS A TEST MESSAGE"
        self.assertEqual(encode_message(message), expected)
        self.assertEqual(decode_message(message), expected)

    def test_message_with_mixed_case_and_punctuation(self):
        # Test that normalization handles mixed case and punctuation correctly
        message = "wAtEr sUpPlIeS lOw! rDv aT bAsE nOrTh."
        expected_encoded = "WTR SPL LOW RDV AT BAS NRT"
        expected_decoded = "WATER SUPPLIES LOW RENDEZVOUS AT BASE NORTH"
        self.assertEqual(encode_message(message), expected_encoded)
        self.assertEqual(decode_message(expected_encoded), expected_decoded)

    def test_message_with_numbers(self):
        # Test that numbers are preserved, and punctuation like '.' is removed by normalization
        message = "BASE ALPHA 7 LOCATION 34.5 12.3"
        expected_encoded = "BAS ALPHA 7 LOC 345 123"
        expected_decoded = "BASE ALPHA 7 LOCATION 345 123"
        self.assertEqual(encode_message(message), expected_encoded)
        self.assertEqual(decode_message(expected_encoded), expected_decoded)

    def test_unknown_codes_in_decode(self):
        # Test decoding a message with unknown codes (should be preserved as is)
        message = "DGR UNKNOWNCODE1 WTR UNKNOWNCODE2"
        expected = "DANGER UNKNOWNCODE1 WATER UNKNOWNCODE2"
        self.assertEqual(decode_message(message), expected)

    def test_dictionary_completeness(self):
        # Ensure all terms in ENCODE_DICT have a corresponding entry in DECODE_DICT
        # Mock rationale: This test ensures internal consistency of the dictionaries.
        # It's deterministic and offline as it only checks predefined data structures.
        for term, code in ENCODE_DICT.items():
            self.assertEqual(DECODE_DICT[code], term)

    def test_normalization_multiple_spaces(self):
        message = "  DANGER   WATER    BASE  "
        expected_encoded = "DGR WTR BAS"
        self.assertEqual(encode_message(message), expected_encoded)
        expected_decoded = "DANGER WATER BASE"
        self.assertEqual(decode_message(expected_encoded), expected_decoded)
