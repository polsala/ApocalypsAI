import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
import requests.exceptions

# Add the src directory to the path to allow importing scavenger
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))))
import scavenger

class TestScavenger(unittest.TestCase):

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('requests.head')
    def test_all_links_working(self, mock_head, mock_exit, mock_stdout):
        # Mock rationale: Prevent actual network calls and control HTTP responses.
        mock_head.side_effect = [
            MagicMock(status_code=200),
            MagicMock(status_code=200)
        ]
        # Mock rationale: Simulate reading from a file without needing a real file.
        with patch('builtins.open', mock_open(read_data='https://example.com/good1\nhttps://example.com/good2')):
            scavenger.check_links('dummy_links.txt')

            self.assertEqual(mock_head.call_count, 2)
            mock_exit.assert_called_once_with(0) # Expect success
            output = mock_stdout.getvalue()
            self.assertIn('[✅ 200] https://example.com/good1', output)
            self.assertIn('[✅ 200] https://example.com/good2', output)
            self.assertIn('Working URLs: 2', output)
            self.assertIn('Broken URLs: 0', output)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('requests.head')
    def test_some_links_broken(self, mock_head, mock_exit, mock_stdout):
        # Mock rationale: Prevent actual network calls and control HTTP responses.
        mock_head.side_effect = [
            MagicMock(status_code=200),
            MagicMock(status_code=404),
            MagicMock(status_code=500)
        ]
        # Mock rationale: Simulate reading from a file without needing a real file.
        with patch('builtins.open', mock_open(read_data='https://example.com/good\nhttps://example.com/bad1\nhttps://example.com/bad2')):
            scavenger.check_links('dummy_links.txt')

            self.assertEqual(mock_head.call_count, 3)
            mock_exit.assert_called_once_with(1) # Expect failure due to broken links
            output = mock_stdout.getvalue()
            self.assertIn('[✅ 200] https://example.com/good', output)
            self.assertIn('[❌ 404] https://example.com/bad1', output)
            self.assertIn('[❌ 500] https://example.com/bad2', output)
            self.assertIn('Working URLs: 1', output)
            self.assertIn('Broken URLs: 2', output)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('requests.head')
    def test_connection_error(self, mock_head, mock_exit, mock_stdout):
        # Mock rationale: Simulate a network connection error.
        mock_head.side_effect = [
            MagicMock(status_code=200),
            requests.exceptions.ConnectionError('DNS lookup failed')
        ]
        # Mock rationale: Simulate reading from a file without needing a real file.
        with patch('builtins.open', mock_open(read_data='https://example.com/good\nhttps://nonexistent.domain/page')):
            scavenger.check_links('dummy_links.txt')

            self.assertEqual(mock_head.call_count, 2)
            mock_exit.assert_called_once_with(1) # Expect failure due to connection error
            output = mock_stdout.getvalue()
            self.assertIn('[✅ 200] https://example.com/good', output)
            self.assertIn('[❌ ERR] https://nonexistent.domain/page (ConnectionError: DNS lookup failed)', output)
            self.assertIn('Working URLs: 1', output)
            self.assertIn('Broken URLs: 1', output)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('requests.head')
    def test_timeout_error(self, mock_head, mock_exit, mock_stdout):
        # Mock rationale: Simulate a request timeout error.
        mock_head.side_effect = [
            requests.exceptions.Timeout('Request timed out')
        ]
        # Mock rationale: Simulate reading from a file without needing a real file.
        with patch('builtins.open', mock_open(read_data='https://slow.server/page')):
            scavenger.check_links('dummy_links.txt')

            self.assertEqual(mock_head.call_count, 1)
            mock_exit.assert_called_once_with(1) # Expect failure due to timeout
            output = mock_stdout.getvalue()
            self.assertIn('[❌ ERR] https://slow.server/page (Timeout: Request timed out)', output)
            self.assertIn('Working URLs: 0', output)
            self.assertIn('Broken URLs: 1', output)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('os.path.exists', return_value=False)
    def test_file_not_found(self, mock_exists, mock_exit, mock_stdout):
        # Mock rationale: Simulate the scenario where the input file does not exist.
        scavenger.check_links('nonexistent_file.txt')

        mock_exit.assert_called_once_with(1)
        output = mock_stdout.getvalue()
        self.assertIn("Error: Link file 'nonexistent_file.txt' not found.", output)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    def test_empty_file(self, mock_exit, mock_stdout):
        # Mock rationale: Simulate reading from an empty file.
        with patch('builtins.open', mock_open(read_data='')):
            scavenger.check_links('empty_links.txt')

            mock_exit.assert_called_once_with(0) # No URLs, so no broken links, exit 0
            output = mock_stdout.getvalue()
            self.assertIn("No URLs found in 'empty_links.txt'. Nothing to scan.", output)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('requests.head')
    def test_redirect_handled(self, mock_head, mock_exit, mock_stdout):
        # Mock rationale: Simulate a redirect (301) that resolves to a 200.
        # requests.head with allow_redirects=True handles this automatically by returning the final status.
        mock_head.side_effect = [
            MagicMock(status_code=200) # The final status after redirect
        ]
        # Mock rationale: Simulate reading from a file without needing a real file.
        with patch('builtins.open', mock_open(read_data='https://example.com/redirect')):
            scavenger.check_links('dummy_links.txt')

            self.assertEqual(mock_head.call_count, 1)
            mock_exit.assert_called_once_with(0)
            output = mock_stdout.getvalue()
            self.assertIn('[✅ 200] https://example.com/redirect', output)
            self.assertIn('Working URLs: 1', output)
            self.assertIn('Broken URLs: 0', output)

    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.exit')
    @patch('requests.head')
    def test_mixed_valid_and_empty_lines(self, mock_head, mock_exit, mock_stdout):
        # Mock rationale: Test handling of empty lines in the input file.
        mock_head.side_effect = [
            MagicMock(status_code=200)
        ]
        with patch('builtins.open', mock_open(read_data='\nhttps://example.com/valid\n\n')):
            scavenger.check_links('dummy_links.txt')

            self.assertEqual(mock_head.call_count, 1)
            mock_exit.assert_called_once_with(0)
            output = mock_stdout.getvalue()
            self.assertIn('[✅ 200] https://example.com/valid', output)
            self.assertIn('Total URLs: 1', output)
            self.assertIn('Working URLs: 1', output)
            self.assertIn('Broken URLs: 0', output)


if __name__ == '__main__':
    unittest.main()
