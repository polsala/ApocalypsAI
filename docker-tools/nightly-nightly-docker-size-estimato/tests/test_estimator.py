import unittest
from unittest.mock import patch, Mock
import src.estimator as estimator


class TestEstimator(unittest.TestCase):
    @patch('src.estimator.requests.get')
    def test_get_image_size_official(self, mock_get):
        # Mock response for an official library image (e.g., python:3.9)
        mock_resp = Mock()
        mock_resp.raise_for_status = Mock()
        mock_resp.json.return_value = {'full_size': 123456789}
        mock_get.return_value = mock_resp

        size = estimator.get_image_size('python:3.9')
        self.assertEqual(size, 117)  # 123456789 bytes ≈ 117.7 MB → int 117
        mock_get.assert_called_with('https://hub.docker.com/v2/repositories/library/python/tags/3.9/', timeout=5)

    @patch('src.estimator.requests.get')
    def test_get_image_size_user(self, mock_get):
        # Mock response for a user namespace image without explicit tag (defaults to latest)
        mock_resp = Mock()
        mock_resp.raise_for_status = Mock()
        mock_resp.json.return_value = {'full_size': 20971520}  # 20 MB
        mock_get.return_value = mock_resp

        size = estimator.get_image_size('myuser/myrepo')
        self.assertEqual(size, 20)
        mock_get.assert_called_with('https://hub.docker.com/v2/repositories/myuser/myrepo/tags/latest/', timeout=5)


if __name__ == '__main__':
    unittest.main()
