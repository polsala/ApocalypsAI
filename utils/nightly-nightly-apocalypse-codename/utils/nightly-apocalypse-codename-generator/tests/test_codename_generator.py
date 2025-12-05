import unittest
from unittest.mock import patch
from src.codename_generator import generate_codename, ADJECTIVES, NOUNS

class TestCodenameGenerator(unittest.TestCase):

    @patch('src.codename_generator.random.choice')
    def test_generate_codename_format(self, mock_choice):
        # Mock rationale: Ensure deterministic output for testing the format.
        # We want to control which adjective and noun are picked to verify the string format.
        mock_choice.side_effect = ["Rusty", "Beacon"]
        codename = generate_codename()
        self.assertEqual(codename, "Rusty-Beacon")
        self.assertEqual(mock_choice.call_count, 2) # Called once for adjective, once for noun

    @patch('src.codename_generator.random.choice')
    def test_generate_codename_contains_valid_parts(self, mock_choice):
        # Mock rationale: Ensure deterministic output to verify that parts come from expected lists.
        mock_choice.side_effect = ["Feral", "Vault"]
        codename = generate_codename()
        
        parts = codename.split('-')
        self.assertEqual(len(parts), 2)
        self.assertIn(parts[0], ADJECTIVES)
        self.assertIn(parts[1], NOUNS)

    @patch('src.codename_generator.random.choice')
    def test_generate_codename_is_string_and_not_empty(self, mock_choice):
        # Mock rationale: Ensure deterministic output to verify basic type and non-emptiness.
        mock_choice.side_effect = ["Shadow", "Drifter"]
        codename = generate_codename()
        self.assertIsInstance(codename, str)
        self.assertTrue(len(codename) > 0)

    @patch('src.codename_generator.random.choice')
    def test_generate_different_codenames(self, mock_choice):
        # Mock rationale: Simulate different random choices to ensure the function can produce varied outputs.
        # This tests the *potential* for variety, not actual randomness, by controlling the mock's return values.
        mock_choice.side_effect = [
            "Wasteland", "Nomad",  # First call
            "Scorched", "Shard"    # Second call
        ]
        codename1 = generate_codename()
        codename2 = generate_codename()
        self.assertEqual(codename1, "Wasteland-Nomad")
        self.assertEqual(codename2, "Scorched-Shard")
        self.assertNotEqual(codename1, codename2)
        self.assertEqual(mock_choice.call_count, 4)

    @patch('src.codename_generator.random.choice')
    def test_generate_with_all_adjectives_and_nouns(self, mock_choice):
        # Mock rationale: Verify that all possible adjectives and nouns can be chosen.
        # This ensures the lists are correctly integrated into the random choice mechanism.
        for adj in ADJECTIVES:
            for noun in NOUNS:
                mock_choice.side_effect = [adj, noun]
                codename = generate_codename()
                self.assertEqual(codename, f"{adj}-{noun}")
                # Reset mock_choice for the next iteration if needed, or ensure side_effect handles it.
                # For this test, side_effect is set per inner loop iteration, so it's fine.
