import unittest
import json
from src.app import app, classify_debris

class TestCosmicDebrisClassifier(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_classify_debris_temporal(self):
        # Mock rationale: The classify_debris function is pure and deterministic, no external mocks needed.
        description = "A strange device that seems to loop through time."
        result = classify_debris(description)
        self.assertEqual(result["category"], "Temporal Fragment")
        self.assertIn("paradoxes", result["survival_tip"])

    def test_classify_debris_eldritch_goo(self):
        # Mock rationale: The classify_debris function is pure and deterministic, no external mocks needed.
        description = "A pulsating, viscous goo found near the crater."
        result = classify_debris(description)
        self.assertEqual(result["category"], "Eldritch Goo")
        self.assertIn("taste it", result["survival_tip"])

    def test_classify_debris_stellar_shard(self):
        # Mock rationale: The classify_debris function is pure and deterministic, no external mocks needed.
        description = "A shimmering crystal, clearly from a distant star."
        result = classify_debris(description)
        self.assertEqual(result["category"], "Stellar Shard")
        self.assertIn("potable water", result["survival_tip"])

    def test_classify_debris_void_touched_relic(self):
        # Mock rationale: The classify_debris function is pure and deterministic, no external mocks needed.
        description = "An ancient, dark artifact that whispers of the void."
        result = classify_debris(description)
        self.assertEqual(result["category"], "Void-Touched Relic")
        self.assertIn("cursed", result["survival_tip"])

    def test_classify_debris_mundane_misdirection(self):
        # Mock rationale: The classify_debris function is pure and deterministic, no external mocks needed.
        description = "Just a regular old rock, covered in dust."
        result = classify_debris(description)
        self.assertEqual(result["category"], "Mundane Misdirection")
        self.assertIn("throwing", result["survival_tip"])

    def test_classify_endpoint_success(self):
        # Mock rationale: Flask's test client provides an isolated environment for testing HTTP requests without needing external network mocks.
        response = self.app.post('/classify',
                                 data=json.dumps({"description": "A shimmering crystal."}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["category"], "Stellar Shard")

    def test_classify_endpoint_missing_description(self):
        # Mock rationale: Flask's test client provides an isolated environment for testing HTTP requests without needing external network mocks.
        response = self.app.post('/classify',
                                 data=json.dumps({"not_description": "something"}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertIn("Missing 'description'", data["error"])

    def test_classify_endpoint_empty_body(self):
        # Mock rationale: Flask's test client provides an isolated environment for testing HTTP requests without needing external network mocks.
        response = self.app.post('/classify',
                                 data=json.dumps({}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertIn("Missing 'description'", data["error"])
