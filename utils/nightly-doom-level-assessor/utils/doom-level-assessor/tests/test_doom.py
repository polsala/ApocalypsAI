import unittest
import sys
from pathlib import Path

# Add the src directory to ``sys.path`` so the module can be imported.
src_path = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(src_path))

from doom import compute_doom_level

class TestDoomLevelAssessor(unittest.TestCase):
    def test_safe(self):
        # 15 years before apocalypse → Safe
        self.assertEqual(compute_doom_level("2084-12-30"), "Safe")

    def test_warning(self):
        # 5 years before apocalypse → Warning
        self.assertEqual(compute_doom_level("2094-12-31"), "Warning")

    def test_critical(self):
        # 1 year before apocalypse → Critical
        self.assertEqual(compute_doom_level("2098-12-31"), "Critical")

    def test_apocalypse(self):
        # 1 month before apocalypse → Apocalypse
        self.assertEqual(compute_doom_level("2099-12-01"), "Apocalypse")

    def test_already_passed(self):
        # After apocalypse date
        self.assertEqual(compute_doom_level("2100-01-01"), "Already passed")

    def test_invalid_format(self):
        # Mock rationale: ensure ValueError is raised for bad format without any network calls.
        with self.assertRaises(ValueError):
            compute_doom_level("2025/01/01")

if __name__ == "__main__":
    unittest.main()
