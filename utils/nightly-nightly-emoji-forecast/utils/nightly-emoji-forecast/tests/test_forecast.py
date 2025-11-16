import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Ensure the src directory is on the import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from forecast import location_to_emoji

class TestForecast(unittest.TestCase):
    @patch('forecast.hashlib.sha256')
    def test_location_to_emoji_sunny(self, mock_sha):
        """# Mock rationale: replace the hash to return a deterministic value mapping to index 0 (sunny)."""
        mock_obj = MagicMock()
        mock_obj.hexdigest.return_value = '0' * 64  # int value 0 -> index 0
        mock_sha.return_value = mock_obj
        self.assertEqual(location_to_emoji('anywhere'), '☀️')

    @patch('forecast.hashlib.sha256')
    def test_location_to_emoji_rain(self, mock_sha):
        """# Mock rationale: replace the hash to return a deterministic value mapping to index 3 (rain)."""
        mock_obj = MagicMock()
        # Hex string that yields integer 3 when converted (e.g., '3' followed by zeros)
        mock_obj.hexdigest.return_value = '3' + '0' * 63
        mock_sha.return_value = mock_obj
        self.assertEqual(location_to_emoji('rainy town'), '🌧️')

    @patch('forecast.hashlib.sha256')
    def test_location_to_emoji_fog(self, mock_sha):
        """# Mock rationale: replace the hash to return a deterministic value mapping to index 6 (fog)."""
        mock_obj = MagicMock()
        # Hex that yields integer 6
        mock_obj.hexdigest.return_value = '6' + '0' * 63
        mock_sha.return_value = mock_obj
        self.assertEqual(location_to_emoji('misty hills'), '🌫️')

if __name__ == '__main__':
    unittest.main()
