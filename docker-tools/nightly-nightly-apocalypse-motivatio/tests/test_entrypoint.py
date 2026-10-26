import os
import subprocess
import unittest

class TestEntryPoint(unittest.TestCase):
    def setUp(self):
        # Path to the entrypoint script relative to this test file
        self.script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'entrypoint.sh'))
        # Ensure the script is executable
        os.chmod(self.script_path, 0o755)

    def test_fixed_index(self):
        """# Mock rationale: use a fixed index to get a deterministic message"""
        env = os.environ.copy()
        env['MOTIVATION_INDEX'] = '0'
        result = subprocess.run([self.script_path], env=env, capture_output=True, text=True)
        self.assertEqual(result.stdout.strip(), "Rise, wanderer! The sun may be a memory, but your spirit still burns.")

    def test_out_of_range_index(self):
        """# Mock rationale: ensure script does not crash on an out‑of‑range index"""
        env = os.environ.copy()
        env['MOTIVATION_INDEX'] = '100'
        result = subprocess.run([self.script_path], env=env, capture_output=True, text=True)
        # When the index is out of range, sed returns nothing, so output should be empty
        self.assertEqual(result.stdout.strip(), "")

if __name__ == '__main__':
    unittest.main()
