import unittest
from unittest.mock import patch
import sys
import io
from src.generator import ApocalypsePetNameGenerator, main

class TestApocalypsePetNameGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = ApocalypsePetNameGenerator()

    @patch('random.choice')
    def test_generate_single_name_pattern_1(self, mock_choice):
        # Mock rationale: Ensure deterministic output for pattern 1 (Adjective + Noun_Core).
        # The first call to random.choice determines the pattern (1).
        # The second call determines the adjective ("Rusty").
        # The third call determines the noun_core ("Bolt").
        mock_choice.side_effect = [1, "Rusty", "Bolt"]
        name = self.generator._generate_single_name()
        self.assertEqual(name, "Rusty Bolt")
        self.assertEqual(mock_choice.call_count, 3)

    @patch('random.choice')
    def test_generate_single_name_pattern_2(self, mock_choice):
        # Mock rationale: Ensure deterministic output for pattern 2 (Noun_Core + Suffix).
        # The first call to random.choice determines the pattern (2).
        # The second call determines the noun_core ("Cinder").
        # The third call determines the suffix ("-Paw").
        mock_choice.side_effect = [2, "Cinder", "-Paw"]
        name = self.generator._generate_single_name()
        self.assertEqual(name, "Cinder-Paw")
        self.assertEqual(mock_choice.call_count, 3)

    @patch('random.choice')
    def test_generate_single_name_pattern_3(self, mock_choice):
        # Mock rationale: Ensure deterministic output for pattern 3 (Noun_Core only).
        # The first call to random.choice determines the pattern (3).
        # The second call determines the noun_core ("Prowler").
        mock_choice.side_effect = [3, "Prowler"]
        name = self.generator._generate_single_name()
        self.assertEqual(name, "Prowler")
        self.assertEqual(mock_choice.call_count, 2)

    @patch('random.choice')
    def test_generate_multiple_names(self, mock_choice):
        # Mock rationale: Ensure deterministic output for multiple name generation.
        # Sequence of choices:
        # 1. Pattern 1, Adjective "Shadow", Noun "Hunter"
        # 2. Pattern 2, Noun "Ghost", Suffix "-Eye"
        # 3. Pattern 3, Noun "Stalker"
        mock_choice.side_effect = [
            1, "Shadow", "Hunter",  # First name: Shadow Hunter
            2, "Ghost", "-Eye",    # Second name: Ghost-Eye
            3, "Stalker"           # Third name: Stalker
        ]
        names = self.generator.generate_names(count=3);
        self.assertEqual(len(names), 3)
        self.assertEqual(names[0], "Shadow Hunter")
        self.assertEqual(names[1], "Ghost-Eye")
        self.assertEqual(names[2], "Stalker")
        self.assertEqual(mock_choice.call_count, 3 + 3 + 2) # 3 calls for first, 3 for second, 2 for third

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.generator.ApocalypsePetNameGenerator.generate_names')
    def test_main_single_name(self, mock_generate_names, mock_parse_args, mock_stdout):
        # Mock rationale: Simulate CLI arguments and capture stdout for main function testing.
        mock_parse_args.return_value.count = 1
        mock_generate_names.return_value = ["TestNameOne"]

        main()
        self.assertEqual(mock_stdout.getvalue().strip(), "TestNameOne")
        mock_generate_names.assert_called_once_with(1)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.generator.ApocalypsePetNameGenerator.generate_names')
    def test_main_multiple_names(self, mock_generate_names, mock_parse_args, mock_stdout):
        # Mock rationale: Simulate CLI arguments and capture stdout for main function testing.
        mock_parse_args.return_value.count = 3
        mock_generate_names.return_value = ["NameA", "NameB", "NameC"]

        main()
        expected_output = "NameA\nNameB\nNameC"
        self.assertEqual(mock_stdout.getvalue().strip(), expected_output)
        mock_generate_names.assert_called_once_with(3)

if __name__ == '__main__':
    unittest.main()
