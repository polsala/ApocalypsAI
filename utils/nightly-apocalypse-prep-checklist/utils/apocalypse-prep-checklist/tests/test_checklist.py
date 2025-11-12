import unittest
import sys
import io
from unittest.mock import patch

# Mock rationale: We need to capture stdout to verify the script's output
# without actually printing to the console during tests. Patching sys.stdout
# allows us to redirect print statements to an in-memory buffer.

# Mock rationale: We need to simulate command-line arguments for the main()
# function without actually running the script from the command line. Patching
# sys.argv allows us to inject arguments programmatically.

# Mock rationale: We want to test the main function's behavior when an invalid
# scenario is provided, which includes exiting with a specific status code.
# Patching sys.exit prevents the test runner from terminating prematurely.

from src.checklist import main, get_checklist

class TestApocalypsePrepChecklist(unittest.TestCase):

    def setUp(self):
        # Capture stdout for all tests
        self.held_stdout = sys.stdout
        self.mock_stdout = io.StringIO()
        sys.stdout = self.mock_stdout

    def tearDown(self):
        # Restore stdout after all tests
        sys.stdout = self.held_stdout

    def test_get_checklist_zombie(self):
        checklist = get_checklist("zombie")
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), 0)
        self.assertIn("Secure a safe location (high ground, defensible structure)", checklist)

    def test_get_checklist_ai_uprising(self):
        checklist = get_checklist("ai-uprising")
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), 0)
        self.assertIn("Build an EMP-proof Faraday cage for essential electronics", checklist)

    def test_get_checklist_meteor_strike(self):
        checklist = get_checklist("meteor-strike")
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), 0)
        self.assertIn("Identify or construct an underground shelter", checklist)

    def test_get_checklist_solar_flare(self):
        checklist = get_checklist("solar-flare")
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), 0)
        self.assertIn("Build an EMP-proof Faraday cage for essential electronics", checklist)

    def test_get_checklist_general(self):
        checklist = get_checklist("general")
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), 0)
        self.assertIn("Stockpile non-perishable food and water (72-hour supply minimum)", checklist)

    def test_get_checklist_unknown_scenario(self):
        checklist = get_checklist("unknown-doom")
        self.assertEqual(checklist, [])

    @patch('sys.argv', ['checklist.py', '--scenario', 'zombie'])
    def test_main_zombie_scenario_output(self):
        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("--- Apocalypse Prep Checklist: Zombie ---", output)
        self.assertIn("1. [ ] Secure a safe location (high ground, defensible structure)", output)
        self.assertIn("8. [ ] Learn basic survival skills (fire starting, knot tying)", output)

    @patch('sys.argv', ['checklist.py', '--scenario', 'general'])
    def test_main_general_scenario_output(self):
        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("--- Apocalypse Prep Checklist: General ---", output)
        self.assertIn("1. [ ] Stockpile non-perishable food and water (72-hour supply minimum)", output)
        self.assertIn("8. [ ] Know your local emergency services and evacuation routes", output)

    @patch('sys.argv', ['checklist.py', '--scenario', 'invalid-scenario'])
    @patch('sys.exit', side_effect=SystemExit) # Mock rationale: Prevent actual exit
    def test_main_invalid_scenario_exits_with_error(self, mock_exit):
        with self.assertRaises(SystemExit):
            main()
        mock_exit.assert_called_with(1)
        output = self.mock_stdout.getvalue()
        self.assertIn("Error: Unknown scenario 'invalid-scenario'.", output)

    @patch('sys.argv', ['checklist.py']) # No scenario argument
    @patch('sys.stderr', new_callable=io.StringIO) # Capture stderr for argparse error
    @patch('sys.exit', side_effect=SystemExit)
    def test_main_no_scenario_argument_exits_with_error(self, mock_exit, mock_stderr):
        with self.assertRaises(SystemExit):
            main()
        mock_exit.assert_called_with(2) # argparse exits with 2 for argument errors
        error_output = mock_stderr.getvalue()
        self.assertIn("the following arguments are required: --scenario", error_output)

if __name__ == '__main__':
    unittest.main()
