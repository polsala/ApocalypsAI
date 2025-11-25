import unittest
from unittest import mock

# Mock rationale: we replace ``random.randint`` to return a predictable sequence
# so the test runs offline and deterministically.

from src.generator import generate_color, classify_brightness


class TestHexColorGenerator(unittest.TestCase):
    @mock.patch('random.randint')
    def test_generate_color_deterministic(self, mock_randint):
        # Define a deterministic sequence: R=10, G=20, B=30
        mock_randint.side_effect = [10, 20, 30]
        colour = generate_color()
        self.assertEqual(colour, '#0A141E')
        # Ensure ``randint`` was called three times
        self.assertEqual(mock_randint.call_count, 3)

    def test_generate_color_with_seed(self):
        # Using a seed should produce the same colour across runs
        colour1 = generate_color(seed=12345)
        colour2 = generate_color(seed=12345)
        self.assertEqual(colour1, colour2)
        # Different seed yields (likely) different colour
        colour3 = generate_color(seed=54321)
        self.assertNotEqual(colour1, colour3)

    def test_classify_brightness_light(self):
        self.assertEqual(classify_brightness('#FFFFFF'), 'light')
        self.assertEqual(classify_brightness('#E0E0E0'), 'light')

    def test_classify_brightness_dark(self):
        self.assertEqual(classify_brightness('#000000'), 'dark')
        self.assertEqual(classify_brightness('#101010'), 'dark')

    def test_classify_brightness_neutral(self):
        self.assertEqual(classify_brightness('#777777'), 'neutral')
        self.assertEqual(classify_brightness('#808080'), 'neutral')

    def test_classify_brightness_invalid(self):
        with self.assertRaises(ValueError):
            classify_brightness('not-a-hex')
        with self.assertRaises(ValueError):
            classify_brightness('#123AB')  # wrong length


if __name__ == '__main__':
    unittest.main()
