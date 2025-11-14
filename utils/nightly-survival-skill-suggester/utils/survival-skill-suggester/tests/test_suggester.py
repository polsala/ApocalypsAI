import unittest
from unittest.mock import patch, MagicMock
import sys
import io
from src.suggester import get_skill_suggestion, main, SKILLS_DATABASE

class TestSurvivalSkillSuggester(unittest.TestCase):

    def test_get_skill_suggestion_valid_main_keyword(self):
        # Test with a direct main keyword
        suggestion = get_skill_suggestion("water")
        self.assertIsNotNone(suggestion)
        self.assertEqual(suggestion["skill"], "Water Purification")
        self.assertIn("filter", suggestion["description"])

    def test_get_skill_suggestion_valid_secondary_keyword(self):
        # Test with a secondary keyword
        suggestion = get_skill_suggestion("hydration")
        self.assertIsNotNone(suggestion)
        self.assertEqual(suggestion["skill"], "Water Purification")

    def test_get_skill_suggestion_case_insensitivity(self):
        # Test case insensitivity
        suggestion = get_skill_suggestion("FoOd")
        self.assertIsNotNone(suggestion)
        self.assertEqual(suggestion["skill"], "Foraging & Edible Plant Identification")

    def test_get_skill_suggestion_unknown_keyword(self):
        # Test with an unknown keyword
        suggestion = get_skill_suggestion("zombies")
        self.assertIsNone(suggestion)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_valid_keyword(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: We need to simulate command-line arguments without actually
        # running the script from the command line. `argparse.ArgumentParser.parse_args`
        # is mocked to return a Namespace object with the desired keyword.
        # `sys.stdout` is mocked to capture printed output for assertion.
        # `sys.exit` is mocked to prevent the test runner from terminating when `main` calls it.
        mock_parse_args.return_value = MagicMock(keyword="shelter")
        mock_exit.side_effect = SystemExit # Allow SystemExit to be caught, but not actually exit

        try:
            main()
        except SystemExit as e:
            self.fail(f"main() unexpectedly called sys.exit() for a valid keyword: {e}")

        output = mock_stdout.getvalue()
        self.assertIn("Skill: Improvised Shelter Construction", output)
        self.assertIn("Description: Master the art of building temporary shelters", output)
        mock_exit.assert_not_called() # Ensure sys.exit was not called for a valid keyword

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_unknown_keyword(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: Similar to the valid keyword test, we mock `parse_args`
        # to simulate an unknown keyword. `sys.stdout` captures output, and `sys.exit`
        # is mocked to verify it's called with the correct error code.
        mock_parse_args.return_value = MagicMock(keyword="aliens")
        mock_exit.side_effect = SystemExit # Allow SystemExit to be caught

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1) # Expect exit code 1 for unknown keyword

        output = mock_stdout.getvalue()
        self.assertIn("No specific skill found for 'aliens'.", output)
        mock_exit.assert_called_once_with(1) # Ensure sys.exit was called with 1

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_no_keyword_argument(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        # Mock rationale: We simulate the scenario where no keyword is provided to the CLI.
        # `parse_args` is mocked to raise an error that argparse would normally raise,
        # and `sys.exit` is mocked to ensure the program exits as expected for invalid arguments.
        mock_parse_args.side_effect = SystemExit(2) # argparse exits with 2 for invalid args

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2) # Expect exit code 2 for argparse error

        # Argparse prints usage to stderr by default for argument errors
        # We don't need to check stdout for this specific case, but stderr might contain usage info.
        # For simplicity, just checking the exit code is sufficient here.
        mock_exit.assert_called_once_with(2)
