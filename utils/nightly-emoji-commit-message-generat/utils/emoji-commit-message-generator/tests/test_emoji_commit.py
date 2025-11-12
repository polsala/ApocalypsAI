import os
import unittest
from src.emoji_commit import generate_message

class TestEmojiCommit(unittest.TestCase):
    def setUp(self):
        # Ensure a clean environment for each test
        os.environ.pop("EMOJI_SEED", None)

    def test_basic_message(self):
        msg = generate_message("Add unit tests")
        # The message should start with the description and contain exactly one emoji
        self.assertTrue(msg.startswith("Add unit tests "))
        self.assertEqual(len(msg.split()), 3)  # description + emoji

    def test_seed_changes_emoji(self):
        # Mock rationale: setting a seed should deterministically change the selected emoji
        os.environ["EMOJI_SEED"] = "seed123"
        msg1 = generate_message("Update docs")
        os.environ["EMOJI_SEED"] = "different"
        msg2 = generate_message("Update docs")
        self.assertNotEqual(msg1, msg2)

    def test_empty_description_raises(self):
        with self.assertRaises(ValueError):
            generate_message("")

if __name__ == "__main__":
    unittest.main()
