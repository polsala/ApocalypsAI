import datetime
import re
from typing import List, Dict

class DoomScrollDigestifier:
    """
    Processes a list of news items to create a concise, thematic digest.
    Identifies key themes and sentiments (doom vs. resilience) based on keywords.
    """

    DOOM_KEYWORDS = [
        "crisis", "collapse", "shortage", "famine", "disaster", "catastrophe",
        "extinction", "threat", "warning", "decline", "recession", "inflation",
        "unrest", "conflict", "pollution", "warming", "drought", "flood",
        "pandemic", "outbreak", "vulnerable", "fragile", "escalation"
    ]

    RESILIENCE_KEYWORDS = [
        "solution", "innovation", "recovery", "resilience", "adaptation",
        "progress", "breakthrough", "cooperation", "community", "support",
        "mitigation", "sustainable", "renewable", "initiative", "hope",
        "rebuild", "prepare", "strategy", "advance", "develop"
    ]

    def __init__(self):
        self.doom_count = 0
        self.resilience_count = 0
        self.themes = set()

    def _analyze_item(self, item: str) -> Dict[str, bool]:
        """Analyzes a single news item for doom and resilience keywords."""
        item_lower = item.lower()
        has_doom = any(keyword in item_lower for keyword in self.DOOM_KEYWORDS)
        has_resilience = any(keyword in item_lower for keyword in self.RESILIENCE_KEYWORDS)

        # Extract potential themes (simple keyword extraction for now)
        for keyword in self.DOOM_KEYWORDS + self.RESILIENCE_KEYWORDS:
            if keyword in item_lower:
                self.themes.add(keyword)

        if has_doom:
            self.doom_count += 1
        if has_resilience:
            self.resilience_count += 1

        return {"has_doom": has_doom, "has_resilience": has_resilience}

    def digest(self, news_items: List[str]) -> str:
        """
        Processes a list of news items and generates a summary digest.
        """
        self.doom_count = 0
        self.resilience_count = 0
        self.themes = set()
        
        if not news_items:
            return self._format_summary(
                "No news items to digest. Perhaps a moment of calm?",
                [],
                "No significant events detected."
            )

        for item in news_items:
            self._analyze_item(item)

        # Determine overall sentiment
        sentiment = self._determine_sentiment()
        
        # Refine themes for readability
        refined_themes = self._refine_themes(list(self.themes))

        return self._format_summary(
            "--- Doom Scroll Digest ---",
            refined_themes,
            sentiment
        )

    def _determine_sentiment(self) -> str:
        """Determines the overall sentiment based on keyword counts."""
        total_keywords = self.doom_count + self.resilience_count

        if total_keywords == 0:
            return "No strong sentiment detected. A quiet day, perhaps?"
        
        doom_ratio = self.doom_count / total_keywords
        resilience_ratio = self.resilience_count / total_keywords

        if doom_ratio > 0.7:
            return "Predominantly challenging outlook, with significant areas of concern. Vigilance is advised."
        elif resilience_ratio > 0.6:
            return "Despite ongoing challenges, a strong undercurrent of innovation and community-led solutions is evident. Hope persists."
        elif self.doom_count > 0 and self.resilience_count > 0:
            return "A mixed bag of challenges and emerging solutions. The future remains fluid, requiring adaptive strategies."
        elif self.doom_count > 0:
            return "Concerns are present, highlighting areas needing immediate attention."
        elif self.resilience_count > 0:
            return "Positive developments and proactive measures are noted, offering pathways forward."
        else:
            return "No strong sentiment detected. A quiet day, perhaps?"

    def _refine_themes(self, themes: List[str]) -> List[str]:
        """Refines raw keywords into more readable thematic statements."""
        
        # Group related keywords into broader themes
        final_themes = set()
        if any(k in themes for k in ["warming", "drought", "flood", "pollution", "extinction", "catastrophe", "disaster"]):
            final_themes.add("Global climate shifts and environmental degradation")
        if any(k in themes for k in ["recession", "inflation", "shortage", "decline", "crisis", "famine"]):
            final_themes.add("Economic instability and resource scarcity")
        if any(k in themes for k in ["unrest", "conflict", "escalation", "threat"]):
            final_themes.add("Geopolitical tensions and social unrest")
        if any(k in themes for k in ["pandemic", "outbreak", "vulnerable", "fragile"]):
            final_themes.add("Public health challenges")
        if any(k in themes for k in ["solution", "innovation", "breakthrough", "advance", "develop"]):
            final_themes.add("Technological advancements and innovative solutions")
        if any(k in themes for k in ["resilience", "adaptation", "cooperation", "community", "support", "rebuild", "prepare", "strategy"]):
            final_themes.add("Community resilience and adaptive strategies")
        if any(k in themes for k in ["sustainable", "renewable", "mitigation", "initiative", "progress"]):
            final_themes.add("Sustainable development and mitigation efforts")

        # Ensure unique and sorted output for final themes
        return sorted(list(final_themes))


    def _format_summary(self, title: str, themes: List[str], sentiment: str) -> str:
        """Formats the summary into a readable string."""
        current_date = datetime.date.today().strftime("%Y-%m-%d") # Mock rationale: Use fixed date for deterministic tests, or mock datetime.date.today()
        
        summary_parts = [
            title,
            f"Date: {current_date}",
            "\nKey Themes:"
        ]
        if themes:
            for theme in themes:
                summary_parts.append(f"- {theme}")
        else:
            summary_parts.append("- No specific themes identified.")

        summary_parts.append("\nOverall Sentiment:")
        summary_parts.append(sentiment)

        return "\n".join(summary_parts)

def main():
    """
    Main function to run the Doom Scroll Digestifier with mock data.
    """
    digestifier = DoomScrollDigestifier()

    # Mock news items for demonstration
    mock_news = [
        "Global warming accelerates, leading to unprecedented droughts and floods across continents.",
        "New agricultural innovations offer hope for sustainable food production amidst climate crisis.",
        "Economic recession deepens as supply chain shortages impact critical industries.",
        "Community initiatives for local resilience gain traction, fostering mutual support networks.",
        "Political unrest escalates in several regions, raising concerns about global stability.",
        "Breakthrough in renewable energy technology promises significant mitigation of carbon emissions.",
        "A new pandemic strain emerges, putting pressure on already fragile healthcare systems.",
        "International cooperation efforts aim to address resource scarcity and promote peace.",
        "Reports warn of impending ecological collapse due to unchecked pollution.",
        "Local groups prepare for future disasters with advanced preparedness strategies."
    ]

    digest = digestifier.digest(mock_news)
    print(digest)

if __name__ == "__main__":
    main()
