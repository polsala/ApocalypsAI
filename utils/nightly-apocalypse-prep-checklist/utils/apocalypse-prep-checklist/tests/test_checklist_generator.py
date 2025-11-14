import unittest
from unittest.mock import patch
import io
from src.checklist_generator import (
    get_base_checklist,
    get_scenario_specific_items,
    get_location_specific_items,
    generate_checklist,
    main
)

class TestChecklistGenerator(unittest.TestCase):

    def test_get_base_checklist(self):
        checklist = get_base_checklist()
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), 10) # Ensure a substantial base list
        self.assertIn("First aid kit", checklist)
        self.assertIn("Water (1 gallon per person per day for at least 3 days)", checklist)

    def test_get_scenario_specific_items_zombie(self):
        items = get_scenario_specific_items("zombie")
        self.assertIsInstance(items, list)
        self.assertIn("Crowbar or blunt weapon (for close encounters)", items)
        self.assertIn("Emergency brain-repellent spray (experimental)", items)
        self.assertNotIn("Potassium iodide pills (radiation protection)", items)

    def test_get_scenario_specific_items_nuclear(self):
        items = get_scenario_specific_items("nuclear")
        self.assertIsInstance(items, list)
        self.assertIn("Potassium iodide pills (radiation protection)", items)
        self.assertIn("Geiger counter (radiation detection)", items)
        self.assertNotIn("Crowbar or blunt weapon (for close encounters)", items)

    def test_get_scenario_specific_items_ai_uprising(self):
        items = get_scenario_specific_items("ai_uprising")
        self.assertIsInstance(items, list)
        self.assertIn("EMP device (theoretical, for disabling electronics)", items)
        self.assertIn("Faraday cage (for protecting electronics)", items)
        self.assertNotIn("Tin foil hat (for mind-control resistance)", items) # This is alien_invasion

    def test_get_scenario_specific_items_unknown(self):
        items = get_scenario_specific_items("unknown_scenario")
        self.assertEqual(items, [])

    def test_get_location_specific_items_urban(self):
        items = get_location_specific_items("urban")
        self.assertIsInstance(items, list)
        self.assertIn("Bolt cutters (for navigating locked areas)", items)
        self.assertIn("Rooftop access tools", items)
        self.assertNotIn("Hunting/fishing gear", items)

    def test_get_location_specific_items_rural(self):
        items = get_location_specific_items("rural")
        self.assertIsInstance(items, list)
        self.assertIn("Hunting/fishing gear", items)
        self.assertIn("Animal traps", items)
        self.assertNotIn("Bolt cutters (for navigating locked areas)", items)

    def test_get_location_specific_items_unknown(self):
        items = get_location_specific_items("unknown_location")
        self.assertEqual(items, [])

    def test_generate_checklist_default(self):
        checklist = generate_checklist()
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), 10)
        self.assertIn("First aid kit", checklist)
        # Ensure no scenario/location specific items are present by default
        self.assertNotIn("Crowbar or blunt weapon (for close encounters)", checklist)
        self.assertNotIn("Bolt cutters (for navigating locked areas)", checklist)

    def test_generate_checklist_specific_scenario_and_location(self):
        checklist = generate_checklist(scenario="zombie", location="urban")
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), 20) # Base + zombie + urban items
        self.assertIn("First aid kit", checklist) # Base item
        self.assertIn("Crowbar or blunt weapon (for close encounters)", checklist) # Zombie item
        self.assertIn("Bolt cutters (for navigating locked areas)", checklist) # Urban item
        # Ensure no duplicates due to set conversion
        self.assertEqual(len(checklist), len(set(checklist)))

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_default_output(self, mock_parse_args, mock_stdout):
        # Mock rationale: We need to capture stdout to verify the script's output
        # without actually printing to the console during tests.
        # We also mock argparse to control the command-line arguments passed to main().
        mock_parse_args.return_value.scenario = "default"
        mock_parse_args.return_value.location = "default"

        main()
        output = mock_stdout.getvalue()

        self.assertIn("--- Apocalypse Preparedness Checklist ---", output)
        self.assertIn("Scenario: Default", output)
        self.assertIn("Location: Default", output)
        self.assertIn("1. Water (1 gallon per person per day for at least 3 days)", output)
        self.assertIn("Stay safe out there, survivor!", output)
        self.assertNotIn("Crowbar or blunt weapon", output) # Should not be in default

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_zombie_urban_output(self, mock_parse_args, mock_stdout):
        # Mock rationale: Same as above, capturing stdout and controlling argparse inputs.
        mock_parse_args.return_value.scenario = "zombie"
        mock_parse_args.return_value.location = "urban"

        main()
        output = mock_stdout.getvalue()

        self.assertIn("Scenario: Zombie", output)
        self.assertIn("Location: Urban", output)
        self.assertIn("Crowbar or blunt weapon (for close encounters)", output)
        self.assertIn("Bolt cutters (for navigating locked areas)", output)
        self.assertIn("First aid kit", output) # Base item should still be there
