import os
import sys
import json
import builtins
import unittest
from unittest import mock

# Import the module under test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import compliment

class TestCompliment(unittest.TestCase):
    def test_select_compliment_returns_valid(self):
        # Ensure the selected compliment is from the predefined list
        result = compliment.select_compliment()
        self.assertIn(result, compliment.COMPLIMENTS)

    @mock.patch('urllib.request.urlopen')
    def test_post_comment_makes_correct_request(self, mock_urlopen):
        # Mock the HTTP response
        mock_response = mock.Mock()
        mock_response.__enter__.return_value = mock_response
        mock_response.read.return_value = json.dumps({"id": 123}).encode('utf-8')
        mock_response.__iter__.return_value = iter([])
        mock_urlopen.return_value = mock_response

        repo = "owner/repo"
        pr_number = 42
        token = "ghp_fakeToken"
        body = "Test comment"
        result = compliment.post_comment(repo, pr_number, token, body)
        # Verify that urlopen was called with correct URL and headers
        expected_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
        args, kwargs = mock_urlopen.call_args
        request_obj = args[0]
        self.assertEqual(request_obj.full_url, expected_url)
        self.assertEqual(request_obj.get_header('Authorization'), f"Bearer {token}")
        self.assertEqual(request_obj.get_header('Accept'), "application/vnd.github+json")
        # Verify payload
        sent_data = json.loads(request_obj.data.decode('utf-8'))
        self.assertEqual(sent_data['body'], body)
        # Verify returned data
        self.assertEqual(result, {"id": 123})

    def test_main_writes_output(self):
        # Prepare environment variables
        env = {
            'GITHUB_REPOSITORY': 'owner/repo',
            'GITHUB_PULL_REQUEST_NUMBER': '1',
            'GITHUB_TOKEN': 'ghp_fake',
            'GITHUB_OUTPUT': 'tmp_output.txt'
        }
        with mock.patch.dict(os.environ, env, clear=True):
            # Mock network call to avoid real HTTP request
            with mock.patch('compliment.post_comment') as mock_post:
                mock_post.return_value = {'id': 1}
                # Run main
                compliment.main()
                # Verify output file content
                with open('tmp_output.txt', 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                self.assertTrue(content.startswith('compliment='))
                # Clean up
                os.remove('tmp_output.txt')

if __name__ == '__main__':
    unittest.main()
