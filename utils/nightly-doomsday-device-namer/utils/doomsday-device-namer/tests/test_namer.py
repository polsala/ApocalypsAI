import unittest
from unittest.mock import patch
import sys
import os
import io

# Add the src directory to the Python path to allow importing namer.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import namer after path modification
import namer

class TestDoomsdayDeviceNamer(unittest.TestCase):

    def test_approved_name(self):
        # Test a name that should pass all rules
        name = "The Omega Annihilation-X Prime"
        result = namer.validate_name(name)
        self.assertTrue(result["approved"], f"'{name}' should be approved but failed: {result['violations']}")
        self.assertEqual(len(result["violations"]), 0)

    def test_name_too_short(self):
        # Test name violating length rule (too short)
        name = "Void-X"
        result = namer.validate_name(name)
        self.assertFalse(result["approved"])
        self.assertIn("Length (must be between 10 and 30 characters)", result["violations"])

    def test_name_too_long(self):
        # Test name violating length rule (too long)
        name = "The Grand Cataclysmic Oblivion Annihilation-X Prime Unit"
        result = namer.validate_name(name)
        self.assertFalse(result["approved"])
        self.assertIn("Length (must be between 10 and 30 characters)", result["violations"])

    def test_missing_ominous_keyword(self):
        # Test name missing an ominous keyword
        name = "The Grand Machine-X Prime"
        result = namer.validate_name(name)
        self.assertFalse(result["approved"])
        self.assertIn("Ominous Keywords (missing at least one)", result["violations"])

    def test_contains_forbidden_keyword(self):
        # Test name containing a forbidden keyword
        name = "The Happy Annihilation-X Prime"
        result = namer.validate_name(name)
        self.assertFalse(result["approved"])
        self.assertIn("Forbidden Keywords (contains 'happy')", result["violations"])

    def test_not_enough_hard_consonants(self):
        # Test name with insufficient distinct hard consonants (only 'D' and 'M' are hard here, 'T' is not)
        name = "The Doom Annihilator-Prime"
        result = namer.validate_name(name)
        self.assertFalse(result["approved"])
        self.assertIn("Hard Consonants (missing at least two distinct ones)", result["violations"])

    def test_missing_approved_suffix(self):
        # Test name not ending with an approved suffix
        name = "The Omega Annihilation-X Core"
        result = namer.validate_name(name)
        self.assertFalse(result["approved"])
        self.assertIn("Approved Suffix (must end with one of: inator, tron, ex, prime, unit, doom, strike)", result["violations"])

    def test_case_insensitivity(self):
        # Test case insensitivity for keywords and suffixes
        name = "the OMEGA annihilation-x PRIME"
        result = namer.validate_name(name)
        self.assertTrue(result["approved"], f"'{name}' should be approved but failed: {result['violations']}")

    def test_multiple_violations(self):
        # Test a name with multiple violations
        name = "Fluffy Sparkletron"
        result = namer.validate_name(name)
        self.assertFalse(result["approved"])
        self.assertIn("Length (must be between 10 and 30 characters)", result["violations"])
        self.assertIn("Ominous Keywords (missing at least one)", result["violations"])
        self.assertIn("Forbidden Keywords (contains 'fluffy')", result["violations"])
        self.assertIn("Hard Consonants (missing at least two distinct ones)", result["violations"])
        # 'Sparkletron' ends with 'tron', so suffix rule should pass.
        self.assertNotIn("Approved Suffix", result["violations"])

    def test_main_script_approved_output(self):
        # Mock rationale: Capture stdout and sys.exit to verify the CLI's output and exit code for an approved name.
        # This tests the `run_cli` function's behavior without actually modifying global state or exiting the test runner.
        test_name = "The Omega Annihilation-X Prime"
        expected_output = f"Name '{test_name}' is Approved for Global Domination!\n"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout,
             patch('sys.exit') as mock_exit:
            exit_code = namer.run_cli(['namer.py', test_name])
            self.assertEqual(exit_code, 0)
            self.assertEqual(mock_stdout.getvalue(), expected_output)
            mock_exit.assert_not_called() # sys.exit should not be called if run_cli returns 0

    def test_main_script_rejected_output(self):
        # Mock rationale: Capture stdout and sys.exit to verify the CLI's output and exit code for a rejected name.
        # This tests the `run_cli` function's behavior without actually modifying global state or exiting the test runner.
        test_name = "Fluffy Sparkletron"
        expected_output_start = f"Name '{test_name}' is NOT approved.\n"
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout,
             patch('sys.exit') as mock_exit:
            exit_code = namer.run_cli(['namer.py', test_name])
            self.assertEqual(exit_code, 1)
            self.assertTrue(mock_stdout.getvalue().startswith(expected_output_start))
            self.assertIn("- Rule Violation: Length", mock_stdout.getvalue())
            self.assertIn("- Rule Violation: Ominous Keywords", mock_stdout.getvalue())
            self.assertIn("- Rule Violation: Forbidden Keywords (contains 'fluffy')", mock_stdout.getvalue())
            self.assertIn("- Rule Violation: Hard Consonants", mock_stdout.getvalue())
            mock_exit.assert_not_called() # sys.exit should not be called if run_cli returns 1

    def test_main_script_no_args(self):
        # Mock rationale: Capture stdout and sys.exit to verify the CLI's output and exit code when no arguments are provided.
        # This tests the `run_cli` function's behavior without actually modifying global state or exiting the test runner.
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout,
             patch('sys.exit') as mock_exit:
            exit_code = namer.run_cli(['namer.py'])
            self.assertEqual(exit_code, 1)
            self.assertEqual(mock_stdout.getvalue(), "Usage: python src/namer.py \"Your Proposed Doomsday Name\"\n")
            mock_exit.assert_not_called()
