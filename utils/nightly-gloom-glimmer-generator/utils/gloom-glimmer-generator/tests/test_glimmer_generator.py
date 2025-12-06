import unittest
from unittest import mock
import sys
import os

# Add the src directory to the Python path to allow importing glimmer_generator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from glimmer_generator import generate_glimmer

class TestGlimmerGenerator(unittest.TestCase):

    @mock.patch('random.choice')
    def test_generate_glimmer_deterministic(self, mock_choice):
        # Mock rationale: We need to ensure that `generate_glimmer` returns a predictable
        # value for testing, even though `random.choice` is inherently non-deterministic.
        # By mocking `random.choice`, we can control its return value and verify
        # that our function correctly uses it.

        expected_glimmer = "Remember to appreciate the resilience of that mutated daisy."
        mock_choice.return_value = expected_glimmer

        result = generate_glimmer()
        self.assertEqual(result, expected_glimmer)
        mock_choice.assert_called_once() # Ensure random.choice was indeed called

    @mock.patch('random.choice')
    def test_generate_glimmer_another_deterministic_case(self, mock_choice):
        # Mock rationale: Similar to the above, this test ensures determinism
        # by controlling the output of `random.choice` for a different expected value.

        expected_glimmer = "Organize your scavenged bottle caps by color. It's surprisingly therapeutic!"
        mock_choice.return_value = expected_glimmer

        result = generate_glimmer()
        self.assertEqual(result, expected_glimmer)
        mock_choice.assert_called_once()

    def test_generate_glimmer_returns_string(self):
        # This test doesn't need mocking as it only checks the type of the return value.
        result = generate_glimmer()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0) # Ensure it's not an empty string

if __name__ == '__main__':
    unittest.main()
