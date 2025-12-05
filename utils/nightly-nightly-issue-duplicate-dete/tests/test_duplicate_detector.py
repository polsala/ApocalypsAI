import unittest
import sys
from pathlib import Path

# Mock rationale: adjust sys.path to import the module from src
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from duplicate_detector import find_duplicates

class TestDuplicateDetector(unittest.TestCase):
    def test_no_duplicates(self):
        titles = ["Add feature X", "Fix bug Y", "Improve docs"]
        groups = find_duplicates(titles, threshold=0.8)
        self.assertEqual(groups, [])

    def test_simple_duplicates(self):
        titles = [
            "Add feature X",
            "Add feature X",
            "Fix bug Y",
            "Add feature X - duplicate",
            "Fix bug Y - duplicate",
        ]
        groups = find_duplicates(titles, threshold=0.8)
        # Expect two groups: indices 0,1,3 and indices 2,4
        expected = [[0, 1, 3], [2, 4]]
        self.assertEqual(groups, expected)

    def test_threshold(self):
        titles = ["Add feature X", "Add feature Y", "Add feature X"]
        groups = find_duplicates(titles, threshold=0.9)
        # With high threshold, only exact duplicates
        self.assertEqual(groups, [[0, 2]])

if __name__ == "__main__":
    unittest.main()
