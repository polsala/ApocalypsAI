import unittest
from unittest.mock import patch
from src.app import app, APOCALYPSE_SCENARIOS

class TestApocalypsePrepKit(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('random.sample') # Mock rationale: Ensure deterministic item selection for testing.
    def test_generate_kit_default_scenario(self, mock_sample):
        mock_sample.return_value = ["Crowbar (for cranial re-education)", "Canned Beans (indefinite shelf life)", "First-Aid Kit (for bites and scrapes)"]
        response = self.app.get('/generate_kit')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['scenario'], 'zombie')
        self.assertIn("Crowbar (for cranial re-education)", data['apocalypse_prep_kit'])
        self.assertEqual(len(data['apocalypse_prep_kit']), 3)

    @patch('random.sample') # Mock rationale: Ensure deterministic item selection for testing.
    def test_generate_kit_specific_scenario(self, mock_sample):
        mock_sample.return_value = ["Tin Foil Hat (for mind-probe deflection)", "Laser Pointer (distract their mothership)", "Universal Translator (wishful thinking)"]
        response = self.app.get('/generate_kit?scenario=alien_invasion')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['scenario'], 'alien_invasion')
        self.assertIn("Tin Foil Hat (for mind-probe deflection)", data['apocalypse_prep_kit'])
        self.assertEqual(len(data['apocalypse_prep_kit']), 3)

    def test_generate_kit_invalid_scenario(self):
        response = self.app.get('/generate_kit?scenario=unicorn_stampede')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("Scenario 'unicorn_stampede' not found", data['error'])

    def test_root_endpoint(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("Welcome to the Pocket Apocalypse Prep-Kit!", data['message'])
        self.assertIn("zombie", data['available_scenarios'])
        self.assertIn("disco_apocalypse", data['available_scenarios'])

    @patch('random.sample') # Mock rationale: Ensure deterministic item selection for testing.
    def test_generate_kit_all_scenarios_exist(self, mock_sample):
        # This test ensures all defined scenarios are reachable and return a 200
        for scenario_name in APOCALYPSE_SCENARIOS.keys():
            mock_sample.return_value = APOCALYPSE_SCENARIOS[scenario_name]["items"][:3] # Ensure a valid return value
            response = self.app.get(f'/generate_kit?scenario={scenario_name}')
            self.assertEqual(response.status_code, 200, f"Scenario {scenario_name} failed")
            data = response.get_json()
            self.assertEqual(data['scenario'], scenario_name)
            self.assertGreater(len(data['apocalypse_prep_kit']), 0)

if __name__ == '__main__':
    unittest.main()
