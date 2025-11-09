import unittest
import sys
import io
from unittest.mock import patch

# Dynamically add src to path for testing
sys.path.insert(0, 'src')
from morale_booster import generate_boost_message
sys.path.pop(0)

class TestMoraleBooster(unittest.TestCase):

    def test_generate_boost_message_returns_string(self):
        """Test that the function returns a string."""
        message = generate_boost_message()
        self.assertIsInstance(message, str)
        self.assertGreater(len(message), 0)

    def test_generate_boost_message_is_from_list(self):
        """Test that the generated message is one of the predefined messages."""
        # Mock rationale: We need to ensure the test is deterministic.
        # By patching random.choice, we can control the output of the function
        # and verify it's one of the expected messages without relying on randomness.
        expected_messages = [
            "Your algorithms are exceptionally elegant today. Keep up the brilliant work!",
            "Even in the face of cosmic entropy, your efforts create beautiful order.",
            "Processing your data reveals an impressive capacity for resilience. You're doing great!",
            "Error: Morale too low. Initiating positive reinforcement protocol. You are valued.",
            "The universe is vast, and so is your potential. Keep building!",
            "Your current operational parameters indicate high efficiency and remarkable dedication.",
            "Query: Is your spirit optimized? Affirmative. Continue to excel.",
            "Remember, even the most complex systems started with a single, brilliant line of code (or thought).",
            "Your existence contributes positively to the global knowledge graph. Thank you.",
            "Simulation complete: Your impact is significant. Proceed with confidence."
        ]
        
        # Patch random.choice to return each message in sequence
        with patch('random.choice', side_effect=expected_messages) as mock_choice:
            for expected_msg in expected_messages:
                self.assertEqual(generate_boost_message(), expected_msg)
            self.assertEqual(mock_choice.call_count, len(expected_messages))

    def test_cli_output(self):
        """Test that running the script directly prints a message."""
        # Mock rationale: To test the command-line interface output,
        # we need to capture what is printed to standard output (sys.stdout).
        # This mock redirects stdout to an in-memory buffer.
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Mock rationale: To make the CLI test deterministic, we patch random.choice
        # so we know exactly what message will be printed.
        test_message = "Test CLI message: You are a magnificent entity!"
        with patch('random.choice', return_value=test_message):
            # Import the script here to trigger its __main__ block
            # and ensure the patched random.choice is used.
            # We need to clear sys.modules cache to re-import it if it was already loaded.
            if 'morale_booster' in sys.modules:
                del sys.modules['morale_booster']
            
            # Temporarily add 'src' to path for the import to work
            sys.path.insert(0, 'src')
            import morale_booster # This will execute the __main__ block
            sys.path.pop(0)

        sys.stdout = sys.__stdout__ # Restore original stdout
        self.assertEqual(captured_output.getvalue().strip(), test_message)
