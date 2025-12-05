import unittest
from src import palette


class TestPalette(unittest.TestCase):
    def test_zero_colors(self):
        self.assertEqual(palette.generate_palette(0, seed=123), [])

    def test_negative_count_raises(self):
        with self.assertRaises(ValueError):
            palette.generate_palette(-1)

    def test_deterministic_output(self):
        # Mock rationale: replace random.Random with a deterministic sequence
        class MockRandom:
            def __init__(self, seed):
                self.values = [0x6A1B9A, 0xC0F5A2, 0x3E2F1D]
                self.idx = 0

            def randint(self, a, b):
                val = self.values[self.idx]
                self.idx = (self.idx + 1) % len(self.values)
                return val

        original_random = palette.random.Random
        palette.random.Random = MockRandom
        try:
            result = palette.generate_palette(3, seed=999)
            self.assertEqual(result, ["#6A1B9A", "#C0F5A2", "#3E2F1D"])
        finally:
            palette.random.Random = original_random


if __name__ == "__main__":
    unittest.main()
