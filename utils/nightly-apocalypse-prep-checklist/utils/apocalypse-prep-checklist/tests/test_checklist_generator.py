import unittest
from unittest.mock import patch
import sys
import io
from src.checklist_generator import ChecklistGenerator, main

class TestChecklistGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = ChecklistGenerator()

    def test_base_items_present(self):
        checklist = self.generator.generate_checklist("general")
        self.assertIn("Water (1 gallon per person per day for 3 days)", checklist)
        self.assertIn("First aid kit", checklist)
        self.assertGreater(len(checklist), 10) # Ensure a reasonable number of base items

    def test_zombie_scenario_items(self):
        checklist = self.generator.generate_checklist("zombie")
        self.assertIn("Crowbar or other blunt weapon", checklist)
        self.assertIn("Heavy-duty boots", checklist)
        self.assertIn("Water (1 gallon per person per day for 3 days)", checklist) # Base item should still be there
        self.assertGreater(len(checklist), len(self.generator.base_items)) # Should have more than just base items

    def test_meteor_scenario_items(self):
        checklist = self.generator.generate_checklist("meteor")
        self.assertIn("Radiation suit (if impact is nuclear)", checklist)
        self.assertIn("Water purification tablets/filter", checklist)
        self.assertIn("First aid kit", checklist) # Base item should still be there

    def test_ai_uprising_scenario_items(self):
        checklist = self.generator.generate_checklist("ai-uprising")
        self.assertIn("EMP-shielded Faraday cage for electronics", checklist)
        self.assertIn("Analog communication devices (ham radio, signal mirror)", checklist)
        self.assertIn("Non-digital maps and compass", checklist)

    def test_unknown_scenario_defaults_to_base(self):
        checklist = self.generator.generate_checklist("unknown-apocalypse")
        self.assertEqual(len(checklist), len(self.generator.base_items)) # Should only contain base items
        self.assertIn("Water (1 gallon per person per day for 3 days)", checklist)
        self.assertNotIn("Crowbar or other blunt weapon", checklist) # Specific item should not be there

    def test_duplicate_items_are_removed(self):
        # If a base item is accidentally added to a scenario list, it should only appear once.
        # This is handled by `set()` in the generate_checklist method.
        # Let's temporarily modify the generator to simulate a duplicate.
        original_specific_items = self.generator.scenario_specific_items.copy()
        self.generator.scenario_specific_items["test-duplicate"] = ["First aid kit", "Crowbar or other blunt weapon"]
        
        checklist = self.generator.generate_checklist("test-duplicate")
        
        # Count occurrences of "First aid kit"
        self.assertEqual(checklist.count("First aid kit"), 1)
        self.assertIn("Crowbar or other blunt weapon", checklist)
        
        # Restore original
        self.generator.scenario_specific_items = original_specific_items

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_output_general(self, mock_parse_args, mock_stdout):
        # Mock rationale: We need to capture stdout to verify the script's output
        # and mock argparse to control the input arguments without actually parsing CLI args.
        mock_parse_args.return_value.scenario = "general"
        main()
        output = mock_stdout.getvalue()
        self.assertIn("--- Apocalypse Survival Checklist for: General ---", output)
        self.assertIn("1. Battery-powered or hand-crank radio", output) # Check for a specific base item
        self.assertNotIn("Crowbar or other blunt weapon", output) # Ensure no specific items for general

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_output_zombie(self, mock_parse_args, mock_stdout):
        # Mock rationale: Same as above, capturing stdout and mocking argparse.
        mock_parse_args.return_value.scenario = "zombie"
        main()
        output = mock_stdout.getvalue()
        self.assertIn("--- Apocalypse Survival Checklist for: Zombie ---", output)
        self.assertIn("Crowbar or other blunt weapon", output) # Check for a specific zombie item
        self.assertIn("Water (1 gallon per person per day for 3 days)", output) # Check for a base item

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_output_default_scenario(self, mock_parse_args, mock_stdout):
        # Mock rationale: Test the default behavior when no scenario is provided.
        mock_parse_args.return_value.scenario = "general" # argparse default
        main()
        output = mock_stdout.getvalue()
        self.assertIn("--- Apocalypse Survival Checklist for: General ---", output)
        self.assertIn("First aid kit", output)
        self.assertNotIn("EMP-shielded Faraday cage for electronics", output)
