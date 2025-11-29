import unittest
from unittest import mock

# Mock rationale: No external services are used; we only need to import the module.
from src.color_namer import get_color_name

class TestHexColorNamer(unittest.TestCase):
    def test_lookup_table(self):
        # Known entries should return the exact whimsical name
        self.assertEqual(get_color_name("#ff0000"), "Blazing Ruby")
        self.assertEqual(get_color_name("ff7f00"), "Fiery Tangerine")
        self.assertEqual(get_color_name("#00FFFF"), "Aqua Whisper")

    def test_fallback_determinism(self):
        # Colours not in the lookup table fall back to a generic name based on hue.
        # The mapping is deterministic, so the same input always yields the same output.
        name1 = get_color_name("#123456")
        name2 = get_color_name("#123456")
        self.assertEqual(name1, name2)
        # Ensure the fallback name is one of the generic bucket names
        self.assertIn(name1, [
            "Crimson Dawn",
            "Sunset Orange",
            "Lemon Zest",
            "Spring Green",
            "Ocean Blue",
            "Violet Dream",
            "Rose Pink",
            "Cool Cyan",
            "Warm Amber",
            "Deep Indigo",
        ])

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            get_color_name("not-a-hex")
        with self.assertRaises(ValueError):
            get_color_name("#12345")  # Too short
        with self.assertRaises(ValueError):
            get_color_name("#GGHHII")  # Invalid characters

if __name__ == "__main__":
    unittest.main()
