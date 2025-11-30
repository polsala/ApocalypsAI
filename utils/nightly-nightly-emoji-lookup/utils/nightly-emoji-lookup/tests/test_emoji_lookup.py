import unittest
from pathlib import Path

# Mock rationale: import the module from the sibling src directory without installing a package.
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from emoji_lookup import get_name

class TestEmojiLookup(unittest.TestCase):
    def test_known_emoji(self):
        self.assertEqual(get_name("😀"), "grinning face")
        self.assertEqual(get_name("🚀"), "rocket")
        self.assertEqual(get_name("❤️"), "red heart")

    def test_unknown_emoji(self):
        self.assertIsNone(get_name("🦄"))  # Not in the static map

    def test_cli_success(self):
        # Run the module as a script and capture stdout.
        import subprocess, json
        result = subprocess.run(
            [sys.executable, "-m", "emoji_lookup", "👍"],
            cwd=str(Path(__file__).resolve().parents[1] / "src"),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "thumbs up")

    def test_cli_failure(self):
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "emoji_lookup", "🦄"],
            cwd=str(Path(__file__).resolve().parents[1] / "src"),
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unknown emoji", result.stderr)

if __name__ == "__main__":
    unittest.main()
