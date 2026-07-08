import unittest
from unittest.mock import patch, MagicMock
import json
import datetime
import os
from drone_sim import generate_report # Assuming drone_sim.py is in the same directory for testing

class TestDroneSim(unittest.TestCase):

    @patch('drone_sim.datetime')
    @patch('drone_sim.random.random')
    @patch('drone_sim.random.choice')
    @patch('drone_sim.random.randint')
    @patch.dict(os.environ, {'DRONE_ID': 'TEST-DRONE-001'}) # Mock rationale: Set a consistent DRONE_ID for tests
    def test_report_with_resources_and_anomalies(self, mock_randint, mock_choice, mock_random, mock_datetime):
        # Mock rationale: Ensure deterministic timestamp
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 27, 10, 30, 0, tzinfo=datetime.timezone.utc)
        mock_datetime.timezone.utc = datetime.timezone.utc

        # Mock rationale: Control random outcomes for resources and anomalies
        # random.random() calls:
        # 1. For resources (should be < 0.7)
        # 2. For anomalies (should be < 0.3)
        mock_random.side_effect = [0.5, 0.2] # 0.5 < 0.7 (resources), 0.2 < 0.3 (anomalies)

        # Mock rationale: Control random choices for items and descriptions
        mock_choice.side_effect = [
            "Alpha", "01-01", # Location
            "scrap metal", # Resource 1
            "diluted fuel", # Resource 2
            "temporal distortion detected", # Anomaly 1
            "unidentified signal source" # Anomaly 2
        ]

        # Mock rationale: Control random integers for quantities and counts
        # random.randint() calls:
        # 1. num_resources (1-3) -> 2
        # 2. quantity for scrap metal (1-10) -> 5
        # 3. quantity for diluted fuel (1-10) -> 3
        # 4. num_anomalies (1-2) -> 2
        mock_randint.side_effect = [2, 5, 3, 2]

        report_str = generate_report()
        report = json.loads(report_str)

        self.assertEqual(report["drone_id"], "TEST-DRONE-001")
        self.assertEqual(report["timestamp"], "2023-10-27T10:30:00+00:00")
        self.assertEqual(report["location"]["sector"], "Alpha")
        self.assertEqual(report["location"]["grid"], "01-01")
        self.assertEqual(len(report["findings"]), 4) # 2 resources + 2 anomalies

        self.assertEqual(report["findings"][0]["type"], "resource")
        self.assertEqual(report["findings"][0]["item"], "scrap metal")
        self.assertEqual(report["findings"][0]["quantity"], 5)

        self.assertEqual(report["findings"][1]["type"], "resource")
        self.assertEqual(report["findings"][1]["item"], "diluted fuel")
        self.assertEqual(report["findings"][1]["quantity"], 3)

        self.assertEqual(report["findings"][2]["type"], "anomaly")
        self.assertEqual(report["findings"][2]["description"], "temporal distortion detected")

        self.assertEqual(report["findings"][3]["type"], "anomaly")
        self.assertEqual(report["findings"][3]["description"], "unidentified signal source")

    @patch('drone_sim.datetime')
    @patch('drone_sim.random.random')
    @patch('drone_sim.random.choice')
    @patch('drone_sim.random.randint')
    @patch.dict(os.environ, {'DRONE_ID': 'TEST-DRONE-002'}) # Mock rationale: Set a consistent DRONE_ID for tests
    def test_report_no_findings(self, mock_randint, mock_choice, mock_random, mock_datetime):
        # Mock rationale: Ensure deterministic timestamp
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 27, 11, 0, 0, tzinfo=datetime.timezone.utc)
        mock_datetime.timezone.utc = datetime.timezone.utc

        # Mock rationale: Control random outcomes to ensure no resources or anomalies are found
        mock_random.side_effect = [0.8, 0.4] # 0.8 > 0.7 (no resources), 0.4 > 0.3 (no anomalies)

        # Mock rationale: Control random choices for location
        mock_choice.side_effect = ["Beta", "02-02"]

        # Mock rationale: No randint calls expected for findings, but location grid uses it.
        mock_randint.side_effect = [2, 2] # For location grid 02-02

        report_str = generate_report()
        report = json.loads(report_str)

        self.assertEqual(report["drone_id"], "TEST-DRONE-002")
        self.assertEqual(report["timestamp"], "2023-10-27T11:00:00+00:00")
        self.assertEqual(report["location"]["sector"], "Beta")
        self.assertEqual(report["location"]["grid"], "02-02")
        self.assertEqual(len(report["findings"]), 1)
        self.assertEqual(report["findings"][0]["type"], "status")
        self.assertEqual(report["findings"][0]["description"], "No significant findings, routine patrol.")

    @patch('drone_sim.datetime')
    @patch('drone_sim.random.random')
    @patch('drone_sim.random.choice')
    @patch('drone_sim.random.randint')
    @patch.dict(os.environ, {'DRONE_ID': 'TEST-DRONE-003'}) # Mock rationale: Set a consistent DRONE_ID for tests
    def test_report_only_resources(self, mock_randint, mock_choice, mock_random, mock_datetime):
        # Mock rationale: Ensure deterministic timestamp
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 10, 27, 12, 0, 0, tzinfo=datetime.timezone.utc)
        mock_datetime.timezone.utc = datetime.timezone.utc

        # Mock rationale: Control random outcomes to ensure resources are found, but no anomalies
        mock_random.side_effect = [0.1, 0.5] # 0.1 < 0.7 (resources), 0.5 > 0.3 (no anomalies)

        # Mock rationale: Control random choices for location and resources
        mock_choice.side_effect = [
            "Gamma", "03-03", # Location
            "purified water" # Resource 1
        ]

        # Mock rationale: Control random integers for quantities and counts
        mock_randint.side_effect = [1, 7, 3, 3] # num_resources=1, quantity=7, location grid 03-03

        report_str = generate_report()
        report = json.loads(report_str)

        self.assertEqual(report["drone_id"], "TEST-DRONE-003")
        self.assertEqual(report["timestamp"], "2023-10-27T12:00:00+00:00")
        self.assertEqual(report["location"]["sector"], "Gamma")
        self.assertEqual(report["location"]["grid"], "03-03")
        self.assertEqual(len(report["findings"]), 1)

        self.assertEqual(report["findings"][0]["type"], "resource")
        self.assertEqual(report["findings"][0]["item"], "purified water")
        self.assertEqual(report["findings"][0]["quantity"], 7)

if __name__ == '__main__':
    unittest.main()
