import unittest
from unittest import mock

from emoji_forecast import get_emoji_forecast


class TestEmojiForecast(unittest.TestCase):
    @mock.patch('emoji_forecast._hash_date')
    def test_mocked_hash(self, mock_hash):
        # Mock rationale: deterministic hash values for test.
        mock_hash.return_value = 0
        self.assertEqual(get_emoji_forecast('any-date'), "🌞")
        mock_hash.return_value = 5
        self.assertEqual(get_emoji_forecast('any-date'), "🌦️")
        mock_hash.return_value = 9
        self.assertEqual(get_emoji_forecast('any-date'), "❄️")

    def test_invalid_format(self):
        # Function does not validate format; it still returns an emoji.
        result = get_emoji_forecast('not-a-date')
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)


if __name__ == '__main__':
    unittest.main()
