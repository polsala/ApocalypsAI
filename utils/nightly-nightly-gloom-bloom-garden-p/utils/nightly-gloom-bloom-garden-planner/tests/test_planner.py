import unittest
from unittest.mock import patch
import sys
import io
import argparse
from src.planner import plan_garden, main, PLANT_DATA

class TestGloomBloomGardenPlanner(unittest.TestCase):

    def test_plan_garden_basic_scenario(self):
        # Test a standard scenario with known outputs
        width, length = 10, 10
        light, soil = "sun", "loamy"
        recommendations = plan_garden(width, length, light, soil)

        self.assertIsInstance(recommendations, dict)
        self.assertGreater(len(recommendations), 0)

        # Expected plants for sun/loamy: Mutant Tomato, Glow-in-the-Dark Carrot, Rad-ish, Survival Beans, Dusty Potato, Wasteland Wheat, Scavenger Squash
        expected_plants = {
            "Mutant Tomato (Red Dawn)", "Glow-in-the-Dark Carrot", "Rad-ish (Quick Sprout)",
            "Survival Beans (Climbing)", "Dusty Potato (Tuber of Hope)", "Wasteland Wheat",
            "Scavenger Squash"
        }
        self.assertSetEqual(set(recommendations.keys()), expected_plants)

        # Verify quantities for a 100 unit area
        self.assertEqual(recommendations["Mutant Tomato (Red Dawn)"], 50) # 100 / 2.0
        self.assertEqual(recommendations["Glow-in-the-Dark Carrot"], 200) # 100 / 0.5
        self.assertEqual(recommendations["Rad-ish (Quick Sprout)"], 333) # 100 / 0.3 = 333.33 -> 333
        self.assertEqual(recommendations["Survival Beans (Climbing)"], 66) # 100 / 1.5 = 66.66 -> 66
        self.assertEqual(recommendations["Dusty Potato (Tuber of Hope)"], 83) # 100 / 1.2 = 83.33 -> 83
        self.assertEqual(recommendations["Wasteland Wheat"], 500) # 100 / 0.2
        self.assertEqual(recommendations["Scavenger Squash"], 33) # 100 / 3.0 = 33.33 -> 33

    def test_plan_garden_no_matching_plants(self):
        # Mock rationale: Temporarily modify PLANT_DATA to ensure no matches for a specific test case.
        # This allows testing the 'no recommendations' path without changing the main PLANT_DATA.
        original_plant_data = PLANT_DATA.copy()
        try:
            # Create a temporary PLANT_DATA that only has 'sun' and 'sandy' plants
            PLANT_DATA.clear()
            PLANT_DATA["Desert Bloom"] = {"space": 1.0, "light": ["sun"], "soil": ["sandy"], "yield": "low", "resilience": "Exceptional"}

            # Test with conditions that won't match the "Desert Bloom"
            recommendations = plan_garden(10, 10, "shade", "loamy")
            self.assertEqual(recommendations, {})

            recommendations = plan_garden(10, 10, "sun", "loamy") # Light matches, soil doesn't
            self.assertEqual(recommendations, {})

            recommendations = plan_garden(10, 10, "partial", "sandy") # Soil matches, light doesn't
            self.assertEqual(recommendations, {})

        finally:
            PLANT_DATA.clear()
            PLANT_DATA.update(original_plant_data) # Restore original PLANT_DATA

    def test_plan_garden_zero_area(self):
        # Test with zero area, should result in no recommendations
        recommendations = plan_garden(0, 10, "sun", "loamy")
        self.assertEqual(recommendations, {})
        recommendations = plan_garden(10, 0, "sun", "loamy")
        self.assertEqual(recommendations, {})

    def test_plan_garden_negative_dimensions(self):
        # Test with negative dimensions, should raise ValueError
        with self.assertRaises(ValueError):
            plan_garden(-1, 10, "sun", "loamy")
        with self.assertRaises(ValueError):
            plan_garden(10, -1, "sun", "loamy")
        with self.assertRaises(ValueError):
            plan_garden(-1, -1, "sun", "loamy")

    def test_plan_garden_invalid_light_or_soil(self):
        # Test with invalid light or soil types, should raise ValueError
        with self.assertRaises(ValueError):
            plan_garden(10, 10, "moonlight", "loamy")
        with self.assertRaises(ValueError):
            plan_garden(10, 10, "sun", "volcanic")

    def test_main_function_success_output(self):
        # Mock rationale: Capture stdout to verify the printed output of the main function.
        # Mock rationale: Patch sys.argv to simulate command-line arguments.
        # Mock rationale: Patch sys.exit to prevent the test runner from exiting prematurely.
        test_args = ["planner.py", "--width", "5", "--length", "2", "--light", "partial", "--soil", "loamy"]
        with patch.object(sys, 'argv', test_args), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout, \
             patch('sys.exit') as mock_exit:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Gloom & Bloom Garden Plan", output)
            self.assertIn("Shadow Lettuce: 10 units", output) # 5*2 / 1.0 = 10
            self.assertIn("Iron-Leaf Spinach: 14 units", output) # 5*2 / 0.7 = 14.28 -> 14
            self.assertIn("Glow-in-the-Dark Carrot: 20 units", output) # 5*2 / 0.5 = 20
            self.assertIn("Rad-ish (Quick Sprout): 33 units", output) # 5*2 / 0.3 = 33.33 -> 33
            mock_exit.assert_called_with(0)

    def test_main_function_no_plants_output(self):
        # Mock rationale: Capture stdout to verify the printed output when no plants are found.
        # Mock rationale: Patch sys.argv to simulate command-line arguments.
        # Mock rationale: Patch sys.exit to prevent the test runner from exiting prematurely.
        test_args = ["planner.py", "--width", "1", "--length", "1", "--light", "shade", "--soil", "sandy"]
        with patch.object(sys, 'argv', test_args), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout, \
             patch('sys.exit') as mock_exit:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("No suitable plants found", output)
            mock_exit.assert_called_with(0)

    def test_main_function_error_output_from_plan_garden(self):
        # Mock rationale: Capture stderr to verify error messages.
        # Mock rationale: Patch sys.argv to simulate command-line arguments that lead to a ValueError in plan_garden.
        # Mock rationale: Patch sys.exit to prevent the test runner from exiting prematurely.
        test_args = ["planner.py", "--width", "0", "--length", "10", "--light", "sun", "--soil", "loamy"] # width=0 should cause ValueError
        with patch.object(sys, 'argv', test_args), \
             patch('sys.stderr', new_callable=io.StringIO) as mock_stderr, \
             patch('sys.exit') as mock_exit:
            main()
            error_output = mock_stderr.getvalue()
            self.assertIn("Error: Width and length must be positive numbers.", error_output)
            mock_exit.assert_called_with(1)

    def test_main_function_argparse_error_output(self):
        # Mock rationale: Capture stderr to verify argparse's error messages.
        # Mock rationale: Patch sys.argv to simulate invalid command-line arguments (missing required).
        # Mock rationale: Patch sys.exit to prevent the test runner from exiting prematurely.
        # Argparse itself calls sys.exit(2) on invalid args, so we need to mock sys.exit.
        test_args = ["planner.py", "--width", "5", "--length", "2", "--light", "partial"] # Missing --soil
        with patch.object(sys, 'argv', test_args), \
             patch('sys.stderr', new_callable=io.StringIO) as mock_stderr, \
             patch('sys.exit') as mock_exit:
            # argparse.parse_args() will print to stderr and call sys.exit(2)
            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 2) # argparse exits with code 2 for invalid arguments
            error_output = mock_stderr.getvalue()
            self.assertIn("argument --soil is required", error_output)
            mock_exit.assert_called_with(2) # Verify sys.exit was called with 2 by argparse


if __name__ == "__main__":
    unittest.main()
