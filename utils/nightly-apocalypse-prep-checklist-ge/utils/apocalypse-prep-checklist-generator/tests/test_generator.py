import unittest
from unittest.mock import patch
import io
import sys
import argparse
from src.generator import generate_checklist, main

class TestApocalypseChecklistGenerator(unittest.TestCase):

    def test_generate_checklist_zombie_urban_first_aid(self):
        # Test a specific scenario, location, and skill combination
        scenario = "zombie"
        location = "urban"
        skills = ["first_aid"]
        checklist = generate_checklist(scenario, location, skills);

        self.assertIn("--- Apocalypse Preparedness Checklist ---", checklist)
        self.assertIn("Scenario: Zombie", checklist)
        self.assertIn("Location: Urban", checklist)
        self.assertIn("Skills: First Aid", checklist)

        # General items
        self.assertIn("- Secure a reliable, off-grid power source.", checklist)

        # Zombie specifics
        self.assertIn("[Zombie Specifics]", checklist)
        self.assertIn("- Barricade entry points and secure your perimeter.", checklist)
        self.assertIn("- Master the art of the headshot (practice on mannequins, not neighbors).", checklist)

        # Urban specifics
        self.assertIn("[Urban Location Specifics]", checklist)
        self.assertIn("- Map out multiple escape routes from your current location.", checklist)
        self.assertIn("- Identify hidden caches of resources (abandoned stores, utility tunnels).", checklist)

        # First Aid specifics
        self.assertIn("[First Aid Skill Enhancements]", checklist)
        self.assertIn("- Assemble a comprehensive medical kit and learn advanced wound care.", checklist)
        self.assertIn("- Practice basic surgical procedures (on non-living subjects, ideally).", checklist)

        self.assertIn("--- End of Checklist ---", checklist)

    def test_generate_checklist_meteor_rural_survivalist_coding(self):
        # Test another combination with multiple skills
        scenario = "meteor"
        location = "rural"
        skills = ["survivalist", "coding"]
        checklist = generate_checklist(scenario, location, skills);

        self.assertIn("Scenario: Meteor", checklist)
        self.assertIn("Location: Rural", checklist)
        self.assertIn("Skills: Survivalist, Coding", checklist)

        # Meteor specifics
        self.assertIn("[Meteor Specifics]", checklist)
        self.assertIn("- Identify or construct a sturdy underground shelter.", checklist)
        self.assertIn("- Prepare for long-term isolation and radiation fallout.", checklist)

        # Rural specifics
        self.assertIn("[Rural Location Specifics]", checklist)
        self.assertIn("- Learn foraging, hunting, and trapping techniques.", checklist)
        self.assertIn("- Master basic shelter construction from natural materials.", checklist)

        # Survivalist specifics
        self.assertIn("[Survivalist Skill Enhancements]", checklist)
        self.assertIn("- Refine advanced navigation techniques (map, compass, stars).", checklist)
        self.assertIn("- Learn to identify edible and medicinal plants.", checklist)

        # Coding specifics
        self.assertIn("[Coding Skill Enhancements]", checklist)
        self.assertIn("- Develop offline tools for data analysis and communication.", checklist)
        self.assertIn("- Secure your own digital footprint and create ghost identities.", checklist)

    def test_generate_checklist_ai_bunker_no_skills(self):
        # Test a scenario with no skills
        scenario = "ai_uprising"
        location = "bunker"
        skills = []
        checklist = generate_checklist(scenario, location, skills);

        self.assertIn("Scenario: AI Uprising", checklist)
        self.assertIn("Location: Bunker", checklist)
        self.assertIn("Skills: None", checklist) # Check for 'None' when no skills

        # AI Uprising specifics
        self.assertIn("[AI Uprising Specifics]", checklist)
        self.assertIn("- Construct a Faraday cage for sensitive electronics.", checklist)
        self.assertIn("- Learn basic social engineering to bypass AI-controlled systems.", checklist)

        # Bunker specifics
        self.assertIn("[Bunker Location Specifics]", checklist)
        self.assertIn("- Ensure air filtration and ventilation systems are operational.", checklist)
        self.assertIn("- Cultivate psychological resilience for long-term isolation.", checklist)

        # Ensure no skill sections are present
        self.assertNotIn("[First Aid Skill Enhancements]", checklist)
        self.assertNotIn("[Coding Skill Enhancements]", checklist)
        self.assertNotIn("[Survivalist Skill Enhancements]", checklist)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function_output(self, mock_parse_args, mock_stdout):
        # Mock rationale: We need to simulate command-line arguments and capture stdout.
        # `argparse.ArgumentParser.parse_args` is mocked to provide specific arguments
        # without actually parsing `sys.argv`. `sys.stdout` is mocked to capture
        # the printed output for assertion.
        mock_parse_args.return_value = argparse.Namespace(
            scenario="zombie",
            location="urban",
            skills=["first_aid"]
        )

        main()
        output = mock_stdout.getvalue()

        self.assertIn("--- Apocalypse Preparedness Checklist ---", output)
        self.assertIn("Scenario: Zombie", output)
        self.assertIn("Location: Urban", output)
        self.assertIn("Skills: First Aid", output)
        self.assertIn("- Barricade entry points and secure your perimeter.", output)
        self.assertIn("- Assemble a comprehensive medical kit and learn advanced wound care.", output)
        self.assertIn("--- End of Checklist ---", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.stderr', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser._print_message') # Mock rationale: Prevent argparse from printing help/usage to stderr
    @patch('sys.exit') # Mock rationale: Prevent sys.exit from terminating the test runner
    def test_main_function_invalid_args(self, mock_exit, mock_print_message, mock_stderr, mock_stdout):
        # Mock rationale: We need to simulate invalid command-line arguments and capture
        # the error output. `argparse.ArgumentParser.parse_args` is implicitly called
        # by `main()` and will raise an error for invalid choices. We mock `sys.exit`
        # to prevent the test from terminating and `_print_message` to avoid
        # polluting test output with argparse's help message.
        with self.assertRaises(SystemExit): # argparse raises SystemExit on invalid args
            # Simulate invalid scenario
            sys.argv = ['generator.py', '--scenario', 'invalid_scenario', '--location', 'urban']
            main()
        
        # Check that sys.exit was called with an error code
        mock_exit.assert_called_with(2) # argparse exits with 2 for invalid arguments

        # Reset sys.argv for other tests if needed, though patch should handle it.
        # For this specific test, we're just checking the SystemExit.

if __name__ == '__main__':
    unittest.main()
