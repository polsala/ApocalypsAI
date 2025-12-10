import os
import json
import unittest
from unittest.mock import patch, MagicMock
import ai_reviewer


class TestAIReviewer(unittest.TestCase):
    
    def setUp(self):
        # Mock environment variables
        os.environ['OPENROUTER_API_KEY'] = 'test-key'
        os.environ['GITHUB_TOKEN'] = 'test-token'
        os.environ['GITHUB_REPOSITORY'] = 'test/repo'
        os.environ['GITHUB_EVENT_PATH'] = '/tmp/test_event.json'
        
        # Create mock event file
        mock_event = {
            'pull_request': {
                'number': 123,
                'base': {'ref': 'main'},
                'head': {'ref': 'feature-branch'}
            }
        }
        with open('/tmp/test_event.json', 'w') as f:
            json.dump(mock_event, f)
    
    def tearDown(self):
        # Clean up
        if os.path.exists('/tmp/test_event.json'):
            os.remove('/tmp/test_event.json')
    
    @patch('subprocess.check_output')
    def test_get_pr_diff(self, mock_git_diff):
        """Test getting PR diff"""
        mock_git_diff.return_value = "diff --git a/test.py b/test.py"
        
        reviewer = ai_reviewer.AIReviewer()
        diff = reviewer.get_pr_diff()
        
        self.assertEqual(diff, "diff --git a/test.py b/test.py")
        mock_git_diff.assert_called_once()
    
    @patch('requests.post')
    def test_analyze_code(self, mock_post):
        """Test code analysis"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'Great code!'}}]
        }
        mock_post.return_value = mock_response
        
        reviewer = ai_reviewer.AIReviewer()
        result = reviewer.analyze_code("diff --git a/test.py b/test.py")
        
        self.assertEqual(result, 'Great code!')
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_analyze_code_error(self, mock_post):
        """Test code analysis with API error"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        reviewer = ai_reviewer.AIReviewer()
        result = reviewer.analyze_code("diff --git a/test.py b/test.py")
        
        self.assertIn("Error: API request failed", result)
    
    @patch('requests.post')
    def test_post_review_comment(self, mock_post):
        """Test posting review comment"""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response
        
        reviewer = ai_reviewer.AIReviewer()
        reviewer.post_review_comment("Great code!")
        
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertIn('Great code!', kwargs['json']['body'])
    
    @patch('ai_reviewer.AIReviewer.get_pr_diff')
    @patch('ai_reviewer.AIReviewer.analyze_code')
    @patch('ai_reviewer.AIReviewer.post_review_comment')
    def test_run(self, mock_post, mock_analyze, mock_get_diff):
        """Test main run method"""
        mock_get_diff.return_value = "diff --git a/test.py b/test.py"
        mock_analyze.return_value = "Great code!"
        
        reviewer = ai_reviewer.AIReviewer()
        result = reviewer.run()
        
        self.assertEqual(result, "Great code!")
        mock_get_diff.assert_called_once()
        mock_analyze.assert_called_once_with("diff --git a/test.py b/test.py")
        mock_post.assert_called_once_with("Great code!")


if __name__ == '__main__':
    unittest.main()
