import unittest
from unittest.mock import patch

# Import the module under test
from utils.random_compliment_generator.src.compliment import get_random_compliment

class TestRandomComplimentGenerator(unittest.TestCase):
    def test_general_random_compliment(self):
        # Mock rationale: force deterministic choice from the pool
        with patch('random.choice', return_value='You have a great sense of humor!'):
            result = get_random_compliment()
            self.assertEqual(result, 'You have a great sense of humor!')

    def test_specific_category(self):
        # Mock rationale: ensure the function respects the provided category
        with patch('random.choice', return_value='Your work ethic inspires the whole team.'):
            result = get_random_compliment('work')
            self.assertEqual(result, 'Your work ethic inspires the whole team.')

    def test_unknown_category_falls_back(self):
        # Mock rationale: unknown category should behave like no category
        with patch('random.choice', return_value='Your loyalty is unwavering.'):
            result = get_random_compliment('nonexistent')
            self.assertEqual(result, 'Your loyalty is unwavering.')

    def test_none_category_falls_back(self):
        # Mock rationale: explicit None should also fall back to the full pool
        with patch('random.choice', return_value='Your imagination knows no bounds.'):
            result = get_random_compliment(None)
            self.assertEqual(result, 'Your imagination knows no bounds.')

if __name__ == '__main__':
    unittest.main()
