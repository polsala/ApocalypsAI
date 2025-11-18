import unittest
from unittest.mock import patch, MagicMock
import io
import sys

# Import the functions from the scribe module
from src.scribe import get_random_tip, get_tips_by_category, list_categories, display_tip, SURVIVAL_TIPS, main

class TestSurvivalSkillScribe(unittest.TestCase):

    @patch('random.choice')
    def test_get_random_tip(self, mock_choice):
        # Mock rationale: random.choice is used to pick a random tip. 
        # Mocking it ensures deterministic test results by controlling which tip is 'chosen'.
        expected_tip = {"category": "Test", "tip": "This is a test tip."}
        mock_choice.return_value = expected_tip
        
        tip = get_random_tip()
        self.assertEqual(tip, expected_tip)
        mock_choice.assert_called_once_with(SURVIVAL_TIPS)

    def test_get_tips_by_category(self):
        # Test with an existing category
        water_tips = get_tips_by_category("Water")
        self.assertTrue(len(water_tips) > 0)
        for tip in water_tips:
            self.assertEqual(tip["category"].lower(), "water")

        # Test with a non-existent category
        no_tips = get_tips_by_category("NonExistentCategory")
        self.assertEqual(len(no_tips), 0)

        # Test case-insensitivity
        water_tips_case_insensitive = get_tips_by_category("wAtEr")
        self.assertTrue(len(water_tips_case_insensitive) > 0)
        self.assertEqual(len(water_tips_case_insensitive), len(water_tips))

    def test_list_categories(self):
        categories = list_categories()
        self.assertIsInstance(categories, list)
        self.assertTrue(len(categories) > 0)
        # Check for some expected categories
        self.assertIn("Water", categories)
        self.assertIn("Shelter", categories)
        self.assertIn("Morale", categories)
        # Ensure categories are unique and sorted
        self.assertEqual(categories, sorted(list(set(tip["category"] for tip in SURVIVAL_TIPS))))

    def test_display_tip(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output # Redirect stdout

        test_tip = {"category": "Test", "tip": "This is a test tip for display."}
        display_tip(test_tip)

        sys.stdout = sys.__stdout__ # Reset stdout
        output = captured_output.getvalue()

        self.assertIn("--- Survival Tip ---", output)
        self.assertIn("Category: Test", output)
        self.assertIn("Tip: This is a test tip for display.", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.scribe.get_random_tip')
    def test_main_random_tip(self, mock_get_random_tip, mock_parse_args, mock_stdout):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to simulate CLI arguments.
        # src.scribe.get_random_tip is mocked to control the tip returned, ensuring deterministic output.
        mock_parse_args.return_value = MagicMock(category=None, list_categories=False)
        mock_get_random_tip.return_value = {"category": "Random", "tip": "A random tip."}

        main()
        output = mock_stdout.getvalue()
        self.assertIn("Category: Random", output)
        self.assertIn("Tip: A random tip.", output)
        mock_get_random_tip.assert_called_once()

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.scribe.get_tips_by_category')
    @patch('src.scribe.random.choice')
    def test_main_category_tip(self, mock_random_choice, mock_get_tips_by_category, mock_parse_args, mock_stdout):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to simulate CLI arguments.
        # src.scribe.get_tips_by_category is mocked to control the list of tips for a category.
        # random.choice is mocked to pick a specific tip from the mocked list.
        mock_parse_args.return_value = MagicMock(category="Water", list_categories=False)
        mock_get_tips_by_category.return_value = [{"category": "Water", "tip": "Drink water."}]
        mock_random_choice.return_value = {"category": "Water", "tip": "Drink water."}

        main()
        output = mock_stdout.getvalue()
        self.assertIn("Category: Water", output)
        self.assertIn("Tip: Drink water.", output)
        mock_get_tips_by_category.assert_called_once_with("Water")
        mock_random_choice.assert_called_once_with([{"category": "Water", "tip": "Drink water."}]
)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_category_not_found(self, mock_parse_args, mock_stdout):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to simulate CLI arguments.
        mock_parse_args.return_value = MagicMock(category="NonExistent", list_categories=False)

        main()
        output = mock_stdout.getvalue()
        self.assertIn("No tips found for category: NonExistent", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.scribe.list_categories')
    def test_main_list_categories(self, mock_list_categories, mock_parse_args, mock_stdout):
        # Mock rationale: argparse.ArgumentParser.parse_args is mocked to simulate CLI arguments.
        # src.scribe.list_categories is mocked to control the list of categories returned.
        mock_parse_args.return_value = MagicMock(category=None, list_categories=True)
        mock_list_categories.return_value = ["Food", "Shelter"]

        main()
        output = mock_stdout.getvalue()
        self.assertIn("Available Categories:", output)
        self.assertIn("- Food", output)
        self.assertIn("- Shelter", output)
        mock_list_categories.assert_called_once()
