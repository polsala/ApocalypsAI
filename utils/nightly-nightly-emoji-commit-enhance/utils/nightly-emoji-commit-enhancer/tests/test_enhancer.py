import unittest
from unittest.mock import patch

# Import the module using its full package path.
from utils.nightly-emoji-commit-enhancer.src.enhancer import enhance_message


class TestEmojiCommitEnhancer(unittest.TestCase):
    @patch('random.choice')
    def test_enhance_feat(self, mock_choice):
        mock_choice.return_value = '🚀'  # Mock rationale: deterministic emoji for test
        msg = "feat: add login"
        result = enhance_message(msg)
        self.assertEqual(result, "feat: add login 🚀")
        mock_choice.assert_called_once_with(["🚀", "✨", "🆕"])

    @patch('random.choice')
    def test_enhance_fix(self, mock_choice):
        mock_choice.return_value = '🐛'  # Mock rationale: deterministic emoji for test
        msg = "fix: correct typo"
        result = enhance_message(msg)
        self.assertEqual(result, "fix: correct typo 🐛")
        mock_choice.assert_called_once_with(["🐛", "🔧", "🩹"])

    @patch('random.choice')
    def test_enhance_unknown(self, mock_choice):
        mock_choice.return_value = '✨'  # Mock rationale: default emoji for unknown type
        msg = "changelog: update history"
        result = enhance_message(msg)
        self.assertEqual(result, "changelog: update history ✨")
        mock_choice.assert_called_once_with(["✨", "🔧", "🛠️"])


if __name__ == '__main__':
    unittest.main()
