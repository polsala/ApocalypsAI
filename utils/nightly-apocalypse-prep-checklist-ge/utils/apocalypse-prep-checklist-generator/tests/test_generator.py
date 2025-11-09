import unittest
from unittest.mock import patch
import sys
import io
from src.generator import generate_checklist, SCENARIOS, main

class TestApocalypseChecklistGenerator(unittest.TestCase):

    def test_generate_checklist_zombie(self):
        # Test that the 'zombie' scenario returns the correct checklist.
        # Mock rationale: No external dependencies, directly testing the function's output.
        checklist = generate_checklist("zombie")
        self.assertEqual(checklist, SCENARIOS["zombie"])
        self.assertGreater(len(checklist), 0)

    def test_generate_checklist_meteor(self):
        # Test that the 'meteor' scenario returns the correct checklist.
        # Mock rationale: No external dependencies, directly testing the function's output.
        checklist = generate_checklist("meteor")
        self.assertEqual(checklist, SCENARIOS["meteor"])
        self.assertGreater(len(checklist), 0)

    def test_generate_checklist_ai_uprising(self):
        # Test that the 'ai-uprising' scenario returns the correct checklist.
        # Mock rationale: No external dependencies, directly testing the function's output.
        checklist = generate_checklist("ai-uprising")
        self.assertEqual(checklist, SCENARIOS["ai-uprising"])
        self.assertGreater(len(checklist), 0)

    def test_generate_checklist_solar_flare(self):
        # Test that the 'solar-flare' scenario returns the correct checklist.
        # Mock rationale: No external dependencies, directly testing the function's output.
        checklist = generate_checklist("solar-flare")
        self.assertEqual(checklist, SCENARIOS["solar-flare"])
        self.assertGreater(len(checklist), 0)

    def test_generate_checklist_default(self):
        # Test that the 'default' scenario returns the correct checklist.
        # Mock rationale: No external dependencies, directly testing the function's output.
        checklist = generate_checklist("default")
        self.assertEqual(checklist, SCENARIOS["default"])
        self.assertGreater(len(checklist), 0)

    def test_generate_checklist_unknown_scenario(self):
        # Test that an unknown scenario falls back to the 'default' checklist.
        # Mock rationale: No external dependencies, directly testing the function's output.
        checklist = generate_checklist("unknown-doom")
        self.assertEqual(checklist, SCENARIOS["default"])

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['generator.py', '--scenario', 'zombie'])
    def test_main_cli_zombie_output(self, mock_stdout):
        # Test the main function's CLI output for the 'zombie' scenario.
        # Mock rationale: sys.stdout is mocked to capture printed output, and sys.argv is mocked
        # to simulate command-line arguments without actually modifying the global sys.argv.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Apocalypse Prep Checklist: Zombie Uprising", output)
        for item in SCENARIOS["zombie"]:
            self.assertIn(item, output)
        self.assertIn("Stay vigilant, survivor!", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['generator.py'])
    def test_main_cli_default_output(self, mock_stdout):
        # Test the main function's CLI output when no scenario is specified (should default).
        # Mock rationale: sys.stdout is mocked to capture printed output, and sys.argv is mocked
        # to simulate command-line arguments without actually modifying the global sys.argv.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Apocalypse Prep Checklist: Default", output)
        for item in SCENARIOS["default"]:
            self.assertIn(item, output)
        self.assertIn("Stay vigilant, survivor!", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['generator.py', '--scenario', 'nonexistent'])
    def test_main_cli_unknown_scenario_output(self, mock_stdout):
        # Test the main function's CLI output for an unknown scenario (should default).
        # Mock rationale: sys.stdout is mocked to capture printed output, and sys.argv is mocked
        # to simulate command-line arguments without actually modifying the global sys.argv.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Apocalypse Prep Checklist: Nonexistent", output) # Title will reflect input, but content is default
        for item in SCENARIOS["default"]:
            self.assertIn(item, output)
        self.assertIn("Stay vigilant, survivor!", output)

if __name__ == '__main__':
    unittest.main()
