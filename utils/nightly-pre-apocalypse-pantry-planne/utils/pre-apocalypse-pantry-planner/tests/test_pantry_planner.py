import unittest
from unittest.mock import patch
import sys
from io import StringIO

# Adjust path to import the module from src
sys.path.insert(0, 'utils/pre-apocalypse-pantry-planner/src')
from pantry_planner import calculate_supplies, main
sys.path.pop(0)

class TestPantryPlanner(unittest.TestCase):

    def test_calculate_supplies_basic(self):
        # Test with a simple, common scenario
        # Mock rationale: Testing the core calculation logic with known inputs.
        supplies = calculate_supplies(num_people=2, duration_days=7)
        self.assertIsInstance(supplies, dict)
        self.assertEqual(supplies["Water"], "14.0 gallons")
        self.assertEqual(supplies["Canned Food (meals)"], "42 cans")
        self.assertEqual(supplies["Batteries (AA)"], "8") # 2 people * (4/7) batteries/day * 7 days = 8
        self.assertEqual(supplies["First Aid Kits"], "1") # ceil(2 people / 2) = 1 kit
        self.assertEqual(supplies["Flashlights"], "2") # 1 per person

    def test_calculate_supplies_single_person_single_day(self):
        # Test edge case for minimum values
        # Mock rationale: Testing the core calculation logic with minimum valid inputs.
        supplies = calculate_supplies(num_people=1, duration_days=1)
        self.assertEqual(supplies["Water"], "1.0 gallons")
        self.assertEqual(supplies["Canned Food (meals)"], "3 cans")
        self.assertEqual(supplies["Batteries (AA)"], "1") # 1 person * (4/7) batteries/day * 1 day = 0.57, rounds up to 1
        self.assertEqual(supplies["First Aid Kits"], "1") # ceil(1 person / 2) = 1
        self.assertEqual(supplies["Flashlights"], "1")

    def test_calculate_supplies_large_group_long_duration(self):
        # Test with larger numbers to ensure scalability
        # Mock rationale: Testing the core calculation logic with larger inputs.
        supplies = calculate_supplies(num_people=10, duration_days=30)
        self.assertEqual(supplies["Water"], "300.0 gallons")
        self.assertEqual(supplies["Canned Food (meals)"], "900 cans")
        self.assertEqual(supplies["Batteries (AA)"], "172") # 10 * (4/7) * 30 = 171.4, rounds up to 172
        self.assertEqual(supplies["First Aid Kits"], "5") # ceil(10 people / 2) = 5 kits
        self.assertEqual(supplies["Flashlights"], "10")

    def test_calculate_supplies_invalid_input(self):
        # Test error handling for invalid inputs
        # Mock rationale: Ensuring the function correctly raises errors for invalid parameters.
        with self.assertRaises(ValueError):
            calculate_supplies(num_people=0, duration_days=5)
        with self.assertRaises(ValueError):
            calculate_supplies(num_people=5, duration_days=0)
        with self.assertRaises(ValueError):
            calculate_supplies(num_people=-1, duration_days=5)

    @patch('builtins.input', side_effect=['2', '7'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_function_basic_input(self, mock_stdout, mock_input):
        # Test the main CLI function with valid inputs
        # Mock rationale: `input` is mocked to provide deterministic user input for the CLI.
        # `sys.stdout` is mocked to capture the printed output for assertion.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Welcome to the Pre-Apocalypse Pantry Planner!", output)
        self.assertIn("Water: 14.0 gallons", output)
        self.assertIn("Canned Food (meals): 42 cans", output)
        self.assertIn("Batteries (AA): 8", output)
        self.assertIn("First Aid Kits: 1", output)
        self.assertIn("Flashlights: 2", output)
        self.assertIn("Stay safe out there!", output)

    @patch('builtins.input', side_effect=['-1', '2', '0', '7'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_function_invalid_then_valid_input(self, mock_stdout, mock_input):
        # Test the main CLI function with initial invalid inputs followed by valid ones
        # Mock rationale: `input` is mocked to simulate user retrying after invalid entries.
        # `sys.stdout` is mocked to capture the printed output for assertion.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Please enter a positive number for people.", output)
        self.assertIn("Please enter a positive number for duration.", output)
        self.assertIn("Water: 14.0 gallons", output)

    @patch('builtins.input', side_effect=['abc', '2', 'xyz', '7'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_function_non_integer_input(self, mock_stdout, mock_input):
        # Test the main CLI function with non-integer inputs followed by valid ones
        # Mock rationale: `input` is mocked to simulate user entering non-numeric values.
        # `sys.stdout` is mocked to capture the printed output for assertion.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Invalid input. Please enter a whole number.", output)
        self.assertIn("Water: 14.0 gallons", output)

if __name__ == '__main__':
    unittest.main()
