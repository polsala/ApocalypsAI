import unittest
import sys
import io
from unittest.mock import patch

# Mock rationale: We need to test the CLI behavior of the script, including argument parsing
# and printing to stdout. Patching sys.argv allows us to simulate different command-line
# inputs without actually running the script as a separate process. Patching sys.stdout
# allows us to capture and assert the printed output. Patching sys.exit allows us to
# prevent the test runner from exiting prematurely when the script calls exit().

# Add the src directory to the Python path for importing
sys.path.insert(0, 'utils/apocalypse-prep-checklist-generator/src')
from checklist_generator import ChecklistGenerator, main
sys.path.pop(0)

class TestChecklistGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = ChecklistGenerator()

    def test_get_available_scenarios(self):
        scenarios = self.generator.get_available_scenarios()
        expected_scenarios = [
            "Zombie Outbreak",
            "Rogue AI Uprising",
            "Solar Flare Cataclysm",
            "Giant Hamster Invasion"
        ]
        self.assertIsInstance(scenarios, list)
        self.assertListEqual(sorted(scenarios), sorted(expected_scenarios))
        self.assertNotIn("General Preparedness", scenarios)

    def test_generate_checklist_zombie_outbreak(self):
        scenario = "Zombie Outbreak"
        checklist = self.generator.generate_checklist(scenario)
        self.assertIsNotNone(checklist)
        self.assertIn("General Preparedness:", checklist)
        self.assertIn("Scenario-Specific Preparedness (Zombie Outbreak):", checklist)
        self.assertIn("-   ✅ 5-gallon water supply per person", checklist)
        self.assertIn("-   ✅ Durable melee weapon (crowbar, machete)", checklist)
        self.assertIn("-   ✅ 'Headshot Training Manual' (for target practice)", checklist)

    def test_generate_checklist_rogue_ai_uprising(self):
        scenario = "Rogue AI Uprising"
        checklist = self.generator.generate_checklist(scenario)
        self.assertIsNotNone(checklist)
        self.assertIn("General Preparedness:", checklist)
        self.assertIn("Scenario-Specific Preparedness (Rogue AI Uprising):", checklist)
        self.assertIn("-   ✅ EMP device (mocked, for disabling electronics)", checklist)
        self.assertIn("-   ✅ Faraday cage for sensitive electronics", checklist)

    def test_generate_checklist_invalid_scenario(self):
        scenario = "Alien Invasion (Not Implemented)"
        checklist = self.generator.generate_checklist(scenario)
        self.assertIsNone(checklist)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['checklist_generator.py', '--scenario', 'Zombie Outbreak'])
    @patch('sys.exit')
    def test_main_with_valid_scenario(self, mock_exit, mock_stdout):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("--- Apocalypse Prep Checklist: Zombie Outbreak ---", output)
        self.assertIn("Durable melee weapon", output)
        self.assertIn("Stay vigilant, survivor!", output)
        mock_exit.assert_not_called()

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['checklist_generator.py', '--scenario', 'NonExistentScenario'])
    @patch('sys.exit')
    def test_main_with_invalid_scenario(self, mock_exit, mock_stdout):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Error: Scenario 'NonExistentScenario' not found.", output)
        self.assertIn("Available scenarios:", output)
        mock_exit.assert_called_once_with(1)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['checklist_generator.py'])
    @patch('sys.exit')
    def test_main_without_scenario(self, mock_exit, mock_stdout):
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Please specify a scenario using --scenario. Available scenarios:", output)
        self.assertIn("- Zombie Outbreak", output)
        mock_exit.assert_called_once_with(0)

if __name__ == '__main__':
    unittest.main()
