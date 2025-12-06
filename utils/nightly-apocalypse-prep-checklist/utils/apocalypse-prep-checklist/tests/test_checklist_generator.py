import unittest
from unittest.mock import patch, mock_open
import json
import os
import sys

# Mock rationale: We need to simulate the file system for scenarios.json
# and user input for the main function without actual file I/O or interactive prompts.
# This ensures tests are deterministic and run offline.

# Add src directory to sys.path for importing the module under test
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from checklist_generator import ChecklistGenerator, main

# Define a mock scenarios.json content
MOCK_SCENARIOS_CONTENT = json.dumps({
    "general_items": [
        "Water (1 gallon/person/day)",
        "First aid kit",
        "Flashlight"
    ],
    "scenarios": {
        "zombie_outbreak": {
            "name": "Zombie Outbreak",
            "description": "Zombies everywhere!",
            "specific_items": [
                "Crowbar",
                "Durable clothing"
            ],
            "whimsical_advice": "Run faster!"
        },
        "solar_flare": {
            "name": "Solar Flare",
            "description": "No power!",
            "specific_items": [
                "Hand-crank radio",
                "Faraday cage"
            ],
            "whimsical_advice": "Enjoy the silence!"
        }
    }
})

class TestChecklistGenerator(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=MOCK_SCENARIOS_CONTENT)
    @patch('os.path.exists', return_value=True)
    def setUp(self, mock_exists, mock_file):
        # Mock rationale: Ensure the ChecklistGenerator loads the mock data
        # by patching 'open' and 'os.path.exists'.
        self.generator = ChecklistGenerator(scenarios_file='scenarios.json')
        self.assertTrue(self.generator.data is not None)

    def test_load_scenarios_success(self):
        # Test that scenarios are loaded correctly
        self.assertIn('zombie_outbreak', self.generator.data['scenarios'])
        self.assertIn('general_items', self.generator.data)

    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('os.path.exists', return_value=True)
    def test_load_scenarios_invalid_json(self, mock_exists, mock_file):
        # Mock rationale: Simulate a corrupted scenarios.json file.
        generator = ChecklistGenerator(scenarios_file='scenarios.json')
        self.assertIsNone(generator.data)

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('os.path.exists', return_value=False)
    def test_load_scenarios_file_not_found(self, mock_exists, mock_file):
        # Mock rationale: Simulate scenarios.json being absent.
        generator = ChecklistGenerator(scenarios_file='scenarios.json')
        self.assertIsNone(generator.data)

    def test_get_available_scenarios(self):
        # Test retrieval of scenario keys
        scenarios = self.generator.get_available_scenarios()
        self.assertListEqual(sorted(scenarios), sorted(['zombie_outbreak', 'solar_flare']))

    def test_generate_checklist_single_scenario_no_resources(self):
        # Test checklist generation for one scenario without user resources
        checklist = self.generator.generate_checklist(['zombie_outbreak'], [])
        self.assertIn('Scenario: Zombie Outbreak', checklist)
        self.assertIn('[ ] Water (1 gallon/person/day)', checklist)
        self.assertIn('[ ] Crowbar', checklist)
        self.assertIn('Whimsical Advice: Run faster!', checklist)
        self.assertNotIn('[HAVE]', checklist)

    def test_generate_checklist_multiple_scenarios_with_resources(self):
        # Test checklist generation for multiple scenarios with user resources
        user_resources = ['Water (1 gallon/person/day)', 'First aid kit', 'Crowbar']
        checklist = self.generator.generate_checklist(['zombie_outbreak', 'solar_flare'], user_resources)

        # Zombie Outbreak checks
        self.assertIn('Scenario: Zombie Outbreak', checklist)
        self.assertIn('[HAVE] Water (1 gallon/person/day)', checklist)
        self.assertIn('[HAVE] First aid kit', checklist)
        self.assertIn('[HAVE] Crowbar', checklist)
        self.assertIn('[ ] Durable clothing', checklist)
        self.assertIn('Whimsical Advice: Run faster!', checklist)

        # Solar Flare checks
        self.assertIn('Scenario: Solar Flare', checklist)
        self.assertIn('[HAVE] Water (1 gallon/person/day)', checklist)
        self.assertIn('[HAVE] First aid kit', checklist)
        self.assertIn('[ ] Hand-crank radio', checklist)
        self.assertIn('[ ] Faraday cage', checklist)
        self.assertIn('Whimsical Advice: Enjoy the silence!', checklist)

    def test_generate_checklist_unknown_scenario(self):
        # Test behavior with an unknown scenario key
        checklist = self.generator.generate_checklist(['unknown_doom'], [])
        self.assertIn("Warning: Scenario 'unknown_doom' not found.", checklist)

    @patch('builtins.input', side_effect=['1,2', 'water (1 gallon/person/day), flashlight'])
    @patch('builtins.print')
    @patch('checklist_generator.ChecklistGenerator._load_scenarios', return_value=json.loads(MOCK_SCENARIOS_CONTENT))
    def test_main_function_success(self, mock_load_scenarios, mock_print, mock_input):
        # Mock rationale: Simulate user input and capture print output
        # to verify the main function's flow and final output.
        main()
        mock_print.assert_any_call('Welcome, future survivor! Let\'s prepare for the end...\n')
        mock_print.assert_any_call('--- Your Personalized Apocalypse Prep Checklist ---')
        mock_print.assert_any_call('Good luck, survivor! May your preps be plentiful and your doom be delayed.')
        
        # Verify specific content in the generated checklist output
        printed_output = "\n".join([call.args[0] for call in mock_print.call_args_list if call.args])
        self.assertIn('Scenario: Zombie Outbreak', printed_output)
        self.assertIn('[HAVE] Water (1 gallon/person/day)', printed_output)
        self.assertIn('[HAVE] Flashlight', printed_output)
        self.assertIn('[ ] Crowbar', printed_output)
        self.assertIn('Scenario: Solar Flare', printed_output)
        self.assertIn('[ ] Hand-crank radio', printed_output)

    @patch('builtins.input', side_effect=['invalid', '1', 'water'])
    @patch('builtins.print')
    @patch('checklist_generator.ChecklistGenerator._load_scenarios', return_value=json.loads(MOCK_SCENARIOS_CONTENT))
    def test_main_function_invalid_scenario_input(self, mock_load_scenarios, mock_print, mock_input):
        # Mock rationale: Test error handling for invalid user input for scenario selection.
        main()
        mock_print.assert_any_call('Invalid input. Please enter numbers separated by commas.')
        mock_print.assert_any_call('--- Your Personalized Apocalypse Prep Checklist ---') # Should still proceed after valid input

    @patch('builtins.input', side_effect=['5', '1', 'water'])
    @patch('builtins.print')
    @patch('checklist_generator.ChecklistGenerator._load_scenarios', return_value=json.loads(MOCK_SCENARIOS_CONTENT))
    def test_main_function_out_of_range_scenario_input(self, mock_load_scenarios, mock_print, mock_input):
        # Mock rationale: Test error handling for out-of-range scenario selection.
        main()
        mock_print.assert_any_call(f'Invalid choice: 5. Please enter numbers between 1 and 2.')
        mock_print.assert_any_call('--- Your Personalized Apocalypse Prep Checklist ---') # Should still proceed after valid input

    @patch('builtins.input', side_effect=['', '1', 'water'])
    @patch('builtins.print')
    @patch('checklist_generator.ChecklistGenerator._load_scenarios', return_value=json.loads(MOCK_SCENARIOS_CONTENT))
    def test_main_function_empty_scenario_input(self, mock_load_scenarios, mock_print, mock_input):
        # Mock rationale: Test error handling for empty scenario selection.
        main()
        mock_print.assert_any_call('No valid scenarios selected. Please try again.')
        mock_print.assert_any_call('--- Your Personalized Apocalypse Prep Checklist ---') # Should still proceed after valid input

    @patch('checklist_generator.ChecklistGenerator._load_scenarios', return_value=None)
    @patch('builtins.print')
    def test_main_function_data_load_error(self, mock_print, mock_load_scenarios):
        # Mock rationale: Simulate a failure in loading scenario data.
        main()
        mock_print.assert_any_call('Exiting due to data loading error.')

    @patch('checklist_generator.ChecklistGenerator._load_scenarios', return_value={'general_items': [], 'scenarios': {}})
    @patch('builtins.print')
    def test_main_function_no_scenarios_available(self, mock_print, mock_load_scenarios):
        # Mock rationale: Simulate a scenarios.json with no actual scenarios.
        main()
        mock_print.assert_any_call('No scenarios available. Exiting.')

if __name__ == '__main__':
    unittest.main()
