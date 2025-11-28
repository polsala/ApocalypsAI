import unittest
from unittest import mock

# Mock rationale: we replace sys.argv to test CLI behaviour without spawning a subprocess.
from utils.nightly-emoji-status-broadcaster.src.broadcaster import (
    status_to_emoji,
    summarize_statuses,
    main,
)

class TestEmojiStatusBroadcaster(unittest.TestCase):
    def test_status_to_emoji_known(self):
        self.assertEqual(status_to_emoji("success"), "✅")
        self.assertEqual(status_to_emoji("FAILURE"), "❌")
        self.assertEqual(status_to_emoji("in-progress"), "⏳")
        self.assertEqual(status_to_emoji("pending"), "🕒")

    def test_status_to_emoji_unknown(self):
        self.assertEqual(status_to_emoji("foobar"), "❓")

    def test_summarize_mixed(self):
        input_statuses = ["success", "failure", "in_progress", "unknown"]
        expected = "✅ Success, ❌ Failure, ⏳ In Progress, ❓ Unknown"
        self.assertEqual(summarize_statuses(input_statuses), expected)

    @mock.patch("builtins.print")
    def test_cli_multiple_lines(self, mock_print):
        # Simulate calling the script without --summary
        argv = ["success", "failure", "in_progress"]
        main(argv)
        mock_print.assert_has_calls([
            mock.call("✅"),
            mock.call("❌"),
            mock.call("⏳"),
        ], any_order=False)

    @mock.patch("builtins.print")
    def test_cli_summary_flag(self, mock_print):
        argv = ["success", "failure", "in_progress", "--summary"]
        # argparse parses flags after positional args, so we need to place flag before statuses
        # Mock rationale: we rearrange to match expected parsing order.
        argv = ["--summary", "success", "failure", "in_progress"]
        main(argv)
        mock_print.assert_called_once_with("✅ Success, ❌ Failure, ⏳ In Progress")

if __name__ == "__main__":
    unittest.main()
