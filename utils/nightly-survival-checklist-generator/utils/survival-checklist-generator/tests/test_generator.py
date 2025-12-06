'''python
import sys
import pathlib
import unittest
from unittest.mock import patch

# Ensure the src directory is on the import path
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from generator import generate_checklist

class TestGenerateChecklist(unittest.TestCase):
    def test_known_scenario(self):
        checklist = generate_checklist("zombie")
        self.assertIn("Secure a fortified shelter", checklist)

    def test_unknown_scenario_returns_generic(self):
        checklist = generate_checklist("alien invasion")
        self.assertEqual(checklist, [
            "Assess the situation",
            "Secure shelter",
            "Gather water and food",
            "Establish communication",
            "Plan for long‑term survival",
        ])

    @patch('generator._DEFAULT_CHECKLISTS', {"custom": ["Do something"]})
    def test_custom_mapping_via_mock(self):
        # Mock rationale: replace internal data to ensure function respects the dict
        checklist = generate_checklist("custom")
        self.assertEqual(checklist, ["Do something"])

if __name__ == "__main__":
    unittest.main()
'''
