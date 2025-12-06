import unittest
from unittest.mock import patch
import io
from src.randomizer import RubbleRouser, main

class TestRubbleRouser(unittest.TestCase):

    def setUp(self):
        self.rouser = RubbleRouser()

    @patch('random.choice')
    def test_get_random_find_specific_category(self, mock_choice):
        # Mock rationale: Ensure deterministic output for a specific category.
        # We want to control which item is chosen from the list.
        mock_choice.side_effect = [
            self.rouser.categories['item'][0], # For item category
            self.rouser.categories['encounter'][0], # For encounter category
            self.rouser.categories['location'][0] # For location category
        ]

        category_name, find = self.rouser.get_random_find('item')
        self.assertEqual(category_name, 'item')
        self.assertEqual(find, "A half-eaten can of peaches (still good!)")
        mock_choice.assert_called_with(self.rouser.categories['item'])

        category_name, find = self.rouser.get_random_find('encounter')
        self.assertEqual(category_name, 'encounter')
        self.assertEqual(find, "A lone, wary survivor seeking trade")
        mock_choice.assert_called_with(self.rouser.categories['encounter'])

        category_name, find = self.rouser.get_random_find('location')
        self.assertEqual(category_name, 'location')
        self.assertEqual(find, "A collapsed overpass, now a makeshift shelter")
        mock_choice.assert_called_with(self.rouser.categories['location'])

    @patch('random.choice')
    def test_get_random_find_no_category_specified(self, mock_choice):
        # Mock rationale: Ensure deterministic output when no category is specified.
        # We need to control both the chosen category and the item within it.
        mock_choice.side_effect = [
            'item', # First call: choose category 'item'
            self.rouser.categories['item'][1] # Second call: choose item from 'item' category
        ]

        category_name, find = self.rouser.get_random_find()
        self.assertEqual(category_name, 'item')
        self.assertEqual(find, "A rusty multi-tool, missing one blade")
        self.assertEqual(mock_choice.call_count, 2)
        mock_choice.assert_any_call(list(self.rouser.categories.keys()))
        mock_choice.assert_any_call(self.rouser.categories['item'])

    def test_get_random_find_invalid_category(self):
        with self.assertRaisesRegex(ValueError, "Invalid category: nonexistent. Choose from item, encounter, location"):
            self.rouser.get_random_find('nonexistent')

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('random.choice')
    def test_main_specific_category_output(self, mock_random_choice, mock_parse_args, mock_stdout):
        # Mock rationale: Simulate command-line arguments and control random output
        # to verify the script's print statements.
        mock_parse_args.return_value.category = 'item'
        mock_random_choice.return_value = self.rouser.categories['item'][2] # A tattered map...

        main()
        expected_output = "Category: Item\nFind: A tattered map of the local area, with cryptic annotations\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('random.choice')
    def test_main_no_category_output(self, mock_random_choice, mock_parse_args, mock_stdout):
        # Mock rationale: Simulate command-line arguments and control random output
        # to verify the script's print statements when no category is specified.
        mock_parse_args.return_value.category = None
        mock_random_choice.side_effect = [
            'encounter', # Choose category 'encounter'
            self.rouser.categories['encounter'][3] # Choose item from 'encounter' category
        ]

        main()
        expected_output = "Category: Encounter\nFind: A small, overgrown garden plot\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
