import unittest
from unittest import mock
import src.generate_message as gen

class TestGenerateMessage(unittest.TestCase):
    def test_mocked_output(self):
        # Mock rationale: ensure deterministic output without relying on RNG
        def mock_choice(seq):
            mapping = {
                tuple(gen.TEMPLATES): "{verb} the {adjective} {noun}",
                tuple(gen.VERBS): "refactor",
                tuple(gen.ADJECTIVES): "fluffy",
                tuple(gen.NOUNS): "unicorn",
            }
            return mapping[tuple(seq)]
        with mock.patch('random.choice', side_effect=mock_choice):
            self.assertEqual(gen.generate_message(), "refactor the fluffy unicorn")

if __name__ == "__main__":
    unittest.main()
