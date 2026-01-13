import unittest
import json
import os
import sys
from unittest import mock
from io import StringIO

# Ensure src is on path for import
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
import main

class TestIssueEmojiBooster(unittest.TestCase):
    @mock.patch("main.requests.post")
    def test_adds_reaction_success(self, mock_post):
        mock_resp = mock.Mock()
        mock_resp.status_code = 201
        mock_post.return_value = mock_resp

        event = {"issue": {"number": 42}}
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(event))):
            with mock.patch.dict(os.environ, {
                "GITHUB_TOKEN": "fake-token",
                "GITHUB_REPOSITORY": "owner/repo",
                "GITHUB_EVENT_PATH": "/path/to/event.json"
            }):
                with mock.patch("sys.stdout", new=StringIO()) as fake_out:
                    main.main()
                    output = fake_out.getvalue()
                    self.assertIn("Added reaction", output)
        expected_url = "https://api.github.com/repos/owner/repo/issues/42/reactions"
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], expected_url)
        self.assertIn("content", kwargs["json"])

    @mock.patch("main.requests.post")
    def test_missing_env_vars(self, mock_post):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit) as cm:
                main.main()
            self.assertEqual(cm.exception.code, 1)

if __name__ == "__main__":
    unittest.main()
