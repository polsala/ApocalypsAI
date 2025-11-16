import unittest
import sys
from io import StringIO
from unittest.mock import patch
import argparse
from src.scribe import list_skills, get_skill_details, search_skills, main, SKILLS_DATA

class TestScribe(unittest.TestCase):

    def setUp(self):
        # Mock rationale: Capture stdout to assert printed output without affecting the console.
        self.held_stdout = sys.stdout
        sys.stdout = self.mock_stdout = StringIO()

    def tearDown(self):
        sys.stdout = self.held_stdout

    def test_list_skills(self):
        list_skills()
        output = self.mock_stdout.getvalue()
        self.assertIn("Available Survival Skills:", output)
        self.assertIn("- Water Purification (water_purification)", output)
        self.assertIn("- Basic First Aid (basic_first_aid)", output)
        self.assertIn("- Fire Starting (fire_starting)", output)

    def test_get_skill_details_existing(self):
        exit_code = get_skill_details("water_purification")
        output = self.mock_stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("--- Water Purification ---", output)
        self.assertIn("Ensuring safe drinking water is paramount", output)
        self.assertIn("1. Filter large debris", output)
        self.assertIn("Keywords: water, purify, drink, hydration", output)

    def test_get_skill_details_non_existing(self):
        exit_code = get_skill_details("non_existent_skill")
        output = self.mock_stdout.getvalue()
        self.assertEqual(exit_code, 1)
        self.assertIn("Error: Skill 'non_existent_skill' not found.", output)

    def test_search_skills_by_keyword(self):
        exit_code = search_skills("water")
        output = self.mock_stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("Skills matching 'water':", output)
        self.assertIn("- Water Purification", output)
        self.assertNotIn("- Basic First Aid", output)

    def test_search_skills_by_title(self):
        exit_code = search_skills("first aid")
        output = self.mock_stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("Skills matching 'first aid':", output)
        self.assertIn("- Basic First Aid", output)

    def test_search_skills_no_match(self):
        exit_code = search_skills("zombie")
        output = self.mock_stdout.getvalue()
        self.assertEqual(exit_code, 1)
        self.assertIn("No skills found matching 'zombie'.", output)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_list_action(self, mock_exit, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(action='list', skill_key_or_query=None)
        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("Available Survival Skills:", output)
        mock_exit.assert_not_called() # list action doesn't exit

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_get_action_existing(self, mock_exit, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(action='get', skill_key_or_query='fire_starting')
        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("--- Fire Starting ---", output)
        mock_exit.assert_called_once_with(0)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_get_action_non_existing(self, mock_exit, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(action='get', skill_key_or_query='unknown_skill')
        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("Error: Skill 'unknown_skill' not found.", output)
        mock_exit.assert_called_once_with(1)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit') # Mock rationale: Prevent argparse from calling sys.exit directly on error.
    @patch('argparse.ArgumentParser.error') # Mock rationale: Prevent argparse from calling sys.exit directly on error.
    def test_main_get_action_no_key(self, mock_error, mock_exit, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(action='get', skill_key_or_query=None)
        main()
        mock_error.assert_called_once_with("The 'get' action requires a skill key.")
        mock_exit.assert_not_called() # argparse.error usually exits, but we mock it.

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_search_action_found(self, mock_exit, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(action='search', skill_key_or_query='aid')
        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("Skills matching 'aid':", output)
        self.assertIn("- Basic First Aid", output)
        mock_exit.assert_called_once_with(0)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    def test_main_search_action_not_found(self, mock_exit, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(action='search', skill_key_or_query='shelter')
        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("No skills found matching 'shelter'.", output)
        mock_exit.assert_called_once_with(1)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner.
    @patch('argparse.ArgumentParser.error') # Mock rationale: Prevent argparse from calling sys.exit directly on error.
    def test_main_search_action_no_query(self, mock_error, mock_exit, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(action='search', skill_key_or_query=None)
        main()
        mock_error.assert_called_once_with("The 'search' action requires a search query.")
        mock_exit.assert_not_called() # argparse.error usually exits, but we mock it.
