import unittest
import json
import os
from unittest.mock import patch, mock_open

# Adjust the import path for testing when the test file is in tests/ and module in src/
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from checklist_generator import (
    load_scenarios,
    generate_checklist,
    get_scenario_choice,
    get_location_choice,
    get_people_count
)
sys.path.pop(0)

class TestChecklistGenerator(unittest.TestCase):

    MOCK_SCENARIOS_JSON = {
        "scenarios": [
            {
                "name": "Zombie Outbreak",
                "keywords": ["zombie"],
                "base_items": ["first aid kit", "water"],
                "location_specific": {
                    "urban": ["crowbar"],
                    "rural": ["hunting rifle"]
                },
                "people_specific": {
                    "1": ["small backpack"],
                    "2-5": ["medium backpack"],
                    "6+": ["large backpack"]
                }
            },
            {
                "name": "Nuclear Winter",
                "keywords": ["nuclear"],
                "base_items": ["iodine tablets", "canned food"],
                "location_specific": {
                    "urban": ["gas mask"],
                    "rural": ["wood stove"]
                },
                "people_specific": {
                    "1": ["thermal blanket"],
                    "2-5": ["sleeping bags"],
                    "6+": ["generator"]
                }
            }
        ],
        "general_items": [
            "flashlight",
            "batteries",
            "multi-tool"
        ]
    }

    # Mock rationale: We need to simulate reading the scenarios.json file
    # without actually touching the filesystem, ensuring tests are deterministic
    # and offline. `mock_open` allows us to provide a string as the file content.
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(MOCK_SCENARIOS_JSON))
    @patch('json.load', return_value=MOCK_SCENARIOS_JSON)
    def test_load_scenarios_success(self, mock_json_load, mock_file_open):
        data = load_scenarios('dummy_path/scenarios.json')
        self.assertIsNotNone(data)
        self.assertEqual(data, self.MOCK_SCENARIOS_JSON)
        mock_file_open.assert_called_once_with('dummy_path/scenarios.json', 'r', encoding='utf-8')
        mock_json_load.assert_called_once()

    # Mock rationale: Simulate FileNotFoundError without creating a non-existent file.
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_scenarios_file_not_found(self, mock_file_open):
        data = load_scenarios('non_existent_path/scenarios.json')
        self.assertIsNone(data)
        mock_file_open.assert_called_once()

    # Mock rationale: Simulate a malformed JSON file without creating one.
    @patch('builtins.open', new_callable=mock_open, read_data='{invalid json')
    @patch('json.load', side_effect=json.JSONDecodeError('Expecting value', 'doc', 1))
    def test_load_scenarios_json_decode_error(self, mock_json_load, mock_file_open):
        data = load_scenarios('malformed_path/scenarios.json')
        self.assertIsNone(data)
        mock_file_open.assert_called_once()
        mock_json_load.assert_called_once()

    def test_generate_checklist_zombie_urban_1_person(self):
        scenario_data = self.MOCK_SCENARIOS_JSON
        chosen_scenario = scenario_data['scenarios'][0] # Zombie Outbreak
        location_type = 'urban'
        people_count = 1
        checklist = generate_checklist(scenario_data, chosen_scenario, location_type, people_count)
        expected = {
            "General Essentials": sorted(["flashlight", "batteries", "multi-tool"]),
            "Scenario-Specific": sorted(["first aid kit", "water"]),
            "Location-Specific": sorted(["crowbar"]),
            "Group-Specific": sorted(["small backpack"])
        }
        self.assertEqual(checklist, expected)

    def test_generate_checklist_nuclear_rural_3_people(self):
        scenario_data = self.MOCK_SCENARIOS_JSON
        chosen_scenario = scenario_data['scenarios'][1] # Nuclear Winter
        location_type = 'rural'
        people_count = 3
        checklist = generate_checklist(scenario_data, chosen_scenario, location_type, people_count)
        expected = {
            "General Essentials": sorted(["flashlight", "batteries", "multi-tool"]),
            "Scenario-Specific": sorted(["iodine tablets", "canned food"]),
            "Location-Specific": sorted(["wood stove"]),
            "Group-Specific": sorted(["sleeping bags"])
        }
        self.assertEqual(checklist, expected)

    def test_generate_checklist_zombie_rural_7_people(self):
        scenario_data = self.MOCK_SCENARIOS_JSON
        chosen_scenario = scenario_data['scenarios'][0] # Zombie Outbreak
        location_type = 'rural'
        people_count = 7
        checklist = generate_checklist(scenario_data, chosen_scenario, location_type, people_count)
        expected = {
            "General Essentials": sorted(["flashlight", "batteries", "multi-tool"]),
            "Scenario-Specific": sorted(["first aid kit", "water"]),
            "Location-Specific": sorted(["hunting rifle"]),
            "Group-Specific": sorted(["large backpack"])
        }
        self.assertEqual(checklist, expected)

    # Mock rationale: Simulate user input for CLI prompts. `patch('builtins.input')`
    # allows us to provide a sequence of return values for `input()` calls.
    @patch('builtins.input', side_effect=['1'])
    @patch('builtins.print') # Mock rationale: Suppress print statements during input prompts
    def test_get_scenario_choice_valid(self, mock_print, mock_input):
        scenarios = self.MOCK_SCENARIOS_JSON['scenarios']
        chosen = get_scenario_choice(scenarios)
        self.assertEqual(chosen, scenarios[0])

    @patch('builtins.input', side_effect=['urban'])
    @patch('builtins.print')
    def test_get_location_choice_valid(self, mock_print, mock_input):
        location = get_location_choice()
        self.assertEqual(location, 'urban')

    @patch('builtins.input', side_effect=['5'])
    @patch('builtins.print')
    def test_get_people_count_valid(self, mock_print, mock_input):
        count = get_people_count()
        self.assertEqual(count, 5)

    @patch('builtins.input', side_effect=['invalid', '2'])
    @patch('builtins.print') # Mock rationale: Suppress print statements during invalid input tests
    def test_get_scenario_choice_invalid_then_valid(self, mock_print, mock_input):
        scenarios = self.MOCK_SCENARIOS_JSON['scenarios']
        chosen = get_scenario_choice(scenarios)
        self.assertEqual(chosen, scenarios[1])
        self.assertTrue(mock_print.called)

    @patch('builtins.input', side_effect=['wrong', 'rural'])
    @patch('builtins.print')
    def test_get_location_choice_invalid_then_valid(self, mock_print, mock_input):
        location = get_location_choice()
        self.assertEqual(location, 'rural')
        self.assertTrue(mock_print.called)

    @patch('builtins.input', side_effect=['zero', '-1', '0', '10'])
    @patch('builtins.print')
    def test_get_people_count_invalid_then_valid(self, mock_print, mock_input):
        count = get_people_count()
        self.assertEqual(count, 10)
        self.assertTrue(mock_print.called)

if __name__ == '__main__':
    unittest.main()
