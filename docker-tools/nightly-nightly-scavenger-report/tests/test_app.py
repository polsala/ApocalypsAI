import unittest
from unittest.mock import mock_open, patch
import sys
import os

# Import the app module from src
from src import app

class TestScavengerReport(unittest.TestCase):
    def test_emoji_for_known(self):
        self.assertEqual(app.emoji_for("canned beans"), "🥫")
        self.assertEqual(app.emoji_for("BOTTLED WATER"), "💧")
    def test_emoji_for_unknown(self):
        self.assertEqual(app.emoji_for("mysterious artifact"), "📦")
    def test_generate_report(self):
        items = [
            {"name": "canned beans", "quantity": 2},
            {"name": "flashlight", "quantity": 1},
        ]
        expected = (
            "🗃️ Scavenger Report\n"
            "--------------------\n"
            "🥫 canned beans x2\n"
            "🔦 flashlight x1"
        )
        self.assertEqual(app.generate_report(items), expected)
    @patch("builtins.open", new_callable=mock_open, read_data='[{"name":"knife","quantity":3}]')
    def test_load_items(self, mock_file):
        result = app.load_items("dummy")
        self.assertEqual(result, [{"name":"knife","quantity":3}])
    @patch("src.app.load_items")
    @patch("builtins.print")
    def test_main_success(self, mock_print, mock_load):
        mock_load.return_value = [{"name":"radio","quantity":1}]
        with patch.dict(os.environ, {"ITEMS_PATH": "dummy"}):
            app.main()
        mock_print.assert_called_once_with(
            "🗃️ Scavenger Report\n--------------------\n📻 radio x1"
        )
    @patch("src.app.load_items", side_effect=Exception("boom"))
    @patch("builtins.print")
    def test_main_failure(self, mock_print, mock_load):
        with self.assertRaises(SystemExit) as cm:
            app.main()
        self.assertEqual(cm.exception.code, 1)
        mock_print.assert_called_once()
        args = mock_print.call_args[0][0]
        self.assertIn("Error loading items", args)

if __name__ == "__main__":
    unittest.main()
