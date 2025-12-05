import unittest
from unittest.mock import patch, mock_open
import json
import sys
import io

# Import functions and classes from the src module
from src.planner import Plant, load_seed_data, plan_garden, main

class TestPlant(unittest.TestCase):
    def test_plant_value_per_sqm(self):
        plant = Plant("Tomato", 0.5, 10, ["temperate"])
        self.assertAlmostEqual(plant.get_value_per_sqm(), 20.0)

        plant_zero_space = Plant("Air Plant", 0, 1, ["any"])
        self.assertEqual(plant_zero_space.get_value_per_sqm(), 0)

class TestLoadSeedData(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_seed_data_success(self, mock_json_load, mock_file_open):
        # Mock rationale: Simulate reading a valid JSON seed file without actual file I/O.
        mock_json_load.return_value = [
            {"name": "Carrot", "space_sqm": 0.1, "yield_units": 5, "climate_zones": ["temperate", "cold"]},
            {"name": "Potato", "space_sqm": 0.5, "yield_units": 20, "climate_zones": ["temperate"]}
        ]
        seeds = load_seed_data("dummy_path.json")
        self.assertEqual(len(seeds), 2)
        self.assertEqual(seeds[0].name, "Carrot")
        self.assertEqual(seeds[1].yield_units, 20)
        mock_file_open.assert_called_once_with("dummy_path.json", 'r', encoding='utf-8')

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_seed_data_file_not_found(self, mock_file_open):
        # Mock rationale: Simulate a missing seed file.
        with self.assertRaises(SystemExit) as cm:
            load_seed_data("non_existent.json")
        self.assertEqual(cm.exception.code, 1)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "", 0))
    def test_load_seed_data_invalid_json(self, mock_json_load, mock_file_open):
        # Mock rationale: Simulate a corrupted or malformed JSON seed file.
        with self.assertRaises(SystemExit) as cm:
            load_seed_data("invalid.json")
        self.assertEqual(cm.exception.code, 1)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_seed_data_missing_key(self, mock_json_load, mock_file_open):
        # Mock rationale: Simulate a JSON seed file missing a required key.
        mock_json_load.return_value = [
            {"name": "Carrot", "space_sqm": 0.1, "yield_units": 5} # Missing 'climate_zones'
        ]
        with self.assertRaises(SystemExit) as cm:
            load_seed_data("missing_key.json")
        self.assertEqual(cm.exception.code, 1)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_seed_data_invalid_type(self, mock_json_load, mock_file_open):
        # Mock rationale: Simulate a JSON seed file with an invalid data type for a key.
        mock_json_load.return_value = [
            {"name": "Carrot", "space_sqm": "0.1", "yield_units": 5, "climate_zones": ["temperate"]}
        ]
        with self.assertRaises(SystemExit) as cm:
            load_seed_data("invalid_type.json")
        self.assertEqual(cm.exception.code, 1)

class TestPlanGarden(unittest.TestCase):
    def setUp(self):
        self.seeds = [
            Plant("Carrot", 0.1, 5, ["temperate", "cold"]), # Value: 50
            Plant("Potato", 0.5, 20, ["temperate"]),        # Value: 40
            Plant("Tomato", 0.3, 12, ["temperate", "warm"]), # Value: 40
            Plant("Cactus", 1.0, 1, ["arid"]),              # Value: 1
            Plant("Wheat", 0.2, 8, ["temperate"]),          # Value: 40
            Plant("Lettuce", 0.1, 3, ["temperate", "cold"]) # Value: 30
        ]

    def test_empty_area(self):
        plan = plan_garden(0, "temperate", self.seeds)
        self.assertEqual(len(plan), 0)

    def test_no_suitable_seeds(self):
        plan = plan_garden(10, "tropical", self.seeds) # No tropical seeds
        self.assertEqual(len(plan), 0)

    def test_basic_plan_temperate(self):
        plan = plan_garden(1.0, "temperate", self.seeds)
        # Expected order: Carrot (50), then Potato/Tomato/Wheat (40), then Lettuce (30)
        # With 1.0 sqm, only carrots fit perfectly if prioritized.
        self.assertGreater(len(plan), 0)
        self.assertEqual(plan[0]['plant'], "Carrot")
        self.assertEqual(plan[0]['count'], 10) # 1.0 / 0.1 = 10
        self.assertAlmostEqual(plan[0]['total_space_used_sqm'], 1.0)
        self.assertEqual(len(plan), 1)

        # Test with more area to see multiple plants
        plan_1_5 = plan_garden(1.5, "temperate", self.seeds)
        self.assertGreater(len(plan_1_5), 0)
        # Carrot (0.1 sqm) -> 10x = 1.0 sqm used. Remaining 0.5 sqm.
        # Next best (value 40): Potato (0.5 sqm) -> 1x = 0.5 sqm used. Remaining 0.0 sqm.
        self.assertEqual(plan_1_5[0]['plant'], "Carrot")
        self.assertEqual(plan_1_5[0]['count'], 10)
        self.assertEqual(plan_1_5[1]['plant'], "Potato")
        self.assertEqual(plan_1_5[1]['count'], 1)
        self.assertAlmostEqual(sum(item['total_space_used_sqm'] for item in plan_1_5), 1.5)

    def test_plan_with_limited_space(self):
        plan = plan_garden(0.25, "temperate", self.seeds)
        # Carrot (0.1 sqm) -> 2x = 0.2 sqm used. Remaining 0.05 sqm.
        self.assertEqual(len(plan), 1)
        self.assertEqual(plan[0]['plant'], "Carrot")
        self.assertEqual(plan[0]['count'], 2)
        self.assertAlmostEqual(plan[0]['total_space_used_sqm'], 0.2)

    def test_plan_arid_climate(self):
        plan = plan_garden(5.0, "arid", self.seeds)
        # Only Cactus is suitable for arid.
        # Cactus (1.0 sqm) -> 5x = 5.0 sqm used.
        self.assertEqual(len(plan), 1)
        self.assertEqual(plan[0]['plant'], "Cactus")
        self.assertEqual(plan[0]['count'], 5)
        self.assertAlmostEqual(plan[0]['total_space_used_sqm'], 5.0)

    def test_plan_cold_climate(self):
        plan = plan_garden(0.3, "cold", self.seeds)
        # Suitable: Carrot (0.1 sqm, 5 yield), Lettuce (0.1 sqm, 3 yield)
        # Carrot (value 50) > Lettuce (value 30)
        # Carrot: 3x = 0.3 sqm used.
        self.assertEqual(len(plan), 1)
        self.assertEqual(plan[0]['plant'], "Carrot")
        self.assertEqual(plan[0]['count'], 3)
        self.assertAlmostEqual(plan[0]['total_space_used_sqm'], 0.3)

class TestMainFunction(unittest.TestCase):
    def setUp(self):
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = self.mock_stdout = io.StringIO()
        sys.stderr = self.mock_stderr = io.StringIO()

    def tearDown(self):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    @patch('src.planner.load_seed_data')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_success(self, mock_parse_args, mock_load_seed_data):
        # Mock rationale: Simulate command-line arguments and successful seed data loading.
        mock_parse_args.return_value = argparse.Namespace(
            area=1.0, climate="temperate", seeds="dummy_seeds.json"
        )
        mock_load_seed_data.return_value = [
            Plant("Carrot", 0.1, 5, ["temperate"]),
            Plant("Potato", 0.5, 20, ["temperate"])
        ]

        main()
        output = self.mock_stdout.getvalue()
        self.assertIn("--- Gloom-to-Bloom Garden Plan ---", output)
        self.assertIn("10x Carrot", output)
        self.assertIn("Total estimated yield: 50 units", output)
        self.assertIn("Total space utilized: 1.00 sqm", output)
        self.assertIn("Remaining unused space: 0.00 sqm", output)
        self.assertEqual(self.mock_stderr.getvalue(), "") # No errors

    @patch('src.planner.load_seed_data', return_value=[])
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_seeds_loaded(self, mock_parse_args, mock_load_seed_data):
        # Mock rationale: Simulate no seeds being loaded, leading to an early exit.
        mock_parse_args.return_value = argparse.Namespace(
            area=1.0, climate="temperate", seeds="empty_seeds.json"
        )
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2) # No-op exit code
        self.assertIn("No seeds loaded or available. Cannot plan a garden.", self.mock_stderr.getvalue())

    @patch('src.planner.load_seed_data')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_viable_plan(self, mock_parse_args, mock_load_seed_data):
        # Mock rationale: Simulate a scenario where no plants can be placed (e.g., wrong climate).
        mock_parse_args.return_value = argparse.Namespace(
            area=1.0, climate="tropical", seeds="dummy_seeds.json"
        )
        mock_load_seed_data.return_value = [
            Plant("Carrot", 0.1, 5, ["temperate"]),
            Plant("Potato", 0.5, 20, ["temperate"])
        ]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 2) # No-op exit code
        self.assertIn("Could not create a viable garden plan", self.mock_stderr.getvalue())

    @patch('src.planner.load_seed_data', side_effect=SystemExit(1)) # Simulate load_seed_data failing
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_seed_load_failure(self, mock_parse_args, mock_load_seed_data):
        # Mock rationale: Simulate load_seed_data encountering an error (e.g., malformed JSON) and exiting.
        mock_parse_args.return_value = argparse.Namespace(
            area=1.0, climate="temperate", seeds="bad_seeds.json"
        )
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1) # Failure exit code
        # The error message itself would be printed by load_seed_data before exiting.
        # We just check the exit code here.

if __name__ == '__main__':
    unittest.main()
