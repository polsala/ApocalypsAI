"""Tests for the ``emoji-lookup`` utility.

All tests are deterministic and run offline – no network calls are performed.
"""

import builtins
import sys
import unittest
from unittest import mock

# Import the module under test. The relative import works because the test runner adds the
# ``utils/emoji-lookup/src`` directory to ``sys.path`` via ``PYTHONPATH`` in the CI workflow.
from utils.emoji_lookup.src.lookup import get_emoji, main


class TestGetEmoji(unittest.TestCase):
    def test_known_emoji(self):
        self.assertEqual(get_emoji("thumbs_up"), "👍")
        self.assertEqual(get_emoji("rocket"), "🚀")
        self.assertEqual(get_emoji("coffee"), "☕")

    def test_unknown_emoji_raises(self):
        with self.assertRaises(KeyError) as ctx:
            get_emoji("nonexistent")
        # Mock rationale: ensure the error message contains the missing name.
        self.assertIn("nonexistent", str(ctx.exception))


class TestCLI(unittest.TestCase):
    @mock.patch.object(sys, "argv", ["lookup.py", "smile"])
    @mock.patch("builtins.print")
    def test_cli_success(self, mock_print):
        # Mock rationale: capture stdout without actually printing.
        exit_code = main()
        self.assertEqual(exit_code, 0)
        mock_print.assert_called_once_with("😄")

    @mock.patch.object(sys, "argv", ["lookup.py", "unknown"])
    @mock.patch("builtins.print")
    def test_cli_failure(self, mock_print):
        # Mock rationale: ensure error path returns non‑zero and prints to stderr.
        with mock.patch("sys.stderr", new_callable=mock.Mock()) as mock_stderr:
            exit_code = main()
            self.assertEqual(exit_code, 1)
            mock_stderr.write.assert_called()  # error message written to stderr
            mock_print.assert_not_called()


if __name__ == "__main__":
    unittest.main()
