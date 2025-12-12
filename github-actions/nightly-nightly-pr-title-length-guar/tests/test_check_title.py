import json
import os
import sys
import tempfile
import unittest
from unittest import mock

# Import the module under test
# The path is relative; adjust sys.path accordingly
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "..", "src"))
sys.path.insert(0, src_dir)
import check_title

class TestCheckTitle(unittest.TestCase):
    def setUp(self):
        # Create a temporary file to act as GITHUB_EVENT_PATH
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8")
        self.addCleanup(os.unlink, self.temp_file.name)

    def write_event(self, payload: dict):
        self.temp_file.seek(0)
        self.temp_file.truncate()
        json.dump(payload, self.temp_file)
        self.temp_file.flush()

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_missing_github_event_path(self):
        # Ensure the script exits with error when env var is missing
        with self.assertRaises(SystemExit) as cm:
            check_title.main("72")
        self.assertEqual(cm.exception.code, 1)

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_no_pull_request_in_payload(self):
        os.environ["GITHUB_EVENT_PATH"] = self.temp_file.name
        self.write_event({"some": "data"})
        with self.assertRaises(SystemExit) as cm:
            check_title.main("72")
        self.assertEqual(cm.exception.code, 1)

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_title_within_limit(self):
        os.environ["GITHUB_EVENT_PATH"] = self.temp_file.name
        payload = {"pull_request": {"title": "Add new feature"}}
        self.write_event(payload)
        # Capture stdout to verify success message
        with mock.patch('sys.stdout') as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                check_title.main("72")
            self.assertEqual(cm.exception.code, 0)
            # Ensure a success message was printed
            printed = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
            self.assertIn("PR title length check passed", printed)

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_title_exceeds_limit(self):
        os.environ["GITHUB_EVENT_PATH"] = self.temp_file.name
        long_title = "A" * 80
        payload = {"pull_request": {"title": long_title}}
        self.write_event(payload)
        with mock.patch('sys.stdout') as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                check_title.main("72")
            self.assertEqual(cm.exception.code, 1)
            printed = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
            self.assertIn("PR title is too long", printed)

if __name__ == "__main__":
    unittest.main()
