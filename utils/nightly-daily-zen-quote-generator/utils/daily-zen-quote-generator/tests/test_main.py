import unittest
from unittest.mock import mock_open, patch
import pathlib
import json
import sys

# Add the src directory to sys.path for import
src_path = pathlib.Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(src_path))

import main as zg  # type: ignore


class TestDailyZenQuoteGenerator(unittest.TestCase):
    def setUp(self):
        self.sample_quotes = ["Test quote one.", "Test quote two."]
        self.mock_json = json.dumps(self.sample_quotes)

    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    def test_load_quotes_invalid(self, m_open):
        # Mock a JSON that is not a list
        m_open.return_value.read.return_value = json.dumps({"not": "a list"})
        with self.assertRaises(ValueError):
            zg.load_quotes(pathlib.Path('dummy'))

    @patch('builtins.open')
    @patch('random.choice')
    def test_get_random_quote(self, m_choice, m_open):
        # Mock file reading to return our sample quotes
        m_open.return_value.__enter__.return_value.read.return_value = self.mock_json
        # Mock random.choice to always pick the first quote
        m_choice.side_effect = lambda seq: seq[0]
        result = zg.get_random_quote(pathlib.Path('dummy'))
        self.assertEqual(result, self.sample_quotes[0])

    @patch.object(zg, 'load_quotes')
    @patch('random.choice')
    def test_main_output(self, m_choice, m_load):
        # Mock load_quotes to return a known list
        m_load.return_value = self.sample_quotes
        # Mock random.choice to pick the second quote
        m_choice.side_effect = lambda seq: seq[1]
        with patch('sys.stdout') as mock_stdout:
            zg.main()
            mock_stdout.write.assert_any_call(self.sample_quotes[1] + '\n')


if __name__ == '__main__':
    unittest.main()
