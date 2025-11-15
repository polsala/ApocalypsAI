import unittest
from unittest.mock import patch
from src.checklist_generator import generate_checklist, get_base_checklist, get_scenario_specific_items

class TestChecklistGenerator(unittest.TestCase):

    def test_get_base_checklist(self):
        """Test that the base checklist contains expected universal items."""
        base_items = get_base_checklist()
        self.assertIsInstance(base_items, list)
        self.assertGreater(len(base_items), 5) # Ensure it's not empty
        self.assertIn("Stockpile non-perishable food (3-month supply)", base_items)
        self.assertIn("First-aid kit (fully stocked)", base_items)
        self.assertIn("Develop a family emergency plan and meeting points", base_items)

    def test_get_scenario_specific_items(self):
        """Test that scenario-specific items are structured correctly."""
        scenario_items = get_scenario_specific_items()
        self.assertIsInstance(scenario_items, dict)
        self.assertIn("zombie_outbreak", scenario_items)
        self.assertIn("ai_uprising", scenario_items)
        self.assertIn("solar_flare", scenario_items)
        self.assertIsInstance(scenario_items["zombie_outbreak"], list)
        self.assertGreater(len(scenario_items["zombie_outbreak"]), 0)
        self.assertIn("Practice headshots (on targets, please!)", scenario_items["zombie_outbreak"])

    def test_generate_checklist_general_catastrophe(self):
        """Test checklist generation for the default/general scenario."""
        checklist = generate_checklist("general_catastrophe")
        base_items = get_base_checklist()
        self.assertIsInstance(checklist, list)
        self.assertEqual(len(checklist), len(base_items)) # Should only contain base items
        for item in base_items:
            self.assertIn(item, checklist)
        # Ensure no scenario-specific items are accidentally included
        scenario_specific = get_scenario_specific_items()
        for scenario_list in scenario_specific.values():
            for item in scenario_list:
                self.assertNotIn(item, checklist)

    def test_generate_checklist_zombie_outbreak(self):
        """Test checklist generation for the zombie outbreak scenario."""
        checklist = generate_checklist("zombie_outbreak")
        base_items = get_base_checklist()
        zombie_items = get_scenario_specific_items()["zombie_outbreak"]
        
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), len(base_items)) # Should have more than just base
        
        for item in base_items:
            self.assertIn(item, checklist)
        for item in zombie_items:
            self.assertIn(item, checklist)
        
        # Ensure no items from other scenarios are included
        ai_items = get_scenario_specific_items()["ai_uprising"]
        for item in ai_items:
            self.assertNotIn(item, checklist)

    def test_generate_checklist_ai_uprising(self):
        """Test checklist generation for the AI uprising scenario."""
        checklist = generate_checklist("ai_uprising")
        base_items = get_base_checklist()
        ai_items = get_scenario_specific_items()["ai_uprising"]
        
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), len(base_items))
        
        for item in base_items:
            self.assertIn(item, checklist)
        for item in ai_items:
            self.assertIn(item, checklist)
        
        # Ensure no items from other scenarios are included
        zombie_items = get_scenario_specific_items()["zombie_outbreak"]
        for item in zombie_items:
            self.assertNotIn(item, checklist)

    def test_generate_checklist_solar_flare(self):
        """Test checklist generation for the solar flare scenario."""
        checklist = generate_checklist("solar_flare")
        base_items = get_base_checklist()
        solar_items = get_scenario_specific_items()["solar_flare"]
        
        self.assertIsInstance(checklist, list)
        self.assertGreater(len(checklist), len(base_items))
        
        for item in base_items:
            self.assertIn(item, checklist)
        for item in solar_items:
            self.assertIn(item, checklist)
        
        # Ensure no items from other scenarios are included
        zombie_items = get_scenario_specific_items()["zombie_outbreak"]
        for item in zombie_items:
            self.assertNotIn(item, checklist)

    def test_generate_checklist_unknown_scenario(self):
        """Test that an unknown scenario defaults to the general catastrophe."""
        checklist = generate_checklist("unknown_alien_invasion")
        base_items = get_base_checklist()
        self.assertEqual(len(checklist), len(base_items))
        for item in base_items:
            self.assertIn(item, checklist)
        # Ensure no scenario-specific items are included for an unknown scenario
        scenario_specific = get_scenario_specific_items()
        for scenario_list in scenario_specific.values():
            for item in scenario_list:
                self.assertNotIn(item, checklist)

    # Mock rationale: Not applicable for this purely functional, self-contained utility.
    # The data is internal to the functions, making tests deterministic and offline.
    # If get_base_checklist or get_scenario_specific_items were reading from files,
    # we would mock file I/O. Since they return hardcoded lists/dicts, they are
    # inherently deterministic and offline.

if __name__ == '__main__':
    unittest.main()
