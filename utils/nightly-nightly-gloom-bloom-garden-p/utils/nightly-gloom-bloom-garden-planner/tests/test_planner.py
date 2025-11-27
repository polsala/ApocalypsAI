import unittest
from unittest.mock import patch
import json
from src.planner import plan_garden, PLANT_CATALOG

class TestGardenPlanner(unittest.TestCase):

    # Mock rationale: The PLANT_CATALOG is hardcoded in src/planner.py for determinism.
    # We don't need to mock file I/O for the catalog itself.
    # We will use specific test cases to ensure the logic works with this catalog.

    def test_empty_space(self):
        # Test case: No space available, should return an empty plan.
        plan = plan_garden(PLANT_CATALOG, "temperate", "loamy", 0.0)
        self.assertEqual(plan["planting_plan"], [])
        self.assertEqual(plan["total_space_used_sqft"], 0.0)
        self.assertEqual(plan["total_estimated_yield_kg"], 0.0)
        self.assertEqual(plan["remaining_space_sqft"], 0.0)

    def test_no_suitable_plants(self):
        # Test case: Climate/soil combination where no plants are suitable.
        # Mock rationale: We're testing the filtering logic against the existing catalog.
        # No need to mock the catalog itself, just provide conditions that won't match.
        plan = plan_garden(PLANT_CATALOG, "arctic", "volcanic", 10.0)
        self.assertEqual(plan["planting_plan"], [])
        self.assertEqual(plan["total_space_used_sqft"], 0.0)
        self.assertEqual(plan["total_estimated_yield_kg"], 0.0)
        self.assertEqual(plan["remaining_space_sqft"], 10.0)

    def test_basic_plan_temperate_loamy_10sqft(self):
        # Test case: Standard conditions, sufficient space.
        plan = plan_garden(PLANT_CATALOG, "temperate", "loamy", 10.0)
        self.assertGreater(len(plan["planting_plan"]), 0)
        self.assertLessEqual(plan["total_space_used_sqft"], 10.0)
        self.assertGreater(plan["total_estimated_yield_kg"], 0.0)

        # Radish is the fastest growing and suitable for temperate/loamy.
        # It will fill the entire 10 sqft.
        self.assertEqual(len(plan["planting_plan"]), 1)
        self.assertEqual(plan["planting_plan"][0]["name"], "Radish")
        self.assertEqual(plan["planting_plan"][0]["quantity"], 50)
        self.assertEqual(plan["planting_plan"][0]["space_used_sqft"], 10.0)
        self.assertEqual(plan["planting_plan"][0]["estimated_yield_kg"], 25.0)
        self.assertEqual(plan["total_space_used_sqft"], 10.0)
        self.assertEqual(plan["total_estimated_yield_kg"], 25.0)
        self.assertEqual(plan["remaining_space_sqft"], 0.0)

    def test_limited_space_warm_loamy_5sqft(self):
        # Test case: Limited space, different conditions.
        plan = plan_garden(PLANT_CATALOG, "warm", "loamy", 5.0)
        self.assertGreater(len(plan["planting_plan"]), 0)
        self.assertLessEqual(plan["total_space_used_sqft"], 5.0)

        # Radish is still the fastest growing and suitable for warm/loamy (via 'temperate').
        # It will fill the entire 5 sqft.
        self.assertEqual(len(plan["planting_plan"]), 1)
        self.assertEqual(plan["planting_plan"][0]["name"], "Radish")
        self.assertEqual(plan["planting_plan"][0]["quantity"], 25)
        self.assertEqual(plan["planting_plan"][0]["space_used_sqft"], 5.0)
        self.assertEqual(plan["planting_plan"][0]["estimated_yield_kg"], 12.5)
        self.assertEqual(plan["total_space_used_sqft"], 5.0)
        self.assertEqual(plan["total_estimated_yield_kg"], 12.5)
        self.assertEqual(plan["remaining_space_sqft"], 0.0)

    def test_specific_plant_selection_cool_sandy_7sqft(self):
        # Test case: Conditions that favor specific plants.
        plan = plan_garden(PLANT_CATALOG, "cool", "sandy", 7.0)

        # Radish is the fastest growing and suitable for cool/sandy.
        # It will fill the entire 7 sqft.
        self.assertEqual(len(plan["planting_plan"]), 1)
        self.assertEqual(plan["planting_plan"][0]["name"], "Radish")
        self.assertEqual(plan["planting_plan"][0]["quantity"], 35)
        self.assertEqual(plan["planting_plan"][0]["space_used_sqft"], 7.0)
        self.assertEqual(plan["planting_plan"][0]["estimated_yield_kg"], 17.5)
        self.assertEqual(plan["total_space_used_sqft"], 7.0)
        self.assertEqual(plan["total_estimated_yield_kg"], 17.5)
        self.assertEqual(plan["remaining_space_sqft"], 0.0)

    def test_small_space_not_enough_for_any_plant(self):
        # Test case: Space too small for even the smallest plant (Radish needs 0.2 sqft).
        plan = plan_garden(PLANT_CATALOG, "temperate", "loamy", 0.1)
        self.assertEqual(plan["planting_plan"], [])
        self.assertEqual(plan["total_space_used_sqft"], 0.0)
        self.assertEqual(plan["total_estimated_yield_kg"], 0.0)
        self.assertEqual(plan["remaining_space_sqft"], 0.1)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_function(self, mock_print, mock_parse_args):
        # Mock rationale: We mock argparse to control CLI input without actually running the CLI.
        # We mock print to capture the output and assert its content.
        mock_parse_args.return_value = argparse.Namespace(
            climate="warm", soil="loamy", space=5.0
        )
        from src.planner import main
        main()
        mock_print.assert_called_once()
        printed_output = json.loads(mock_print.call_args[0][0])

        self.assertEqual(printed_output["climate_zone"], "warm")
        self.assertEqual(printed_output["soil_type"], "loamy")
        self.assertEqual(printed_output["available_space_sqft"], 5.0)
        self.assertEqual(len(printed_output["planting_plan"]), 1)
        self.assertEqual(printed_output["planting_plan"][0]["name"], "Radish")
        self.assertEqual(printed_output["planting_plan"][0]["quantity"], 25)
        self.assertEqual(printed_output["total_space_used_sqft"], 5.0)
        self.assertEqual(printed_output["total_estimated_yield_kg"], 12.5)


if __name__ == "__main__":
    unittest.main()
