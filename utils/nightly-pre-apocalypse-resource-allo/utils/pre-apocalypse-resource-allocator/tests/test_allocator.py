import unittest
from src.allocator import allocate_resources

class TestResourceAllocator(unittest.TestCase):

    def test_sufficient_resources(self):
        # Mock rationale: Simulating a scenario with ample resources.
        resources = {
            "food_rations": 100,
            "water_bottles": 50,
            "medkits": 10,
            "tools": 5
        }
        survivors = [
            {"name": "Alice", "needs": {"food_rations": 10, "water_bottles": 5}, "skills": ["medic"]},
            {"name": "Bob", "needs": {"food_rations": 8, "water_bottles": 4}, "skills": ["engineer"]},
        ]
        
        allocation, remaining, unmet = allocate_resources(resources, survivors)

        self.assertEqual(unmet, [])
        self.assertEqual(remaining["food_rations"], 100 - 10 - 8) # 82
        self.assertEqual(remaining["water_bottles"], 50 - 5 - 4) # 41
        self.assertEqual(remaining["medkits"], 10 - 1) # Alice gets one
        self.assertEqual(remaining["tools"], 5 - 1) # Bob gets one

        self.assertEqual(allocation["Alice"]["food_rations"], 10)
        self.assertEqual(allocation["Alice"]["water_bottles"], 5)
        self.assertEqual(allocation["Alice"]["medkits"], 1) # Skill-based
        self.assertEqual(allocation["Bob"]["food_rations"], 8)
        self.assertEqual(allocation["Bob"]["water_bottles"], 4)
        self.assertEqual(allocation["Bob"]["tools"], 1) # Skill-based

    def test_scarce_resources(self):
        # Mock rationale: Simulating a scenario where resources are limited.
        resources = {
            "food_rations": 15,
            "water_bottles": 7,
            "medkits": 0,
            "tools": 0
        }
        survivors = [
            {"name": "Alice", "needs": {"food_rations": 10, "water_bottles": 5}, "skills": ["medic"]},
            {"name": "Bob", "needs": {"food_rations": 8, "water_bottles": 4}, "skills": ["engineer"]},
        ]

        allocation, remaining, unmet = allocate_resources(resources, survivors)

        self.assertEqual(remaining["food_rations"], 0)
        self.assertEqual(remaining["water_bottles"], 0)
        self.assertEqual(remaining["medkits"], 0)
        self.assertEqual(remaining["tools"], 0)

        # Alice gets 10 food, 5 water
        # Bob gets 5 food (15-10), 2 water (7-5)
        self.assertEqual(allocation["Alice"]["food_rations"], 10)
        self.assertEqual(allocation["Alice"]["water_bottles"], 5)
        self.assertNotIn("medkits", allocation["Alice"]) # No medkits available

        self.assertEqual(allocation["Bob"]["food_rations"], 5)
        self.assertEqual(allocation["Bob"]["water_bottles"], 2)
        self.assertNotIn("tools", allocation["Bob"]) # No tools available

        # Unmet needs should be sorted for deterministic comparison
        expected_unmet = [
            ("Bob", "food_rations", 3), # Bob needed 8, got 5
            ("Bob", "water_bottles", 2) # Bob needed 4, got 2
        ]
        self.assertEqual(unmet, expected_unmet)

    def test_no_survivors(self):
        # Mock rationale: Testing an edge case with no survivors.
        resources = {
            "food_rations": 100,
            "water_bottles": 50,
        }
        survivors = []

        allocation, remaining, unmet = allocate_resources(resources, survivors)

        self.assertEqual(allocation, {})
        self.assertEqual(remaining, resources) # All resources remain
        self.assertEqual(unmet, [])

    def test_no_resources(self):
        # Mock rationale: Testing an edge case with no resources.
        resources = {}
        survivors = [
            {"name": "Alice", "needs": {"food_rations": 10, "water_bottles": 5}, "skills": ["medic"]},
        ]

        allocation, remaining, unmet = allocate_resources(resources, survivors)

        self.assertEqual(allocation["Alice"], {}) # Alice gets nothing
        self.assertEqual(remaining, {})
        expected_unmet = [
            ("Alice", "food_rations", 10),
            ("Alice", "water_bottles", 5)
        ]
        self.assertEqual(unmet, expected_unmet)

    def test_skill_based_allocation_only_if_available(self):
        # Mock rationale: Ensuring skill-based items are only allocated if available.
        resources = {
            "food_rations": 10,
            "water_bottles": 5,
            "medkits": 1, # Only one medkit
            "tools": 0   # No tools
        }
        survivors = [
            {"name": "Alice", "needs": {"food_rations": 1, "water_bottles": 1}, "skills": ["medic"]},
            {"name": "Bob", "needs": {"food_rations": 1, "water_bottles": 1}, "skills": ["engineer"]},
            {"name": "Charlie", "needs": {"food_rations": 1, "water_bottles": 1}, "skills": ["medic"]}, # Another medic
        ]

        allocation, remaining, unmet = allocate_resources(resources, survivors)

        # Alice gets the medkit as she is the first medic in the list
        self.assertEqual(allocation["Alice"]["medkits"], 1)
        self.assertNotIn("medkits", allocation["Charlie"]) # Charlie, the second medic, gets none
        self.assertNotIn("tools", allocation["Bob"]) # No tools for Bob

        self.assertEqual(remaining["medkits"], 0)
        self.assertEqual(remaining["tools"], 0)

        # Check basic needs are met
        self.assertEqual(allocation["Alice"]["food_rations"], 1)
        self.assertEqual(allocation["Bob"]["food_rations"], 1)
        self.assertEqual(allocation["Charlie"]["food_rations"], 1)

        self.assertEqual(remaining["food_rations"], 10 - 3) # 7
        self.assertEqual(remaining["water_bottles"], 5 - 3) # 2
        self.assertEqual(unmet, []) # All basic needs met, skill items handled

    def test_resource_priority(self):
        # Mock rationale: Verifying that water is prioritized over food.
        resources = {
            "food_rations": 1,
            "water_bottles": 1,
        }
        survivors = [
            {"name": "Alice", "needs": {"food_rations": 1, "water_bottles": 1}, "skills": []},
            {"name": "Bob", "needs": {"food_rations": 1, "water_bottles": 1}, "skills": []},
        ]

        allocation, remaining, unmet = allocate_resources(resources, survivors)

        # Water has higher priority (1) than food (2)
        # Alice gets water first, then food.
        # Bob gets nothing for water, then food.
        self.assertEqual(allocation["Alice"]["water_bottles"], 1)
        self.assertEqual(allocation["Alice"]["food_rations"], 1)
        self.assertNotIn("water_bottles", allocation["Bob"])
        self.assertNotIn("food_rations", allocation["Bob"])

        self.assertEqual(remaining["food_rations"], 0)
        self.assertEqual(remaining["water_bottles"], 0)

        expected_unmet = [
            ("Bob", "food_rations", 1),
            ("Bob", "water_bottles", 1)
        ]
        self.assertEqual(unmet, expected_unmet)


if __name__ == '__main__':
    unittest.main()
