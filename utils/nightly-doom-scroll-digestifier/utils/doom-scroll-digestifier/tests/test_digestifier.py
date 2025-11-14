import unittest
from unittest.mock import patch
import datetime
from src.digestifier import DoomScrollDigestifier

class TestDoomScrollDigestifier(unittest.TestCase):

    @patch('datetime.date') # Mock rationale: Ensure deterministic date for summary output.
    def setUp(self, mock_date):
        self.digestifier = DoomScrollDigestifier()
        mock_date.today.return_value = datetime.date(2242, 10, 27) # Fixed date for tests

    def test_empty_news_list(self):
        """Test with an empty list of news items."""
        news_items = []
        digest = self.digestifier.digest(news_items)
        self.assertIn("No news items to digest. Perhaps a moment of calm?", digest)
        self.assertIn("No significant events detected.", digest)
        self.assertIn("Date: 2242-10-27", digest)

    def test_all_doom_news(self):
        """Test with news items predominantly featuring doom keywords."""
        news_items = [
            "Global warming accelerates, leading to unprecedented droughts and floods.",
            "Economic recession deepens as supply chain shortages impact critical industries.",
            "Political unrest escalates in several regions, raising concerns about global stability.",
            "Reports warn of impending ecological collapse due to unchecked pollution."
        ]
        digest = self.digestifier.digest(news_items)
        self.assertIn("--- Doom Scroll Digest ---", digest)
        self.assertIn("Date: 2242-10-27", digest)
        self.assertIn("Key Themes:", digest)
        self.assertIn("- Global climate shifts and environmental degradation", digest)
        self.assertIn("- Economic instability and resource scarcity", digest)
        self.assertIn("- Geopolitical tensions and social unrest", digest)
        self.assertIn("Overall Sentiment:", digest)
        self.assertIn("Predominantly challenging outlook, with significant areas of concern. Vigilance is advised.", digest)
        
        # Ensure no resilience themes appear
        self.assertNotIn("Community resilience", digest)
        self.assertNotIn("Technological advancements", digest)

    def test_all_resilience_news(self):
        """Test with news items predominantly featuring resilience keywords."""
        news_items = [
            "New agricultural innovations offer hope for sustainable food production.",
            "Community initiatives for local resilience gain traction, fostering mutual support networks.",
            "Breakthrough in renewable energy technology promises significant mitigation of carbon emissions.",
            "International cooperation efforts aim to address resource scarcity and promote peace."
        ]
        digest = self.digestifier.digest(news_items)
        self.assertIn("--- Doom Scroll Digest ---", digest)
        self.assertIn("Date: 2242-10-27", digest)
        self.assertIn("Key Themes:", digest)
        self.assertIn("- Technological advancements and innovative solutions", digest)
        self.assertIn("- Community resilience and adaptive strategies", digest)
        self.assertIn("- Sustainable development and mitigation efforts", digest)
        self.assertIn("Overall Sentiment:", digest)
        self.assertIn("Despite ongoing challenges, a strong undercurrent of innovation and community-led solutions is evident. Hope persists.", digest)
        
        # Ensure no doom themes appear
        self.assertNotIn("Global climate shifts", digest)
        self.assertNotIn("Economic instability", digest)

    def test_mixed_news(self):
        """Test with a mix of doom and resilience keywords."""
        news_items = [
            "Global warming accelerates, leading to unprecedented droughts.",
            "New agricultural innovations offer hope for sustainable food production.",
            "Economic recession deepens as supply chain shortages.",
            "Community initiatives for local resilience gain traction.",
            "Political unrest escalates in several regions.",
            "Breakthrough in renewable energy technology promises significant mitigation.",
            "A new pandemic strain emerges, putting pressure on fragile healthcare systems.",
            "International cooperation efforts aim to address resource scarcity."
        ]
        digest = self.digestifier.digest(news_items)
        self.assertIn("--- Doom Scroll Digest ---", digest)
        self.assertIn("Date: 2242-10-27", digest)
        self.assertIn("Key Themes:", digest)
        self.assertIn("- Global climate shifts and environmental degradation", digest)
        self.assertIn("- Economic instability and resource scarcity", digest)
        self.assertIn("- Geopolitical tensions and social unrest", digest)
        self.assertIn("- Public health challenges", digest)
        self.assertIn("- Technological advancements and innovative solutions", digest)
        self.assertIn("- Community resilience and adaptive strategies", digest)
        self.assertIn("- Sustainable development and mitigation efforts", digest)
        self.assertIn("Overall Sentiment:", digest)
        self.assertIn("A mixed bag of challenges and emerging solutions. The future remains fluid, requiring adaptive strategies.", digest)

    def test_no_strong_keywords(self):
        """Test with news items that don't contain strong doom or resilience keywords."""
        news_items = [
            "Local council discusses new park benches.",
            "Cat rescued from tree in suburban area.",
            "New recipe for vegan stew published online."
        ]
        digest = self.digestifier.digest(news_items)
        self.assertIn("No specific themes identified.", digest)
        self.assertIn("No strong sentiment detected. A quiet day, perhaps?", digest)

    def test_keyword_counting(self):
        """Verify that doom and resilience counts are correctly updated."""
        news_items = [
            "Crisis looms, but solutions are being developed.", # 1 doom, 1 resilience
            "Famine threat, yet community support grows.",      # 1 doom, 1 resilience
            "Pure doom and collapse.",                          # 2 doom
            "Pure innovation and progress."                     # 2 resilience
        ]
        self.digestifier.digest(news_items)
        self.assertEqual(self.digestifier.doom_count, 4)
        self.assertEqual(self.digestifier.resilience_count, 4)

    def test_theme_refinement_logic(self):
        """Test the theme refinement and grouping logic."""
        news_items = [
            "Global warming causes severe droughts.",
            "New renewable energy initiatives launched.",
            "Economic recession impacts supply chains.",
            "Community support for adaptation strategies."
        ]
        digest = self.digestifier.digest(news_items)
        self.assertIn("- Global climate shifts and environmental degradation", digest)
        self.assertIn("- Economic instability and resource scarcity", digest)
        self.assertIn("- Sustainable development and mitigation efforts", digest)
        self.assertIn("- Community resilience and adaptive strategies", digest)
        
        # Ensure specific keywords are grouped into broader themes
        self.assertNotIn("warming", digest)
        self.assertNotIn("droughts", digest)
        self.assertNotIn("recession", digest)
        self.assertNotIn("supply chains", digest)
        self.assertNotIn("renewable", digest)
        self.assertNotIn("adaptation", digest)


if __name__ == '__main__':
    unittest.main()
