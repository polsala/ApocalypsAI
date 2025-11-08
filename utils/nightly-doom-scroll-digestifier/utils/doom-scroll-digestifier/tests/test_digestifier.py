import unittest
from unittest.mock import patch, MagicMock
import sys
import io
# Import the Digestifier class using its full path from the repository root
from utils.doom_scroll_digestifier.src.digestifier import Digestifier
import requests.exceptions

class TestDigestifier(unittest.TestCase):

    def setUp(self):
        self.digestifier = Digestifier()
        self.mock_html_success = """
        <html>
        <head><title>Test Article</title></head>
        <body>
            <header>Header content</header>
            <main>
                <h1>Article Title</h1>
                <p>This is the first sentence of the article. This is the second sentence. This is the third sentence.</p>
                <p>A global crisis is looming. We face a significant threat to our way of life. However, there is hope for a solution if we act now.</p>
                <ul><li>Item 1</li><li>Item 2</li></ul>
            </main>
            <footer>Footer content</footer>
        </body>
        </html>
        """
        self.mock_html_no_article = """
        <html>
        <body>
            <div>
                <p>Just some random text here. No specific article structure.</p>
                <p>Another paragraph with some details.</p>
            </div>
        </body>
        </html>
        """
        self.mock_html_empty = "<html><body></body></html>"

    @patch('requests.get')
    def test_fetch_article_content_success(self, mock_get):
        # Mock rationale: Simulate a successful HTTP request to a URL.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.mock_html_success
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        url = "http://example.com/test-article"
        content = self.digestifier.fetch_article_content(url)
        self.assertEqual(content, self.mock_html_success)
        mock_get.assert_called_once_with(url, headers={'User-Agent': 'ApocalypsAI-DoomScrollDigestifier/1.0'}, timeout=10)

    @patch('requests.get')
    def test_fetch_article_content_failure(self, mock_get):
        # Mock rationale: Simulate an HTTP request failure (e.g., 404, network error).
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        url = "http://example.com/bad-url"
        content = self.digestifier.fetch_article_content(url)
        self.assertEqual(content, "")
        mock_get.assert_called_once()

    def test_extract_main_text_with_article(self):
        text = self.digestifier.extract_main_text(self.mock_html_success)
        expected_text_start = "Article Title\n\nThis is the first sentence of the article. This is the second sentence. This is the third sentence.\n\nA global crisis is looming. We face a significant threat to our way of life. However, there is hope for a solution if we act now.\n\nItem 1\n\nItem 2"
        self.assertTrue(text.startswith("Article Title"))
        self.assertIn("A global crisis is looming.", text)
        self.assertIn("Item 1", text)
        self.assertIn("Item 2", text)
        self.assertNotIn("Header content", text)
        self.assertNotIn("Footer content", text)
        self.assertEqual(text, expected_text_start)

    def test_extract_main_text_no_article_tag(self):
        text = self.digestifier.extract_main_text(self.mock_html_no_article)
        self.assertIn("Just some random text here.", text)
        self.assertIn("Another paragraph with some details.", text)

    def test_extract_main_text_empty_html(self):
        text = self.digestifier.extract_main_text(self.mock_html_empty)
        self.assertEqual(text, "")

    def test_summarize_text_default_sentences(self):
        long_text = "Sentence one. Sentence two. Sentence three. Sentence four. Sentence five."
        summary = self.digestifier.summarize_text(long_text)
        self.assertEqual(summary, "Sentence one. Sentence two. Sentence three.")

    def test_summarize_text_custom_sentences(self):
        long_text = "Sentence one. Sentence two. Sentence three. Sentence four. Sentence five."
        summary = self.digestifier.summarize_text(long_text, num_sentences=2)
        self.assertEqual(summary, "Sentence one. Sentence two.")

    def test_summarize_text_fewer_than_requested(self):
        short_text = "Sentence one. Sentence two."
        summary = self.digestifier.summarize_text(short_text, num_sentences=5)
        self.assertEqual(summary, "Sentence one. Sentence two.")

    def test_summarize_text_empty(self):
        summary = self.digestifier.summarize_text("")
        self.assertEqual(summary, "")

    def test_analyze_sentiment_doom_laden(self):
        text = "A global crisis is looming, threatening our future. This disaster requires immediate action."
        sentiment, keywords = self.digestifier.analyze_sentiment(text)
        self.assertEqual(sentiment, "Doom-laden")
        self.assertIn('crisis', keywords)
        self.assertIn('threat', keywords) # 'threat' is found within 'threatening'
        self.assertIn('disaster', keywords)

    def test_analyze_sentiment_hopeful(self):
        text = "There is hope for a solution, and significant progress has been made. Innovation will lead to recovery."
        sentiment, keywords = self.digestifier.analyze_sentiment(text)
        self.assertEqual(sentiment, "Hopeful")
        self.assertIn('hope', keywords)
        self.assertIn('solution', keywords)
        self.assertIn('progress', keywords)
        self.assertIn('innovation', keywords)
        self.assertIn('recovery', keywords)

    def test_analyze_sentiment_neutral(self):
        text = "The cat sat on the mat. The dog barked loudly."
        sentiment, keywords = self.digestifier.analyze_sentiment(text)
        self.assertEqual(sentiment, "Neutral")
        self.assertEqual(keywords, [])

    def test_analyze_sentiment_mixed_equal(self):
        text = "A crisis is here, but there is hope for a solution."
        sentiment, keywords = self.digestifier.analyze_sentiment(text)
        self.assertEqual(sentiment, "Neutral") # Equal count of doom and silver lining keywords
        self.assertEqual(keywords, [])

    def test_analyze_sentiment_empty(self):
        sentiment, keywords = self.digestifier.analyze_sentiment("")
        self.assertEqual(sentiment, "Neutral")
        self.assertEqual(keywords, [])

    @patch('argparse.ArgumentParser.parse_args')
    @patch('utils.doom_scroll_digestifier.src.digestifier.Digestifier.fetch_article_content')
    @patch('utils.doom_scroll_digestifier.src.digestifier.Digestifier.extract_main_text')
    @patch('utils.doom_scroll_digestifier.src.digestifier.Digestifier.summarize_text')
    @patch('utils.doom_scroll_digestifier.src.digestifier.Digestifier.analyze_sentiment')
    def test_main_function_success(self, mock_analyze, mock_summarize, mock_extract, mock_fetch, mock_parse_args):
        # Mock rationale: Simulate the full execution flow of the main function without actual network calls or file I/O.
        mock_parse_args.return_value = MagicMock(url="http://example.com/test", sentences=2)
        mock_fetch.return_value = self.mock_html_success
        mock_extract.return_value = "Article Title. Sentence one. Sentence two. Crisis looming. Hope for solution."
        mock_summarize.return_value = "Article Title. Sentence one."
        mock_analyze.return_value = ("Doom-laden", ['crisis'])

        captured_output = io.StringIO()
        sys.stdout = captured_output

        from utils.doom_scroll_digestifier.src.digestifier import main
        main()

        sys.stdout = sys.__stdout__ # Reset stdout

        output = captured_output.getvalue()
        self.assertIn("Article URL: http://example.com/test", output)
        self.assertIn("--- Summary ---", output)
        self.assertIn("Article Title. Sentence one.", output)
        self.assertIn("--- Sentiment Analysis ---", output)
        self.assertIn("Overall Mood: Doom-laden (Keywords: crisis)", output)
        self.assertIn("--- Full Article Snippet ---", output)
        self.assertIn("Crisis looming. Hope for solution.", output)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('utils.doom_scroll_digestifier.src.digestifier.Digestifier.fetch_article_content')
    def test_main_function_fetch_failure(self, mock_fetch, mock_parse_args):
        # Mock rationale: Simulate a failure during article content fetching.
        mock_parse_args.return_value = MagicMock(url="http://example.com/bad", sentences=2)
        mock_fetch.return_value = ""

        captured_output = io.StringIO()
        sys.stdout = captured_output

        from utils.doom_scroll_digestifier.src.digestifier import main
        main()

        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("Could not fetch article content.", output)
        self.assertNotIn("--- Summary ---", output)
