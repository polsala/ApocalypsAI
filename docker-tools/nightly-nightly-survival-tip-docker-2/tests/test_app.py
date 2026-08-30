import unittest
import json
from src.app import app, TIPS, get_random_tip

class TestSurvivalTip(unittest.TestCase):
    def test_get_random_tip(self):
        tip = get_random_tip()
        self.assertIn(tip, TIPS)

    def test_tip_endpoint(self):
        client = app.test_client()
        response = client.get("/tip")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("tip", data)
        self.assertIn(data["tip"], TIPS)

if __name__ == "__main__":
    unittest.main()
