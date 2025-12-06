import unittest
from src.optimizer import optimize_inventory

class TestScavengerInventoryOptimizer(unittest.TestCase):

    def test_empty_items(self):
        # Test with an empty list of items
        items = []
        capacity = 10
        selected, value, weight = optimize_inventory(items, capacity)
        self.assertEqual(selected, [])
        self.assertEqual(value, 0)
        self.assertEqual(weight, 0)

    def test_zero_capacity(self):
        # Test with zero capacity
        items = [
            {'name': 'Rusty Can', 'value': 1, 'weight': 1},
            {'name': 'Shiny Bolt', 'value': 5, 'weight': 3},
        ]
        capacity = 0
        selected, value, weight = optimize_inventory(items, capacity)
        self.assertEqual(selected, [])
        self.assertEqual(value, 0)
        self.assertEqual(weight, 0)

    def test_basic_selection(self):
        # Test a simple case where some items are selected
        items = [
            {'name': 'Water Purifier', 'value': 10, 'weight': 4},
            {'name': 'MRE Pack', 'value': 7, 'weight': 3},
            {'name': 'Broken Radio', 'value': 3, 'weight': 2},
        ]
        capacity = 6
        selected, value, weight = optimize_inventory(items, capacity)
        # Expected: MRE Pack (3kg, 7v) + Broken Radio (2kg, 3v) = 5kg, 10v
        # Water Purifier (4kg, 10v) alone is 4kg, 10v.
        # Both combinations yield 10 value. The algorithm will pick one based on internal order.
        # We assert on the total value and weight, and that the expected items are present.
        self.assertIn('MRE Pack', selected)
        self.assertIn('Broken Radio', selected)
        self.assertEqual(len(selected), 2)
        self.assertEqual(value, 10)
        self.assertEqual(weight, 5)

    def test_items_exceeding_capacity(self):
        # Test where all items exceed capacity
        items = [
            {'name': 'Heavy Armor', 'value': 100, 'weight': 20},
            {'name': 'Large Generator', 'value': 500, 'weight': 30},
        ]
        capacity = 10
        selected, value, weight = optimize_inventory(items, capacity)
        self.assertEqual(selected, [])
        self.assertEqual(value, 0)
        self.assertEqual(weight, 0)

    def test_full_capacity_usage(self):
        # Test where capacity is fully utilized
        items = [
            {'name': 'Medkit', 'value': 20, 'weight': 5},
            {'name': 'Ammo Crate', 'value': 15, 'weight': 4},
            {'name': 'Survival Knife', 'value': 10, 'weight': 2},
        ]
        capacity = 11
        selected, value, weight = optimize_inventory(items, capacity)
        # Expected: Medkit (5kg, 20v) + Ammo Crate (4kg, 15v) + Survival Knife (2kg, 10v) = 11kg, 45v
        self.assertIn('Medkit', selected)
        self.assertIn('Ammo Crate', selected)
        self.assertIn('Survival Knife', selected)
        self.assertEqual(len(selected), 3)
        self.assertEqual(value, 45)
        self.assertEqual(weight, 11)

    def test_complex_scenario(self):
        # A more complex scenario with various item values and weights
        items = [
            {'name': 'Ancient Map', 'value': 60, 'weight': 10},
            {'name': 'Geiger Counter', 'value': 100, 'weight': 20},
            {'name': 'Mutant Repellent', 'value': 120, 'weight': 30},
            {'name': 'Shiny Trinket', 'value': 10, 'weight': 5},
            {'name': 'Rusty Pipe', 'value': 5, 'weight': 1},
        ]
        capacity = 50
        selected, value, weight = optimize_inventory(items, capacity)
        # Expected optimal: Geiger Counter (20kg, 100v) + Mutant Repellent (30kg, 120v) = 50kg, 220v
        self.assertIn('Geiger Counter', selected)
        self.assertIn('Mutant Repellent', selected)
        self.assertEqual(len(selected), 2)
        self.assertEqual(value, 220)
        self.assertEqual(weight, 50)

    def test_items_with_same_name_but_distinct_properties(self):
        # Test with items having the same name but different properties (treated as distinct entities)
        items = [
            {'name': 'Scrap Metal (small)', 'value': 5, 'weight': 2},
            {'name': 'Scrap Metal (large)', 'value': 8, 'weight': 3}, # A better piece of scrap
            {'name': 'Rope', 'value': 3, 'weight': 1},
        ]
        capacity = 4
        selected, value, weight = optimize_inventory(items, capacity)
        # Expected: 'Scrap Metal (large)' (value 8, weight 3) + 'Rope' (value 3, weight 1) = 4kg, 11v
        self.assertIn('Scrap Metal (large)', selected)
        self.assertIn('Rope', selected)
        self.assertEqual(len(selected), 2)
        self.assertEqual(value, 11)
        self.assertEqual(weight, 4)

    # Mock rationale: The `optimize_inventory` function is a pure computational function;
    # it takes inputs and produces outputs deterministically without external dependencies.
    # Therefore, explicit mocking of external services or data sources is not required
    # for its unit tests. The tests directly provide input data (items and capacity)
    # and assert on the returned values, ensuring determinism and offline execution.
    # If the utility were to fetch items from a file or API, those would be mocked.
    # For this self-contained computational utility, direct input is the 'mock' data source.
