import unittest\nfrom unittest.mock import patch\nimport datetime\n\n# Mock rationale: Ensure deterministic behavior without relying on the actual current date.\nfrom utils.daily_zen_quote_generator.src.main import get_zen_quote, main\n\n\nclass TestZenQuote(unittest.TestCase):\n    def test_known_date(self):\n        # 2023-01-01 should map to a predictable quote based on the algorithm.\n        date = datetime.date(2023, 1, 1)\n        expected = get_zen_quote(date)\n        # Manually compute expected using the same logic for verification.\n        index = int(date.strftime("%Y%m%d")) % 8  # there are 8 quotes\n        quotes = [\
            "The journey of a thousand miles begins with one step.",\
            "Simplicity is the ultimate sophistication.",\
            "When the mind is still, the universe surrenders.",\
            "The obstacle is the path.",\
            "Let go or be dragged.",\
            "Silence is a source of great strength.",\
            "Be present, not perfect.",\
            "All is water.",\
        ]\n        self.assertEqual(expected, quotes[index])\n\n    @patch('utils.daily_zen_quote_generator.src.main.datetime.date')\n    def test_cli_today(self, mock_date):\n        # Mock rationale: Simulate today as 2022-12-31 to make the CLI deterministic.\n        mock_date.today.return_value = datetime.date(2022, 12, 31)\n        # Run CLI with no arguments (should use mocked today).\n        with patch('sys.argv', ['prog']):\n            exit_code = main()\n        self.assertEqual(exit_code, 0)\n\n\nif __name__ == '__main__':\n    unittest.main()
