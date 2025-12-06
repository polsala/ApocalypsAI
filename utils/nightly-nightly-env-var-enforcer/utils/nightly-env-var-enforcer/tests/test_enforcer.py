import unittest
import os
from unittest.mock import patch, MagicMock
import sys

# Adjust sys.path to allow importing from the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from enforcer import check_env_vars, main
sys.path.pop(0) # Clean up sys.path

class TestEnvVarEnforcer(unittest.TestCase):

    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_all_vars_present_and_non_empty(self, mock_print):
        # Mock rationale: Simulate os.environ for deterministic testing without affecting actual environment.
        with patch.dict(os.environ, {'VAR1': 'value1', 'VAR2': 'value2'}, clear=True):
            result = check_env_vars('VAR1,VAR2')
            self.assertTrue(result)
            mock_print.assert_any_call("✅ PRESENT: Environment variable 'VAR1' is set and non-empty.")
            mock_print.assert_any_call("✅ PRESENT: Environment variable 'VAR2' is set and non-empty.")
            mock_print.assert_any_call("All required environment variables are present and non-empty. Good to go!")

    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_some_vars_missing(self, mock_print):
        # Mock rationale: Simulate os.environ for deterministic testing without affecting actual environment.
        with patch.dict(os.environ, {'VAR1': 'value1'}, clear=True):
            result = check_env_vars('VAR1,VAR2')
            self.assertFalse(result)
            mock_print.assert_any_call("✅ PRESENT: Environment variable 'VAR1' is set and non-empty.")
            mock_print.assert_any_call("❌ MISSING: Environment variable 'VAR2' is not set.")
            mock_print.assert_any_call("Some required environment variables are missing or empty. Please address them.")

    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_some_vars_empty(self, mock_print):
        # Mock rationale: Simulate os.environ for deterministic testing without affecting actual environment.
        with patch.dict(os.environ, {'VAR1': 'value1', 'VAR2': ''}, clear=True):
            result = check_env_vars('VAR1,VAR2')
            self.assertFalse(result)
            mock_print.assert_any_call("✅ PRESENT: Environment variable 'VAR1' is set and non-empty.")
            mock_print.assert_any_call("⚠️ EMPTY: Environment variable 'VAR2' is set but empty.")
            mock_print.assert_any_call("Some required environment variables are missing or empty. Please address them.")

    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    def test_no_required_vars_specified(self, mock_print):
        # Mock rationale: Simulate os.environ for deterministic testing without affecting actual environment.
        with patch.dict(os.environ, {'VAR1': 'value1'}, clear=True):
            result = check_env_vars('')
            self.assertTrue(result)
            mock_print.assert_any_call("No required environment variables specified.")
            mock_print.assert_any_call("All required environment variables are present and non-empty. Good to go!")

    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    @patch('sys.exit') # Mock rationale: Prevent actual system exit during test.
    @patch('sys.argv', ['enforcer.py', 'VAR1,VAR2']) # Mock rationale: Simulate command-line arguments.
    def test_main_success(self, mock_exit, mock_print):
        # Mock rationale: Simulate os.environ for deterministic testing without affecting actual environment.
        with patch.dict(os.environ, {'VAR1': 'value1', 'VAR2': 'value2'}, clear=True):
            main()
            mock_exit.assert_not_called() # Should not exit on success
            mock_print.assert_any_call("All required environment variables are present and non-empty. Good to go!")

    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    @patch('sys.exit') # Mock rationale: Prevent actual system exit during test.
    @patch('sys.argv', ['enforcer.py', 'VAR1,VAR2']) # Mock rationale: Simulate command-line arguments.
    def test_main_failure(self, mock_exit, mock_print):
        # Mock rationale: Simulate os.environ for deterministic testing without affecting actual environment.
        with patch.dict(os.environ, {'VAR1': 'value1'}, clear=True):
            main()
            mock_exit.assert_called_once_with(1) # Should exit with 1 on failure
            mock_print.assert_any_call("Some required environment variables are missing or empty. Please address them.")

    @patch('builtins.print') # Mock rationale: Capture print output for verification.
    @patch('sys.exit') # Mock rationale: Prevent actual system exit during test.
    @patch('sys.argv', ['enforcer.py']) # Mock rationale: Simulate command-line arguments.
    def test_main_no_args(self, mock_exit, mock_print):
        main()
        mock_exit.assert_called_once_with(1) # Should exit with 1 for incorrect usage
        mock_print.assert_any_call("Usage: python enforcer.py <comma_separated_required_env_vars>")

if __name__ == '__main__':
    unittest.main()
