import unittest
from unittest.mock import patch, MagicMock
import json
from src.app import app # Import the Flask app directly

class TestWastelandCourierDispatcher(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('src.app.random.uniform')
    def test_optimize_route_basic(self, mock_uniform):
        # Mock rationale: Ensure deterministic distance calculation for testing.
        # Without mocking, random.uniform would make tests non-deterministic.
        mock_uniform.return_value = 10.0 # Simulate a fixed distance for all segments

        payload = {
            "start": "Oasis Haven",
            "end": "Dusty Flats",
            "waypoints": ["Sector Alpha"]
        }
        response = self.app.post('/optimize_route',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertIn("path_taken", data)
        self.assertEqual(data["path_taken"], ["Oasis Haven", "Sector Alpha", "Dusty Flats"])
        self.assertIn("overall_danger_rating", data)
        self.assertIn("estimated_total_resource_consumption", data)
        self.assertIn("detailed_segments", data)
        self.assertEqual(len(data["detailed_segments"]), 2)

        # Check calculated values based on mocked uniform distance (10.0)
        # Oasis Haven -> Sector Alpha: (0.05+0.05 + 0.8+0.2)/4 * 10 = 1.1/4 * 10 = 2.75
        # Sector Alpha -> Dusty Flats: (0.8+0.2 + 0.1+0.5)/4 * 10 = 1.6/4 * 10 = 4.0
        # Total danger: 2.75 + 4.0 = 6.75
        self.assertAlmostEqual(data["overall_danger_rating"], 6.75)

        # Resource consumption: (distance * 0.1) + (segment_danger * 0.05)
        # Segment 1: (10 * 0.1) + (2.75 * 0.05) = 1 + 0.1375 = 1.1375
        # Segment 2: (10 * 0.1) + (4.0 * 0.05) = 1 + 0.2 = 1.2
        # Total consumption: 1.1375 + 1.2 = 2.3375
        self.assertAlmostEqual(data["estimated_total_resource_consumption"], 2.34) # Rounded to 2 decimal places

    @patch('src.app.random.uniform')
    def test_optimize_route_no_waypoints(self, mock_uniform):
        # Mock rationale: Ensure deterministic distance calculation for testing.
        mock_uniform.return_value = 20.0

        payload = {
            "start": "Oasis Haven",
            "end": "Ruined City Center"
        }
        response = self.app.post('/optimize_route',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertEqual(data["path_taken"], ["Oasis Haven", "Ruined City Center"])
        self.assertEqual(len(data["detailed_segments"]), 1)

        # Oasis Haven -> Ruined City Center: (0.05+0.05 + 0.9+0.9)/4 * 20 = 2.0/4 * 20 = 10.0
        self.assertAlmostEqual(data["overall_danger_rating"], 10.0)
        # Consumption: (20 * 0.1) + (10.0 * 0.05) = 2 + 0.5 = 2.5
        self.assertAlmostEqual(data["estimated_total_resource_consumption"], 2.5)

    def test_optimize_route_missing_fields(self):
        payload = {
            "start": "Oasis Haven"
            # "end" is missing
        }
        response = self.app.post('/optimize_route',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Start and end points are required.")

    @patch('src.app.random.uniform')
    def test_optimize_route_unknown_sectors(self, mock_uniform):
        # Mock rationale: Ensure deterministic distance calculation for testing.
        mock_uniform.return_value = 15.0

        payload = {
            "start": "Unknown Outpost A",
            "end": "Unknown Outpost B",
            "waypoints": ["Mysterious Swamp"]
        }
        response = self.app.post('/optimize_route',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertEqual(data["path_taken"], ["Unknown Outpost A", "Mysterious Swamp", "Unknown Outpost B"])
        self.assertEqual(len(data["detailed_segments"]), 2)

        # For unknown sectors, hazard is hardcoded to 0.5 for radiation and mutants.
        # Segment 1 (Unknown A -> Mysterious Swamp): (0.5+0.5 + 0.5+0.5)/4 * 15 = 1.0/4 * 15 = 7.5
        # Segment 2 (Mysterious Swamp -> Unknown B): (0.5+0.5 + 0.5+0.5)/4 * 15 = 1.0/4 * 15 = 7.5
        # Total danger: 7.5 + 7.5 = 15.0
        self.assertAlmostEqual(data["overall_danger_rating"], 15.0)

        # Consumption: (distance * 0.1) + (segment_danger * 0.05)
        # Segment 1: (15 * 0.1) + (7.5 * 0.05) = 1.5 + 0.375 = 1.875
        # Segment 2: (15 * 0.1) + (7.5 * 0.05) = 1.5 + 0.375 = 1.875
        # Total consumption: 1.875 + 1.875 = 3.75
        self.assertAlmostEqual(data["estimated_total_resource_consumption"], 3.75)

if __name__ == '__main__':
    unittest.main()
