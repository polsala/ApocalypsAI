import unittest
import os
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Mock rationale: We need to mock os.environ to control the environment variables
# for deterministic testing without affecting the actual system environment.
# We also mock sys.stdout to capture printed output for verification.
# The patch.dict(os.environ, {}, clear=True) is used during import to ensure
# a clean state for the module under test, preventing real environment variables
# from interfering with test setup.
with patch.dict(os.environ, {}, clear=True):
    from src.whisperer import get_env_vars, identify_sensitive_vars, main

class TestEnvVarWhisperer(unittest.TestCase):

    @patch.dict(os.environ, {'TEST_VAR_1': 'value1', 'ANOTHER_VAR': 'value2', 'TEST_SECRET_KEY': 'secret'}, clear=True)
    def test_get_env_vars_no_prefix(self):
        # Mock rationale: os.environ is mocked to provide a controlled set of environment variables.
        env_vars = get_env_vars()
        self.assertIn('TEST_VAR_1', env_vars)
        self.assertIn('ANOTHER_VAR', env_vars)
        self.assertIn('TEST_SECRET_KEY', env_vars)
        self.assertEqual(env_vars['TEST_VAR_1'], 'value1')

    @patch.dict(os.environ, {'TEST_VAR_1': 'value1', 'ANOTHER_VAR': 'value2', 'TEST_SECRET_KEY': 'secret'}, clear=True)
    def test_get_env_vars_with_prefix(self):
        # Mock rationale: os.environ is mocked to provide a controlled set of environment variables.
        env_vars = get_env_vars(prefix="TEST_")
        self.assertIn('TEST_VAR_1', env_vars)
        self.assertIn('TEST_SECRET_KEY', env_vars)
        self.assertNotIn('ANOTHER_VAR', env_vars)
        self.assertEqual(env_vars['TEST_VAR_1'], 'value1')

    def test_identify_sensitive_vars(self):
        env_vars = {
            'MY_API_KEY': 'abc',
            'REGULAR_VAR': 'def',
            'DB_PASSWORD': '123',
            'USER_TOKEN': 'xyz',
            'NON_SENSITIVE': 'data'
        }
        sensitive_keywords = ['KEY', 'PASSWORD', 'TOKEN']
        sensitive_status = identify_sensitive_vars(env_vars, sensitive_keywords)

        self.assertTrue(sensitive_status['MY_API_KEY'])
        self.assertFalse(sensitive_status['REGULAR_VAR'])
        self.assertTrue(sensitive_status['DB_PASSWORD'])
        self.assertTrue(sensitive_status['USER_TOKEN'])
        self.assertFalse(sensitive_status['NON_SENSITIVE'])

    def test_identify_sensitive_vars_case_insensitive(self):
        env_vars = {'my_secret_key': 'abc'}
        sensitive_keywords = ['key']
        sensitive_status = identify_sensitive_vars(env_vars, sensitive_keywords)
        self.assertTrue(sensitive_status['my_secret_key'])

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch.dict(os.environ, {'APP_KEY': 'app_secret', 'APP_NAME': 'my_app', 'OTHER_VAR': 'value'}, clear=True)
    def test_main_no_args(self, mock_parse_args, mock_stdout):
        # Mock rationale:
        # 1. sys.stdout is mocked to capture printed output for assertion.
        # 2. argparse.ArgumentParser.parse_args is mocked to control command-line arguments.
        # 3. os.environ is mocked to provide a controlled set of environment variables.
        mock_parse_args.return_value = MagicMock(prefix="", sensitive_keywords="KEY,TOKEN,PASSWORD,SECRET,API_KEY,AUTH")
        main()
        output = mock_stdout.getvalue()

        self.assertIn("🌌 Nightly Env-Var Whisperer 🌌", output)
        self.assertIn("APP_KEY: ***REDACTED*** (Sensitive? ✨)", output)
        self.assertIn("APP_NAME: my_app", output)
        self.assertIn("OTHER_VAR: value", output)
        self.assertNotIn("APP_KEY: app_secret", output) # Ensure redaction

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch.dict(os.environ, {'APP_KEY': 'app_secret', 'APP_NAME': 'my_app', 'OTHER_VAR': 'value'}, clear=True)
    def test_main_with_prefix(self, mock_parse_args, mock_stdout):
        # Mock rationale: Same as above, but testing prefix filtering.
        mock_parse_args.return_value = MagicMock(prefix="APP_", sensitive_keywords="KEY,TOKEN,PASSWORD,SECRET,API_KEY,AUTH")
        main()
        output = mock_stdout.getvalue()

        self.assertIn("APP_KEY: ***REDACTED*** (Sensitive? ✨)", output)
        self.assertIn("APP_NAME: my_app", output)
        self.assertNotIn("OTHER_VAR", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch.dict(os.environ, {'MY_VAR': 'val', 'MY_TOKEN': 'tok'}, clear=True)
    def test_main_custom_sensitive_keywords(self, mock_parse_args, mock_stdout):
        # Mock rationale: Same as above, but testing custom sensitive keywords.
        mock_parse_args.return_value = MagicMock(prefix="", sensitive_keywords="TOKEN")
        main()
        output = mock_stdout.getvalue()

        self.assertIn("MY_VAR: val", output)
        self.assertIn("MY_TOKEN: ***REDACTED*** (Sensitive? ✨)", output)
        self.assertNotIn("MY_VAR: ***REDACTED***", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch.dict(os.environ, {}, clear=True) # Empty environment
    def test_main_no_env_vars(self, mock_parse_args, mock_stdout):
        # Mock rationale: Testing an empty environment scenario.
        mock_parse_args.return_value = MagicMock(prefix="", sensitive_keywords="KEY")
        main()
        output = mock_stdout.getvalue()
        self.assertIn("No environment variables found matching the criteria.", output)

if __name__ == '__main__':
    unittest.main()
