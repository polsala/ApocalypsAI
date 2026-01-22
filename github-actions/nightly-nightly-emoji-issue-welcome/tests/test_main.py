import unittest
import os
from unittest import mock
import sys

# Adjust path so we can import the action module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import src.main as action

class TestBuildComment(unittest.TestCase):
    def test_emoji_selection(self):
        self.assertEqual(action.build_comment(0), "🚀 Welcome to the apocalypse! Thanks for opening this issue.")
        self.assertEqual(action.build_comment(7), "💫 Welcome to the apocalypse! Thanks for opening this issue.")
        self.assertEqual(action.build_comment(8), "🚀 Welcome to the apocalypse! Thanks for opening this issue.")

class TestPostComment(unittest.TestCase):
    @mock.patch('src.main.requests.post')
    def test_post_comment(self, mock_post):
        mock_resp = mock.Mock()
        mock_resp.json.return_value = {"id": 1}
        mock_resp.raise_for_status.return_value = None
        mock_post.return_value = mock_resp

        result = action.post_comment('owner/repo', 42, 'test comment', 'token123')
        mock_post.assert_called_once_with(
            'https://api.github.com/repos/owner/repo/issues/42/comments',
            headers={'Authorization': 'token token123', 'Accept': 'application/vnd.github+json'},
            json={'body': 'test comment'}
        )
        self.assertEqual(result, {"id": 1})

class TestMainFlow(unittest.TestCase):
    @mock.patch('src.main.post_comment')
    @mock.patch('src.main.load_event')
    def test_main(self, mock_load_event, mock_post_comment):
        mock_load_event.return_value = {'issue': {'number': 5, 'html_url': 'https://github.com/owner/repo/issues/5'}}
        with mock.patch.dict(os.environ, {'GITHUB_TOKEN': 'tok', 'GITHUB_REPOSITORY': 'owner/repo'}):
            action.main()
        mock_post_comment.assert_called_once_with('owner/repo', 5, action.build_comment(5), 'tok')

if __name__ == '__main__':
    unittest.main()
