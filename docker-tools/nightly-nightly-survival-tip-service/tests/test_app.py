import unittest
from unittest.mock import patch
from src.app import app

class SurvivalTipServiceTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch("src.app.random.choice")
    def test_tip_endpoint_returns_mocked_tip(self, mock_choice):
        mock_choice.return_value = "Mocked tip for testing."
        response = self.client.get("/tip?scenario=storm")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["tip"], "Mocked tip for testing.")
        self.assertEqual(data["scenario"], "storm")

if __name__ == "__main__":
    unittest.main()
