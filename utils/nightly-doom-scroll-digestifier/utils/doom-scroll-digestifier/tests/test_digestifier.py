import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import requests.exceptions

# Add the src directory to the path to allow importing digestifier
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from digestifier import fetch_url_content, strip_html, analyze_doom_level, summarize_text, main, DOOM_KEYWORDS, DOOM_LEVEL_MAP

class TestDigestifier(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_url_content_success(self, mock_get):
        # Mock rationale: Avoid actual network requests for deterministic, offline tests.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Hello World</body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        url = "http://example.com"
        content = fetch_url_content(url)
        self.assertEqual(content, "<html><body>Hello World</body></html>")
        mock_get.assert_called_once_with(url, timeout=10)

    @patch('requests.get')
    def test_fetch_url_content_failure(self, mock_get):
        # Mock rationale: Simulate network errors or bad HTTP responses.
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        url = "http://bad-example.com"
        with patch('sys.stderr', new=MagicMock()) as mock_stderr:
            content = fetch_url_content(url)
            self.assertEqual(content, "")
            # Check if an error message was printed to stderr
            self.assertIn("Error fetching URL", mock_stderr.getvalue())

    def test_strip_html_basic(self):
        html = "<html><body><h1>Title</h1><p>Some text.</p></body></html>"
        expected = "Title Some text."
        self.assertEqual(strip_html(html), expected)

    def test_strip_html_with_scripts_styles(self):
        html = """
        <html>
        <head><style>body { color: red; }</style></head>
        <body>
            <script>alert('hello');</script>
            <p>Important info.</p>
            <!-- comment -->
        </body>
        </html>
        """
        expected = "Important info."
        self.assertEqual(strip_html(html), expected)

    def test_strip_html_empty(self):
        self.assertEqual(strip_html(""), "")
        self.assertEqual(strip_html("<!-- comment -->"), "")

    def test_analyze_doom_level_no_doom(self):
        text = "This is a very positive article about puppies and rainbows."
        self.assertEqual(analyze_doom_level(text), 0)

    def test_analyze_doom_level_some_doom(self):
        text = "There is a minor risk of a small crisis, but experts are optimistic."
        # 'risk', 'crisis' are in DOOM_KEYWORDS. 2 unique keywords.
        self.assertEqual(analyze_doom_level(text), 2)

    def test_analyze_doom_level_high_doom(self):
        text = "The world faces an unprecedented catastrophe, a dire warning of global collapse and widespread suffering. This is an apocalyptic threat."
        # 'unprecedented', 'catastrophe', 'dire', 'warning', 'collapse', 'suffering', 'apocalyptic', 'threat'
        # 8 unique keywords.
        self.assertEqual(analyze_doom_level(text), 8)

    def test_analyze_doom_level_max_doom(self):
        text = "A global crisis and an unprecedented disaster leading to a catastrophic collapse. This is a dire warning of an apocalyptic threat and widespread suffering, an emergency of grave peril."
        # 'crisis', 'unprecedented', 'disaster', 'catastrophic', 'collapse', 'dire', 'warning', 'apocalyptic', 'threat', 'suffering', 'emergency', 'grave', 'peril'
        # 13 unique keywords, capped at 10.
        self.assertEqual(analyze_doom_level(text), 10)

    def test_analyze_doom_level_empty_text(self):
        self.assertEqual(analyze_doom_level(""), 0)

    def test_summarize_text_basic(self):
        text = "This is the first sentence. This is the second sentence. This is the third sentence. This is the fourth sentence."
        expected = "This is the first sentence. This is the second sentence. This is the third sentence."
        self.assertEqual(summarize_text(text, max_sentences=3), expected)

    def test_summarize_text_fewer_sentences_than_max(self):
        text = "Only one sentence here. Another one."
        expected = "Only one sentence here. Another one."
        self.assertEqual(summarize_text(text, max_sentences=3), expected)

    def test_summarize_text_empty(self):
        self.assertEqual(summarize_text(""), "")

    @patch('requests.get')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_success(self, mock_parse_args, mock_stderr, mock_stdout, mock_get):
        # Mock rationale: Simulate CLI arguments and network requests, capture output.
        mock_parse_args.return_value = MagicMock(url="http://example.com/news")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><p>This is a crisis. A very big crisis. But we will overcome.</p></body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        main()

        mock_get.assert_called_once_with("http://example.com/news", timeout=10)
        output = mock_stdout.getvalue()
        self.assertIn("URL: http://example.com/news", output)
        # 'crisis' is 1 unique keyword. So doom level should be 1.
        self.assertIn("Doom Level: 1/10 (Calm)", output)
        self.assertIn("Summary: This is a crisis. A very big crisis. But we will overcome.", output)
        mock_stderr.assert_not_called()

    @patch('requests.get')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_fetch_failure(self, mock_parse_args, mock_stderr, mock_stdout, mock_get):
        # Mock rationale: Simulate network failure during main execution.
        mock_parse_args.return_value = MagicMock(url="http://bad-example.com")
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Error fetching URL", mock_stderr.getvalue())

    @patch('requests.get')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('sys.stderr', new_callable=MagicMock)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_no_plain_text(self, mock_parse_args, mock_stderr, mock_stdout, mock_get):
        # Mock rationale: Simulate a URL that returns unparseable content (e.g., only scripts).
        mock_parse_args.return_value = MagicMock(url="http://empty-content.com")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><script>console.log('no text');</script></body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Could not extract plain text", mock_stderr.getvalue())
