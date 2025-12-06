import unittest
import datetime

# Mock rationale: Tests use fixed historic dates with known moon phases.
# The algorithm is deterministic and offline, so these assertions are stable.

from utils.nightly-moon-phase-emoji.src.moon_phase import get_moon_phase

class TestMoonPhase(unittest.TestCase):
    def test_new_moon(self):
        # 2023‑01‑21 was a New Moon
        d = datetime.date(2023, 1, 21)
        phase, emoji = get_moon_phase(d)
        self.assertEqual(phase, "New Moon")
        self.assertEqual(emoji, "🌑")

    def test_first_quarter(self):
        # 2023‑01‑28 was First Quarter
        d = datetime.date(2023, 1, 28)
        phase, emoji = get_moon_phase(d)
        self.assertEqual(phase, "First Quarter")
        self.assertEqual(emoji, "🌓")

    def test_full_moon(self):
        # 2023‑02‑05 was Full Moon
        d = datetime.date(2023, 2, 5)
        phase, emoji = get_moon_phase(d)
        self.assertEqual(phase, "Full Moon")
        self.assertEqual(emoji, "🌕")

    def test_last_quarter(self):
        # 2023‑02‑13 was Last Quarter
        d = datetime.date(2023, 2, 13)
        phase, emoji = get_moon_phase(d)
        self.assertEqual(phase, "Last Quarter")
        self.assertEqual(emoji, "🌗")

    def test_today_cli(self):
        # Ensure the CLI runs without error for today (no assertion on output).
        import subprocess, sys, os
        script_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "moon_phase.py"
        )
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(result.stdout.strip())

if __name__ == "__main__":
    unittest.main()
