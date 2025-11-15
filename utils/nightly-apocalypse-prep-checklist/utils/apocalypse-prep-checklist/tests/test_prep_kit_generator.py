import unittest
import sys
import os

# Add the src directory to the Python path to allow importing prep_kit_generator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from prep_kit_generator import generate_checklist, get_scenario_data

class TestPrepKitGenerator(unittest.TestCase):

    def test_zombie_apocalypse_checklist(self):
        # Mock rationale: The get_scenario_data function is deterministic and returns hardcoded data.
        # No external dependencies or random elements, so direct testing is sufficient.
        expected_items = get_scenario_data()["zombie-apocalypse"]
        expected_output = "# Zombie Apocalypse Prep Checklist\n\n" + "\n".join([f"- [ ] {item}" for item in expected_items])
        self.assertEqual(generate_checklist("zombie-apocalypse"), expected_output)

    def test_ai_uprising_checklist(self):
        # Mock rationale: Same as above, data is internal and deterministic.
        expected_items = get_scenario_data()["ai-uprising"]
        expected_output = "# Ai Uprising Prep Checklist\n\n" + "\n".join([f"- [ ] {item}" for item in expected_items])
        self.assertEqual(generate_checklist("ai-uprising"), expected_output)

    def test_solar_flare_checklist(self):
        # Mock rationale: Same as above, data is internal and deterministic.
        expected_items = get_scenario_data()["solar-flare"]
        expected_output = "# Solar Flare Prep Checklist\n\n" + "\n".join([f"- [ ] {item}" for item in expected_items])
        self.assertEqual(generate_checklist("solar-flare"), expected_output)

    def test_unknown_scenario_checklist(self):
        # Mock rationale: Same as above, data is internal and deterministic.
        expected_items = get_scenario_data()["_default_"]
        expected_output = "# Generic Apocalypse Prep Checklist\n\n" + "\n".join([f"- [ ] {item}" for item in expected_items])
        self.assertEqual(generate_checklist("unknown-alien-invasion"), expected_output)
        self.assertEqual(generate_checklist("non-existent-doom"), expected_output)

    def test_case_insensitivity(self):
        # Mock rationale: Same as above, data is internal and deterministic.
        expected_items = get_scenario_data()["zombie-apocalypse"]
        expected_output = "# Zombie Apocalypse Prep Checklist\n\n" + "\n".join([f"- [ ] {item}" for item in expected_items])
        self.assertEqual(generate_checklist("ZOMBIE-APOCALYPSE"), expected_output)
        self.assertEqual(generate_checklist("zOmBiE-aPoCaLyPsE"), expected_output)

if __name__ == '__main__':
    unittest.main()
