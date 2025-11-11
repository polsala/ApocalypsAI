import unittest
import sys
import os
from unittest.mock import patch
from io import StringIO

# Mock rationale: This allows the test script to import the module under test
# as if it were a standard Python module, without needing to install it or
# rely on the system's PYTHONPATH being pre-configured. It ensures the test
# is self-contained and can locate the source file relative to its own location.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from checklist_generator import generate_checklist, SCENARIOS, main

class TestChecklistGenerator(unittest.TestCase):

    def test_generate_checklist_zombie(self):
        # Test a known scenario
        checklist = generate_checklist("zombie")
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), 0)
        self.assertEqual(checklist[0], "Secure a safe house with multiple exits.")
        self.assertEqual(checklist, SCENARIOS["zombie"])

    def test_generate_checklist_meteor(self):
        # Test another known scenario
        checklist = generate_checklist("meteor")
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), 0)
        self.assertEqual(checklist[0], "Prepare an underground shelter or reinforced basement.")
        self.assertEqual(checklist, SCENARIOS["meteor"])

    def test_generate_checklist_ai_uprising(self):
        # Test another known scenario
        checklist = generate_checklist("ai-uprising")
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), 0)
        self.assertEqual(checklist[0], "Unplug all non-essential smart devices.")
        self.assertEqual(checklist, SCENARIOS["ai-uprising"])

    def test_generate_checklist_solar_flare(self):
        # Test another known scenario
        checklist = generate_checklist("solar-flare")
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), 0)
        self.assertEqual(checklist[0], "Prepare for widespread power grid failure (EMP-resistant electronics).")
        self.assertEqual(checklist, SCENARIOS["solar-flare"])

    def test_generate_checklist_general(self):
        # Test the default scenario
        checklist = generate_checklist("general")
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), 0)
        self.assertEqual(checklist[0], "Assemble a 72-hour emergency kit (Go-Bag).")
        self.assertEqual(checklist, SCENARIOS["general"])

    def test_generate_checklist_unknown_scenario(self):
        # Test an unknown scenario, should return an empty list
        checklist = generate_checklist("alien-invasion")
        self.assertIsInstance(checklist, list)
        self.assertEqual(len(checklist), 0)
        self.assertEqual(checklist, [])

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['checklist_generator.py', '--scenario', 'zombie'])
    def test_main_zombie_output(self, mock_stdout):
        # Mock rationale: We need to capture stdout to verify the printed output
        # and mock sys.argv to simulate command-line arguments without actually
        # modifying the global sys.argv during the test run.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("--- Apocalypse Prep Checklist: Zombie Outbreak ---", output)
        self.assertIn("1. Secure a safe house with multiple exits.", output)
        self.assertIn("7. Establish a rendezvous point with trusted allies.", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['checklist_generator.py'])
    def test_main_default_output(self, mock_stdout):
        # Mock rationale: Same as above, for default scenario.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("--- Apocalypse Prep Checklist: General ---", output)
        self.assertIn("1. Assemble a 72-hour emergency kit (Go-Bag).", output)
        self.assertIn("7. Ensure you have multiple ways to get news and weather alerts.", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.exit')
    @patch('sys.argv', ['checklist_generator.py', '--scenario', 'unknown-doom'])
    def test_main_unknown_scenario_error(self, mock_exit, mock_stderr, mock_stdout):
        # Mock rationale: We need to capture stderr for error messages and
        # mock sys.exit to prevent the test runner from exiting prematurely.
        main()
        err_output = mock_stderr.getvalue()
        self.assertIn("Error: Unknown scenario 'unknown-doom'.", err_output)
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
