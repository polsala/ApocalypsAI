import unittest
import json
from unittest.mock import patch, mock_open
from src.optimizer import GearItem, load_gear_from_json, optimize_loadout

class TestGearOptimizer(unittest.TestCase):

    def setUp(self):
        # Mock rationale: Provides a consistent set of gear items for testing
        # without relying on external files or dynamic data.
        self.mock_gear_data = [
            {"name": "Rusty Machete", "weight": 1.5, "base_utility": 7, "condition": 0.6, "tags": ["combat", "scavenging"]},
            {"name": "Duct Tape Roll", "weight": 0.2, "base_utility": 9, "condition": 1.0, "tags": ["repair", "utility"]},
            {"name": "Water Purifier (Broken)", "weight": 0.8, "base_utility": 8, "condition": 0.1, "tags": ["survival", "hydration"]},
            {"name": "Radiation Suit (Patched)", "weight": 5.0, "base_utility": 10, "condition": 0.7, "tags": ["protection", "survival"]},
            {"name": "Shiny Bottlecaps", "weight": 0.1, "base_utility": 1, "condition": 1.0, "tags": ["currency", "trade"]},
            {"name": "Medical Kit (Basic)", "weight": 0.7, "base_utility": 8, "condition": 0.9, "tags": ["medical", "survival"]},
            {"name": "Energy Bar", "weight": 0.1, "base_utility": 5, "condition": 1.0, "tags": ["food", "survival"]},
            {"name": "Heavy Plasma Rifle", "weight": 8.0, "base_utility": 15, "condition": 0.8, "tags": ["combat", "heavy"]},
            {"name": "Lightweight Binoculars", "weight": 0.3, "base_utility": 6, "condition": 0.9, "tags": ["exploration", "utility"]}
        ]
        self.expected_gear_items = [
            GearItem("Rusty Machete", 1.5, 7, 0.6, ["combat", "scavenging"]),
            GearItem("Duct Tape Roll", 0.2, 9, 1.0, ["repair", "utility"]),
            GearItem("Water Purifier (Broken)", 0.8, 8, 0.1, ["survival", "hydration"]),
            GearItem("Radiation Suit (Patched)", 5.0, 10, 0.7, ["protection", "survival"]),
            GearItem("Shiny Bottlecaps", 0.1, 1, 1.0, ["currency", "trade"]),
            GearItem("Medical Kit (Basic)", 0.7, 8, 0.9, ["medical", "survival"]),
            GearItem("Energy Bar", 0.1, 5, 1.0, ["food", "survival"]),
            GearItem("Heavy Plasma Rifle", 8.0, 15, 0.8, ["combat", "heavy"]),
            GearItem("Lightweight Binoculars", 0.3, 6, 0.9, ["exploration", "utility"])
        ]

    def test_gear_item_properties(self):
        item = GearItem("Test Item", 1.0, 10, 0.5, ["test"])
        self.assertEqual(item.effective_utility, 5.0)
        self.assertEqual(item.utility_per_weight, 5.0)

        item_zero_weight = GearItem("Zero Weight", 0.0, 10, 1.0, ["test"])
        self.assertEqual(item_zero_weight.utility_per_weight, float('inf'))

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_load_gear_from_json(self, mock_json_load, mock_file_open):
        # Mock rationale: Prevents actual file system access during testing
        # and allows control over the JSON data returned.
        mock_json_load.return_value = self.mock_gear_data
        
        gear = load_gear_from_json("dummy_path.json")
        self.assertEqual(len(gear), len(self.mock_gear_data))
        self.assertEqual(gear[0].name, "Rusty Machete")
        self.assertAlmostEqual(gear[0].effective_utility, 7 * 0.6)
        self.assertEqual(gear[1].tags, ["repair", "utility"])

        # Test malformed data
        mock_json_load.return_value = [
            {"name": "Good Item", "weight": 1.0, "base_utility": 5},
            {"name": "Bad Item", "weight": "invalid", "base_utility": 3} # Malformed weight
        ]
        # Assuming logging is used for warnings, capture and check output
        with self.assertLogs('src.optimizer', level='WARNING') as cm:
            gear_malformed = load_gear_from_json("dummy_path.json")
            self.assertEqual(len(gear_malformed), 1)
            self.assertIn("Warning: Skipping malformed gear item Bad Item", cm.output[0])


    def test_optimize_loadout_basic(self):
        # Mock rationale: Uses pre-defined GearItem objects for deterministic testing
        # of the optimization logic without external dependencies.
        loadout = optimize_loadout(self.expected_gear_items, max_weight=3.0)
        names = sorted([item.name for item in loadout])
        # Expected: Duct Tape (9/0.2=45), Energy Bar (5/0.1=50), Medical Kit (7.2/0.7=10.2), Binoculars (5.4/0.3=18), Machete (4.2/1.5=2.8)
        # Order by utility_per_weight: Energy Bar (50), Duct Tape (45), Lightweight Binoculars (18), Medical Kit (10.2), Machete (2.8)
        # Loadout: Energy Bar (0.1), Duct Tape (0.2), Lightweight Binoculars (0.3), Medical Kit (0.7) -> Total 1.3kg
        # Next: Machete (1.5kg) -> Total 2.8kg
        # Total weight: 0.1 + 0.2 + 0.3 + 0.7 + 1.5 = 2.8
        self.assertIn("Energy Bar", names)
        self.assertIn("Duct Tape Roll", names)
        self.assertIn("Lightweight Binoculars", names)
        self.assertIn("Medical Kit (Basic)", names)
        self.assertIn("Rusty Machete", names)
        self.assertAlmostEqual(sum(item.weight for item in loadout), 2.8)
        self.assertAlmostEqual(sum(item.effective_utility for item in loadout), 5.0 + 9.0 + 5.4 + 7.2 + 4.2) # 30.8

    def test_optimize_loadout_max_weight_low(self):
        # Mock rationale: Uses pre-defined GearItem objects for deterministic testing
        # of the optimization logic under specific constraints.
        loadout = optimize_loadout(self.expected_gear_items, max_weight=0.1)
        names = sorted([item.name for item in loadout])
        # Only Energy Bar or Shiny Bottlecaps fit, Energy Bar has higher utility_per_weight (50 vs 10)
        self.assertEqual(len(loadout), 1)
        self.assertEqual(names[0], "Energy Bar")
        self.assertAlmostEqual(sum(item.weight for item in loadout), 0.1)

    def test_optimize_loadout_no_items_fit(self):
        # Mock rationale: Uses pre-defined GearItem objects for deterministic testing
        # of the optimization logic when no items can be selected.
        loadout = optimize_loadout(self.expected_gear_items, max_weight=0.05)
        self.assertEqual(len(loadout), 0)
        self.assertAlmostEqual(sum(item.weight for item in loadout), 0.0)

    def test_optimize_loadout_with_task_tags(self):
        # Mock rationale: Uses pre-defined GearItem objects for deterministic testing
        # of the optimization logic with tag-based filtering.
        # Task: "scavenging"
        loadout = optimize_loadout(self.expected_gear_items, max_weight=2.0, task_tags=["scavenging"])
        names = sorted([item.name for item in loadout])
        # Relevant items for "scavenging": Rusty Machete (1.5kg, U:4.2, U/W:2.8)
        # Only Machete fits within 2.0kg
        self.assertEqual(len(loadout), 1)
        self.assertEqual(names[0], "Rusty Machete")
        self.assertAlmostEqual(sum(item.weight for item in loadout), 1.5)

        # Task: "combat"
        loadout_combat = optimize_loadout(self.expected_gear_items, max_weight=10.0, task_tags=["combat"])
        names_combat = sorted([item.name for item in loadout_combat])
        # Relevant items for "combat": Rusty Machete (1.5kg, U:4.2, U/W:2.8), Heavy Plasma Rifle (8.0kg, U:12, U/W:1.5)
        # Both fit within 10kg. Machete has higher U/W.
        self.assertIn("Rusty Machete", names_combat)
        self.assertIn("Heavy Plasma Rifle", names_combat)
        self.assertAlmostEqual(sum(item.weight for item in loadout_combat), 1.5 + 8.0) # 9.5
        self.assertAlmostEqual(sum(item.effective_utility for item in loadout_combat), 4.2 + 12.0) # 16.2

    def test_optimize_loadout_no_matching_tags_but_still_provides_loadout(self):
        # Mock rationale: Uses pre-defined GearItem objects for deterministic testing
        # of the fallback logic when no items match the specified tags.
        # Task: "nonexistent_tag"
        loadout = optimize_loadout(self.expected_gear_items, max_weight=1.0, task_tags=["nonexistent_tag"])
        names = sorted([item.name for item in loadout])
        # Should fall back to considering all items, then pick best U/W
        # Expected: Energy Bar (0.1), Duct Tape (0.2), Lightweight Binoculars (0.3), Medical Kit (0.7)
        # Total weight: 0.1 + 0.2 + 0.3 = 0.6 (Medical Kit would make it 1.3, too much)
        self.assertIn("Energy Bar", names)
        self.assertIn("Duct Tape Roll", names)
        self.assertIn("Lightweight Binoculars", names)
        self.assertNotIn("Medical Kit (Basic)", names) # 0.6 + 0.7 = 1.3 > 1.0
        self.assertAlmostEqual(sum(item.weight for item in loadout), 0.1 + 0.2 + 0.3) # 0.6

    def test_optimize_loadout_empty_available_items(self):
        # Mock rationale: Tests edge case where no items are available.
        loadout = optimize_loadout([], max_weight=5.0, task_tags=["survival"])
        self.assertEqual(len(loadout), 0)
        self.assertAlmostEqual(sum(item.weight for item in loadout), 0.0)

    def test_optimize_loadout_zero_utility_items(self):
        # Mock rationale: Tests behavior with items that have zero effective utility.
        items = [
            GearItem("Broken Radio", 0.5, 0, 0.0, ["utility"]),
            GearItem("Shiny Rock", 0.1, 1, 1.0, ["currency"])
        ]
        loadout = optimize_loadout(items, max_weight=0.5)
        names = sorted([item.name for item in loadout])
        self.assertEqual(len(loadout), 1)
        self.assertEqual(names[0], "Shiny Rock") # Rock has U/W 10, Radio has 0
        self.assertAlmostEqual(sum(item.weight for item in loadout), 0.1)
