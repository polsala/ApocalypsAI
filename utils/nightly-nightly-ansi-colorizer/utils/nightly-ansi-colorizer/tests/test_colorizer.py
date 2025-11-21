import unittest
from utils.nightly-ansi-colorizer.src.colorizer import colorize, RED, YELLOW, GREEN, RESET

class TestAnsiColorizer(unittest.TestCase):
    def test_basic_replacements(self):
        input_text = "Info: all good. Warning: low battery. Error: crash."
        expected = (
            f"{GREEN}Info{RESET}: all good. "
            f"{YELLOW}Warning{RESET}: low battery. "
            f"{RED}Error{RESET}: crash."
        )
        self.assertEqual(colorize(input_text), expected)

    def test_case_insensitivity(self):
        input_text = "INFO, warning, ErRoR"
        expected = f"{GREEN}INFO{RESET}, {YELLOW}warning{RESET}, {RED}ErRoR{RESET}"
        self.assertEqual(colorize(input_text), expected)

    def test_no_keywords(self):
        input_text = "All systems operational."
        self.assertEqual(colorize(input_text), input_text)

    def test_multiple_occurrences(self):
        input_text = "error error error"
        coloured = f"{RED}error{RESET} {RED}error{RESET} {RED}error{RESET}"
        self.assertEqual(colorize(input_text), coloured)

    # Mock rationale: No external resources are accessed; all tests are deterministic.

if __name__ == "__main__":
    unittest.main()
