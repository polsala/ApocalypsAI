import unittest
import sys
import os
from unittest.mock import patch

# Mock rationale: This is needed to allow the test file to import the module
# under test as if it were a standard package, without modifying sys.path
# globally or relying on complex package structures for a simple utility.
# It ensures the test is self-contained and runnable from its own directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from checklist_generator import generate_checklist, BASE_ITEMS, SCENARIO_SPECIFIC_ITEMS

class TestChecklistGenerator(unittest.TestCase):

    def test_generate_checklist_zombie_scenario(self):
        # Test basic zombie scenario with base items
        # Mock rationale: No external mocks needed as the function relies on internal constants.
        # The test directly calls the function with predefined inputs.
        checklist = generate_checklist(scenario="zombie")
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), len(BASE_ITEMS))
        for item in BASE_ITEMS:
            self.assertIn(item, checklist)
        for item in SCENARIO_SPECIFIC_ITEMS["zombie"]:
            self.assertIn(item, checklist)
        self.assertIn("Melee weapon (e.g., crowbar, baseball bat)", checklist)

    def test_generate_checklist_ai_uprising_no_base(self):
        # Test AI uprising scenario without base items
        # Mock rationale: No external mocks needed.
        checklist = generate_checklist(scenario="ai_uprising", include_base=False)
        self.assertIsInstance(checklist, list)
        # Should contain only scenario-specific items and no base items
        self.assertEqual(len(checklist), len(SCENARIO_SPECIFIC_ITEMS["ai_uprising"]))
        for item in BASE_ITEMS:
            self.assertNotIn(item, checklist)
        for item in SCENARIO_SPECIFIC_ITEMS["ai_uprising"]:
            self.assertIn(item, checklist)
        self.assertIn("EMP device (if available)", checklist)

    def test_generate_checklist_economic_collapse_with_custom(self):
        # Test economic collapse with custom items
        # Mock rationale: No external mocks needed.
        custom = ["Emergency cryptocurrency wallet", "Gold coins"]
        checklist = generate_checklist(scenario="economic_collapse", custom_items=custom)
        self.assertIsInstance(checklist, list)
        for item in BASE_ITEMS:
            self.assertIn(item, checklist)
        for item in SCENARIO_SPECIFIC_ITEMS["economic_collapse"]:
            self.assertIn(item, checklist)
        for item in custom:
            self.assertIn(item, checklist)
        self.assertIn("Emergency cryptocurrency wallet", checklist)
        self.assertIn("Gold coins", checklist)

    def test_generate_checklist_unknown_scenario(self):
        # Test an unknown scenario, should only return base items if include_base is True
        # Mock rationale: No external mocks needed.
        checklist = generate_checklist(scenario="alien_invasion")
        self.assertIsInstance(checklist, list)
        self.assertEqual(len(checklist), len(BASE_ITEMS))
        for item in BASE_ITEMS:
            self.assertIn(item, checklist)
        self.assertNotIn("Ray gun", checklist) # Should not include alien-specific items

    def test_generate_checklist_no_duplicates_and_sorted(self):
        # Test that duplicates are removed and list is sorted
        # Mock rationale: No external mocks needed.
        custom = ["Water (1 gallon per person per day for at least 3 days)", "Flashlight and extra batteries", "New custom item"]
        checklist = generate_checklist(scenario="zombie", custom_items=custom)
        self.assertIsInstance(checklist, list)
        # Check for duplicates by comparing length of list and set
        self.assertEqual(len(checklist), len(set(checklist)))
        # Check if sorted
        self.assertEqual(checklist, sorted(checklist))
        self.assertIn("New custom item", checklist)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_function_output(self, mock_print, mock_parse_args):
        # Test the main function's output for a specific scenario
        # Mock rationale: We mock argparse.ArgumentParser.parse_args to control
        # the command-line arguments passed to main() without actually running
        # the CLI. We mock builtins.print to capture what main() prints to stdout
        # and assert its content, preventing actual console output during tests.
        mock_parse_args.return_value = argparse.Namespace(
            scenario='zombie',
            no_base=False,
            custom=[]
        )
        from checklist_generator import main
        main()

        # Assert that print was called with expected output structure
        self.assertTrue(any("--- Apocalypse Prep Checklist for Zombie" in call.args[0] for call in mock_print.call_args_list))
        self.assertTrue(any("[ ] Water (1 gallon per person per day for at least 3 days)" in call.args[0] for call in mock_print.call_args_list))
        self.assertTrue(any("[ ] Melee weapon (e.g., crowbar, baseball bat)" in call.args[0] for call in mock_print.call_args_list))

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_function_output_no_base_custom(self, mock_print, mock_parse_args):
        # Test the main function's output for a scenario with no base and custom items
        # Mock rationale: Same as above, controlling CLI args and capturing print output.
        mock_parse_args.return_value = argparse.Namespace(
            scenario='ai_uprising',
            no_base=True,
            custom=['Offline AI disabler']
        )
        from checklist_generator import main
        main()

        self.assertTrue(any("--- Apocalypse Prep Checklist for Ai Uprising" in call.args[0] for call in mock_print.call_args_list))
        self.assertFalse(any("[ ] Water (1 gallon per person per day for at least 3 days)" in call.args[0] for call in mock_print.call_args_list))
        self.assertTrue(any("[ ] EMP device (if available)" in call.args[0] for call in mock_print.call_args_list))
        self.assertTrue(any("[ ] Offline AI disabler" in call.args[0] for call in mock_print.call_args_list))


if __name__ == '__main__':
    unittest.main()
