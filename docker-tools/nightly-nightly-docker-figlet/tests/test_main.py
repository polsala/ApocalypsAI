import unittest
import subprocess
import sys
import os

class TestFigletCLI(unittest.TestCase):
    def test_basic_render(self):
        # Run the script directly
        result = subprocess.run([sys.executable, os.path.join("src", "main.py"), "HELLO"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        # The output should contain the ASCII art for HELLO in standard font
        self.assertIn(" _   _      _ _ ", output)  # part of the expected art

if __name__ == "__main__":
    unittest.main()
