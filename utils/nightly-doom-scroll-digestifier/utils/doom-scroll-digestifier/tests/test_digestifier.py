import unittest
from unittest.mock import patch
import datetime
from src.digestifier import DoomScrollDigestifier

class TestDoomScrollDigestifier(unittest.TestCase):

    def setUp(self):
        self.digestifier = DoomScrollDigestifier(max_summary_sentences=2, max_actionable_sentences=1)
        self.mock_articles = [
            {
                "title": "Test Article 1: Climate Crisis",
                "content": "This is the first sentence about climate. It talks about rising temperatures. Urgent action is required to mitigate effects. Individuals must support sustainable initiatives. Reduce your carbon footprint.",
                "source": "Climate News"
            },
            {
                "title": "Test Article 2: Tech Threat",
                "content": "A major cyberattack occurred. It caused significant disruption. Review your cybersecurity practices. Ensure strong passwords. Update systems regularly.",
                "source": "Cyber Daily"
            },
            {
                "title": "Test Article 3: No Action",
                "content": "This article has no clear actionable advice. It just describes a problem. The problem is very complex and difficult to solve. There are no easy answers here.",
                "source": "Problem Report"
            }
        ]

    def test_summarize_text(self):
        text = "This is the first sentence. This is the second sentence. This is the third sentence."
        summary = self.digestifier._summarize_text(text)
        self.assertEqual(summary, "This is the first sentence. This is the second sentence.")

        text_short = "Only one sentence."
        summary_short = self.digestifier._summarize_text(text_short)
        self.assertEqual(summary_short, "Only one sentence.")

        text_empty = ""
        summary_empty = self.digestifier._summarize_text(text_empty)
        self.assertEqual(summary_empty, "")

    def test_extract_actionable_insights(self):
        text = "You must prepare for the worst. Review your plans. This is a non-actionable sentence. Ensure all systems are secure."
        actionable = self.digestifier._extract_actionable_insights(text)
        self.assertEqual(actionable, "You must prepare for the worst.") # Only takes max_actionable_sentences=1

        text_no_action = "This is a descriptive sentence. Another descriptive sentence follows. No action words here."
        actionable_no_action = self.digestifier._extract_actionable_insights(text_no_action)
        self.assertEqual(actionable_no_action, "No immediate action suggested.")

        text_multiple_action = "Support local businesses. Reduce waste. Monitor your health. Update your software."
        actionable_multiple = self.digestifier._extract_actionable_insights(text_multiple_action)
        self.assertEqual(actionable_multiple, "Support local businesses.") # Only takes max_actionable_sentences=1

    def test_digest_articles(self):
        digested = self.digestifier.digest(self.mock_articles)
        self.assertEqual(len(digested), 3)

        # Test Article 1
        self.assertEqual(digested[0]['title'], "Test Article 1: Climate Crisis")
        self.assertEqual(digested[0]['summary'], "This is the first sentence about climate. It talks about rising temperatures.")
        self.assertEqual(digested[0]['actionable'], "Urgent action is required to mitigate effects.")
        self.assertEqual(digested[0]['source'], "Climate News")

        # Test Article 2
        self.assertEqual(digested[1]['title'], "Test Article 2: Tech Threat")
        self.assertEqual(digested[1]['summary'], "A major cyberattack occurred. It caused significant disruption.")
        self.assertEqual(digested[1]['actionable'], "Review your cybersecurity practices.")
        self.assertEqual(digested[1]['source'], "Cyber Daily")

        # Test Article 3
        self.assertEqual(digested[2]['title'], "Test Article 3: No Action")
        self.assertEqual(digested[2]['summary'], "This article has no clear actionable advice. It just describes a problem.")
        self.assertEqual(digested[2]['actionable'], "No immediate action suggested.")
        self.assertEqual(digested[2]['source'], "Problem Report")

    @patch('datetime.date')
    def test_format_digest_output(self, mock_date):
        # Mock rationale: datetime.date.today() is non-deterministic.
        # Patching it ensures the date in the output is always the same for testing.
        mock_date.today.return_value = datetime.date(2023, 10, 27)
        mock_date.isoformat.return_value = "2023-10-27"

        digested_articles = [
            {
                'title': 'Mock Title',
                'summary': 'Mock Summary.',
                'actionable': 'Mock Action.',
                'source': 'Mock Source'
            }
        ]
        output = self.digestifier.format_digest_output(digested_articles)
        expected_output = (
            "--- Doom-Scroll Digest ---\n"
            "Date: 2023-10-27\n"
            "\n"
            "[Mock Title]\n"
            "Summary: Mock Summary.\n"
            "Actionable: Mock Action.\n"
            "Source: Mock Source\n"
            "\n"
            "--- End Digest ---"
        )
        self.assertEqual(output, expected_output)

    def test_digestifier_with_different_sentence_counts(self):
        digestifier_custom = DoomScrollDigestifier(max_summary_sentences=1, max_actionable_sentences=2)
        digested = digestifier_custom.digest(self.mock_articles)

        self.assertEqual(digested[0]['summary'], "This is the first sentence about climate.")
        self.assertEqual(digested[0]['actionable'], "Urgent action is required to mitigate effects. Individuals must support sustainable initiatives.")

        self.assertEqual(digested[1]['summary'], "A major cyberattack occurred.")
        self.assertEqual(digested[1]['actionable'], "Review your cybersecurity practices. Ensure strong passwords.")


if __name__ == '__main__':
    unittest.main()
