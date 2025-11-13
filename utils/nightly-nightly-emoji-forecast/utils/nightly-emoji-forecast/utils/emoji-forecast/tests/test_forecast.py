import unittest
from unittest import mock
from emoji_forecast.src.forecast import generate_forecast, EMOJI_SETS

class TestEmojiForecast(unittest.TestCase):
    def test_deterministic_with_mock(self):
        # Mock rationale: force a known hash value to predict output
        with mock.patch('emoji_forecast.src.forecast._hash_city', return_value=3):
            result = generate_forecast("anycity", days=4)
            expected = [EMOJI_SETS[(3 + i) % len(EMOJI_SETS)] for i in range(4)]
            self.assertEqual(result, expected)

    def test_default_parameters(self):
        # Ensure default days = 3 and default city works without errors
        result = generate_forecast("Nowhere")
        self.assertEqual(len(result), 3)
        # All items should be strings from EMOJI_SETS
        for emoji in result:
            self.assertIn(emoji, EMOJI_SETS)

if __name__ == "__main__":
    unittest.main()
