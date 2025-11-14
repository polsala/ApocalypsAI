import unittest
from src.checklist_generator import generate_checklist

class TestChecklistGenerator(unittest.TestCase):

    def test_zombie_scenario(self):
        # Mock rationale: The function is deterministic based on input and internal data.
        # No external calls or random elements to mock.
        checklist = generate_checklist("zombie")
        self.assertIn("# Apocalypse Preparedness Checklist: Zombie", checklist)
        self.assertIn("- [ ] Water (1 gallon per person per day, 3-day supply minimum)", checklist)
        self.assertIn("- [ ] Crowbar or blunt weapon (for 'persuasion')", checklist)
        self.assertIn("- [ ] A copy of 'The Zombie Survival Guide'", checklist)
        self.assertNotIn("**Warning**", checklist)

    def test_meteor_scenario(self):
        # Mock rationale: The function is deterministic based on input and internal data.
        # No external calls or random elements to mock.
        checklist = generate_checklist("meteor")
        self.assertIn("# Apocalypse Preparedness Checklist: Meteor", checklist)
        self.assertIn("- [ ] Non-perishable food (3-day supply minimum)", checklist)
        self.assertIn("- [ ] Hard hat or helmet (for falling debris)", checklist)
        self.assertIn("- [ ] Telescope (to watch the show... from a safe distance)", checklist)
        self.assertNotIn("**Warning**", checklist)

    def test_ai_uprising_scenario(self):
        # Mock rationale: The function is deterministic based on input and internal data.
        # No external calls or random elements to mock.
        checklist = generate_checklist("ai_uprising")
        self.assertIn("# Apocalypse Preparedness Checklist: Ai Uprising", checklist)
        self.assertIn("- [ ] First aid kit (with extra meds)", checklist)
        self.assertIn("- [ ] EMP-proof Faraday cage (for electronics)", checklist)
        self.assertIn("- [ ] A good old-fashioned axe (for 'rebooting' rogue servers')", checklist)
        self.assertNotIn("**Warning**", checklist)

    def test_general_scenario(self):
        # Mock rationale: The function is deterministic based on input and internal data.
        # No external calls or random elements to mock.
        checklist = generate_checklist("general")
        self.assertIn("# Apocalypse Preparedness Checklist: General", checklist)
        self.assertIn("- [ ] Water (1 gallon per person per day, 3-day supply minimum)", checklist)
        self.assertIn("- [ ] Duct tape (the ultimate survival tool)", checklist)
        self.assertNotIn("- [ ] Crowbar or blunt weapon", checklist) # Specific to zombie
        self.assertNotIn("**Warning**", checklist)

    def test_unknown_scenario(self):
        # Mock rationale: The function is deterministic based on input and internal data.
        # No external calls or random elements to mock.
        checklist = generate_checklist("alien_invasion")
        self.assertIn("# Apocalypse Preparedness Checklist: Alien Invasion", checklist)
        self.assertIn("- [ ] Water (1 gallon per person per day, 3-day supply minimum)", checklist)
        self.assertIn("**Warning**: Unknown or unsupported specific scenario 'alien_invasion'. Generating a general preparedness checklist.", checklist)
        self.assertNotIn("- [ ] Crowbar or blunt weapon", checklist) # Should not include specific items

    def test_scenario_with_extra_words(self):
        # Mock rationale: The function is deterministic based on input and internal data.
        # No external calls or random elements to mock.
        checklist_zombie_apocalypse = generate_checklist("zombie apocalypse")
        self.assertIn("# Apocalypse Preparedness Checklist: Zombie Apocalypse", checklist_zombie_apocalypse)
        self.assertIn("- [ ] Crowbar or blunt weapon (for 'persuasion')", checklist_zombie_apocalypse) # Should include zombie specific items
        self.assertNotIn("**Warning**", checklist_zombie_apocalypse)

        checklist_ai_robot_uprising = generate_checklist("AI Robot Uprising")
        self.assertIn("# Apocalypse Preparedness Checklist: Ai Robot Uprising", checklist_ai_robot_uprising)
        self.assertIn("- [ ] EMP-proof Faraday cage (for electronics)", checklist_ai_robot_uprising) # Should include AI specific items
        self.assertNotIn("**Warning**", checklist_ai_robot_uprising)

    def test_case_insensitivity(self):
        # Mock rationale: The function is deterministic based on input and internal data.
        # No external calls or random elements to mock.
        checklist_lower = generate_checklist("zombie")
        checklist_upper = generate_checklist("ZOMBIE")
        checklist_mixed = generate_checklist("zOmBiE")
        self.assertEqual(checklist_lower, checklist_upper)
        self.assertEqual(checklist_lower, checklist_mixed)
        self.assertIn("# Apocalypse Preparedness Checklist: Zombie", checklist_mixed)
        self.assertIn("- [ ] Crowbar or blunt weapon", checklist_mixed)
        self.assertNotIn("**Warning**", checklist_mixed)
