import unittest
import os
import sys

# Add src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import tip

class TestTip(unittest.TestCase):
    def test_get_tip_returns_known(self):
        tip_str = tip.get_tip()
        self.assertIn(tip_str, tip._TIPS)

    def test_dockerfile_contains_entrypoint(self):
        dockerfile_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Dockerfile"))
        with open(dockerfile_path, "r") as f:
            content = f.read()
        self.assertIn("ENTRYPOINT", content)

if __name__ == "__main__":
    unittest.main()
