import unittest
import sys
import os

# Add the src directory to the Python path to allow importing scrambler
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from scrambler import scramble_text

class TestScrambler(unittest.TestCase):

    def test_empty_string(self):
        # Test with an empty string, should return empty.
        self.assertEqual(scramble_text("", intensity=0.5, seed=1), "")

    def test_zero_intensity(self):
        # Test with zero intensity, should return original text.
        text = "Hello World"
        self.assertEqual(scramble_text(text, intensity=0.0, seed=1), text)

    def test_full_intensity_is_different(self):
        # Test with full intensity, should almost certainly be different.
        text = "This is a test string for maximum glitching."
        glitched_text = scramble_text(text, intensity=1.0, seed=1)
        self.assertNotEqual(glitched_text, text)
        # It should still produce *some* output, not just empty
        self.assertGreater(len(glitched_text), 0)

    def test_deterministic_output_with_seed(self):
        # Mock rationale: Using a fixed seed for the random number generator ensures
        # that the output of scramble_text is always the same for the same input
        # and seed, making the test deterministic and offline.
        text = "ApocalypsAI Integrator Agent"
        seed = 123
        result1 = scramble_text(text, intensity=0.3, seed=seed)
        result2 = scramble_text(text, intensity=0.3, seed=seed)
        self.assertEqual(result1, result2)
        self.assertEqual(result1, "Apoc@lypsAI Integr@tor Agent") # Expected output for this seed/intensity

        text2 = "Another test string for determinism."
        seed2 = 456
        result3 = scramble_text(text2, intensity=0.6, seed=seed2)
        result4 = scramble_text(text2, intensity=0.6, seed=seed2)
        self.assertEqual(result3, result4)
        self.assertEqual(result3, "Anoth3r test string for determinism.") # Expected output for this seed/intensity

    def test_different_seeds_produce_different_output(self):
        # Ensure different seeds lead to different results (probabilistically).
        text = "Randomness check"
        result1 = scramble_text(text, intensity=0.5, seed=1)
        result2 = scramble_text(text, intensity=0.5, seed=2)
        self.assertNotEqual(result1, result2)

    def test_intensity_range_validation(self):
        # Test that intensity outside [0, 1] raises ValueError.
        text = "Test"
        with self.assertRaises(ValueError):
            scramble_text(text, intensity=-0.1)
        with self.assertRaises(ValueError):
            scramble_text(text, intensity=1.1)

    def test_various_glitch_types_at_medium_intensity(self):
        # Test that various glitch types (sub, ins, del, case) occur.
        text = "The quick brown fox jumps over the lazy dog."
        glitched_text = scramble_text(text, intensity=0.4, seed=789)
        expected_glitched_text = "t h!E q c k! !b r o w n f 0 x j u m p 5 0 v 3 r 7 h 3 l @ z y d 0 g ."
        self.assertEqual(glitched_text, expected_glitched_text)

    def test_segment_reversal_at_high_intensity(self):
        text = "This is a long sentence to test segment reversal."
        # Mock rationale: Using a fixed seed for the random number generator ensures
        # that the output of scramble_text is always the same for the same input
        # and seed, making the test deterministic and offline.
        glitched_text_with_reversal = scramble_text(text, intensity=0.9, seed=101)
        expected_reversal_text = "Th!s is a l0ng s3ntence to lasr3v3r tnm3g3s t."
        self.assertEqual(glitched_text_with_reversal, expected_reversal_text)

    def test_full_string_reversal_at_high_intensity(self):
        text = "Reverse this entire string please."
        # Mock rationale: Using a fixed seed for the random number generator ensures
        # that the output of scramble_text is always the same for the same input
        # and seed, making the test deterministic and offline.
        glitched_text = scramble_text(text, intensity=0.9, seed=200)
        expected_full_reversal_text = ".3sa3lp gn!rts 3r!tn3 s!ht 3sr3v3R"
        self.assertEqual(glitched_text, expected_full_reversal_text)

    def test_character_substitution_logic(self):
        text = "aeiouAEIOU12345"
        # Mock rationale: Using a fixed seed for the random number generator ensures
        # that the output of scramble_text is always the same for the same input
        # and seed, making the test deterministic and offline.
        glitched_text = scramble_text(text, intensity=1.0, seed=300)
        expected_sub_text = "@310u4€!0U12345"
        self.assertEqual(glitched_text, expected_sub_text)

    def test_character_insertion_logic(self):
        text = "abc"
        # Mock rationale: Using a fixed seed for the random number generator ensures
        # that the output of scramble_text is always the same for the same input
        # and seed, making the test deterministic and offline.
        glitched_text = scramble_text(text, intensity=1.0, seed=400)
        expected_ins_text = "a!b@c#"
        self.assertEqual(glitched_text, expected_ins_text)

    def test_character_deletion_logic(self):
        text = "abcdef"
        # Mock rationale: Using a fixed seed for the random number generator ensures
        # that the output of scramble_text is always the same for the same input
        # and seed, making the test deterministic and offline.
        glitched_text = scramble_text(text, intensity=1.0, seed=502)
        expected_del_text = "abc"
        self.assertEqual(glitched_text, expected_del_text)

    def test_case_change_logic(self):
        text = "aBcDeF"
        # Mock rationale: Using a fixed seed for the random number generator ensures
        # that the output of scramble_text is always the same for the same input
        # and seed, making the test deterministic and offline.
        glitched_text = scramble_text(text, intensity=1.0, seed=600)
        expected_case_text = "AbCdEf"
        self.assertEqual(glitched_text, expected_case_text)

if __name__ == '__main__':
    unittest.main()
