import builtins
import io
import json
import pathlib
import unittest
from unittest import mock

# Import the module under test
from src.tracker import mood_to_emoji, load_mood_file, print_mood_report

class TestMoodToEmoji(unittest.TestCase):
    def test_valid_mappings(self):
        expected = {
            0: "😞",
            1: "🙁",
            2: "😐",
            3: "🙂",
            4: "😄",
        }
        for score, emoji in expected.items():
            self.assertEqual(mood_to_emoji(score), emoji)

    def test_invalid_score_raises(self):
        for invalid in [-1, 5, 10]:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    mood_to_emoji(invalid)

class TestLoadMoodFile(unittest.TestCase):
    # Mock rationale: we avoid filesystem I/O by mocking Path.read_text()
    @mock.patch.object(pathlib.Path, "read_text")
    def test_load_valid_json(self, mock_read):
        mock_content = json.dumps({"2025-11-20": 4, "2025-11-21": 2})
        mock_read.return_value = mock_content
        result = load_mood_file(pathlib.Path("dummy.json"))
        self.assertEqual(result, {"2025-11-20": 4, "2025-11-21": 2})

    @mock.patch.object(pathlib.Path, "read_text")
    def test_invalid_json_raises(self, mock_read):
        mock_read.return_value = "{ not: valid json }"
        with self.assertRaises(ValueError):
            load_mood_file(pathlib.Path("bad.json"))

    @mock.patch.object(pathlib.Path, "read_text")
    def test_non_dict_json_raises(self, mock_read):
        mock_read.return_value = json.dumps([1, 2, 3])
        with self.assertRaises(ValueError):
            load_mood_file(pathlib.Path("list.json"))

    @mock.patch.object(pathlib.Path, "read_text")
    def test_invalid_score_type_raises(self, mock_read):
        mock_read.return_value = json.dumps({"2025-11-20": "high"})
        with self.assertRaises(ValueError):
            load_mood_file(pathlib.Path("type.json"))

    @mock.patch.object(pathlib.Path, "read_text")
    def test_score_out_of_range_raises(self, mock_read):
        mock_read.return_value = json.dumps({"2025-11-20": 7})
        with self.assertRaises(ValueError):
            load_mood_file(pathlib.Path("range.json"))

class TestPrintMoodReport(unittest.TestCase):
    def test_output_order_and_format(self):
        data = {"2025-11-22": 0, "2025-11-20": 4, "2025-11-21": 2}
        expected_output = "2025-11-20 😄\n2025-11-21 😐\n2025-11-22 😞\n"
        with mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
            print_mood_report(data)
            self.assertEqual(fake_out.getvalue(), expected_output)

if __name__ == "__main__":
    unittest.main()
