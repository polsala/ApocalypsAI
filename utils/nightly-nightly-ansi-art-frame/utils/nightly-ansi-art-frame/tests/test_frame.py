import unittest
from utils.nightly-ansi_art_frame.src.frame import frame_text, _choose_style

class TestAnsiArtFrame(unittest.TestCase):
    def test_single_style(self):
        txt = "Hi"
        expected = (
            "┌────┐\n"
            "│ Hi │\n"
            "└────┘"
        )
        self.assertEqual(frame_text(txt, style="single"), expected)

    def test_double_style_multi_line(self):
        txt = "Line1\nLine2"
        expected = (
            "╔───────╗\n"
            "║ Line1 │\n"
            "║ Line2 │\n"
            "╚───────╝"
        )
        self.assertEqual(frame_text(txt, style="double"), expected)

    def test_auto_style_is_deterministic(self):
        txt = "deterministic"
        first = _choose_style(txt)
        second = _choose_style(txt)
        # Mock rationale: we rely on the deterministic hash function; no external state.
        self.assertEqual(first, second)
        # Ensure the chosen style is one of the allowed keys.
        self.assertIn(first, {"single", "double", "bold"})

if __name__ == "__main__":
    unittest.main()
