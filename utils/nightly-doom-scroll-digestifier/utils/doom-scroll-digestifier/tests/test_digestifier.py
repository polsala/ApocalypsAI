import unittest
from unittest.mock import patch, MagicMock
import random
from src.digestifier import DoomScrollDigestifier

class TestDoomScrollDigestifier(unittest.TestCase):

    def setUp(self):
        self.digestifier = DoomScrollDigestifier()
        # Ensure deterministic random choice for whimsical spins
        # Mock rationale: `random.choice` is non-deterministic. Mocking it ensures tests always use the same spin.
        self.mock_random_choice = patch('random.choice', return_value=self.digestifier.WHIMSICAL_SPINS[0])
        self.mock_random_choice.start()

    def tearDown(self):
        self.mock_random_choice.stop()

    @patch('requests.get')
    def test_digest_with_doom_content(self, mock_get):
        # Mock rationale: `requests.get` performs network I/O. Mocking it allows offline, deterministic testing.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            "<html><body><h1>Breaking News</h1>" +
            "<p>Experts warn of an unprecedented global crisis. " +
            "The economic collapse is accelerating faster than anticipated. " +
            "A new environmental threat looms over the horizon, causing widespread panic. " +
            "Governments are struggling to respond to the impending disaster. " +
            "Citizens face peril and uncertainty. " +
            "But some say there's hope. This is a normal sentence. " +
            "Another sentence without doom. The world is fine. " +
            "The ultimate apocalypse is still far away. " +
            "A final warning about the future of humanity.</p></body></html>"
        )
        mock_get.return_value = mock_response

        url = "http://example.com/doom-news"
        expected_output = (
            "--- Doom Scroll Digest --- \n\nDetected signals of impending doom:\n" +
            "- \"Experts warn of an unprecedented global crisis.\" \n" +
            "- \"The economic collapse is accelerating faster than anticipated.\" \n" +
            "- \"A new environmental threat looms over the horizon, causing widespread panic.\" \n" +
            "- \"Governments are struggling to respond to the impending disaster.\" \n" +
            "- \"Citizens face peril and uncertainty.\" \n" +
            f"\n{self.digestifier.WHIMSICAL_SPINS[0]}\n"
        )
        self.assertEqual(self.digestifier.digest(url), expected_output)

    @patch('requests.get')
    def test_digest_without_doom_content(self, mock_get):
        # Mock rationale: `requests.get` performs network I/O. Mocking it allows offline, deterministic testing.
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            "<html><body><h1>Good News!</h1>" +
            "<p>The economy is booming. New technologies are bringing prosperity. " +
            "Everyone is happy and well-fed. There are no problems whatsoever. " +
            "The future is bright and full of promise.</p></body></html>"
        )
        mock_get.return_value = mock_response

        url = "http://example.com/good-news"
        expected_output = (
            "--- Doom Scroll Digest --- \n\n" +
            "No significant signs of impending doom detected today! " +
            "Perhaps the apocalypse is taking a coffee break. Enjoy the peace while it lasts!"
        )
        self.assertEqual(self.digestifier.digest(url), expected_output)

    @patch('requests.get')
    def test_digest_http_error(self, mock_get):
        # Mock rationale: `requests.get` performs network I/O. Mocking it allows offline, deterministic testing.
        mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")

        url = "http://example.com/non-existent"
        expected_output_prefix = "Error fetching URL http://example.com/non-existent: 404 Not Found"
        self.assertTrue(self.digestifier.digest(url).startswith(expected_output_prefix))

    @patch('requests.get')
    def test_digest_connection_error(self, mock_get):
        # Mock rationale: `requests.get` performs network I/O. Mocking it allows offline, deterministic testing.
        mock_get.side_effect = requests.exceptions.ConnectionError("DNS lookup failed")

        url = "http://example.com/unreachable"
        expected_output_prefix = "Error fetching URL http://example.com/unreachable: DNS lookup failed"
        self.assertTrue(self.digestifier.digest(url).startswith(expected_output_prefix))

    def test_extract_text_from_html(self):
        html_content = "<html><head><title>Test</title><style>body{}</style></head><body><p>Hello <b>World</b>!</p><script>alert('hi');</script></body></html>"
        expected_text = "Hello World!"
        self.assertEqual(self.digestifier._extract_text_from_html(html_content), expected_text)

    def test_split_into_sentences(self):
        text = "This is sentence one. This is sentence two! Is this sentence three? Yes, it is."
        expected_sentences = [
            "This is sentence one.",
            "This is sentence two!",
            "Is this sentence three?",
            "Yes, it is."
        ]
        self.assertEqual(self.digestifier._split_into_sentences(text), expected_sentences)

    def test_split_into_sentences_with_multiple_spaces(self):
        text = "Sentence one.  Sentence two!   Sentence three."
        expected_sentences = [
            "Sentence one.",
            "Sentence two!",
            "Sentence three."
        ]
        self.assertEqual(self.digestifier._split_into_sentences(text), expected_sentences)

    def test_split_into_sentences_empty_string(self):
        text = ""
        expected_sentences = []
        self.assertEqual(self.digestifier._split_into_sentences(text), expected_sentences)

    def test_split_into_sentences_no_punctuation(self):
        text = "This is a single line of text without punctuation"
        expected_sentences = [
            "This is a single line of text without punctuation"
        ]
        self.assertEqual(self.digestifier._split_into_sentences(text), expected_sentences)
