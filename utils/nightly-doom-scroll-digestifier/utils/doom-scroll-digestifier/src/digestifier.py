import datetime
import re
from typing import List, Dict, Any

class DoomScrollDigestifier:
    """
    Processes a list of "doom-and-gloom" articles and distills them into a concise,
    less overwhelming digest.
    """

    def __init__(self, max_summary_sentences: int = 2, max_actionable_sentences: int = 1):
        self.max_summary_sentences = max_summary_sentences
        self.max_actionable_sentences = max_actionable_sentences

    def _summarize_text(self, text: str) -> str:
        """
        Simple summarization by taking the first few sentences.
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return ' '.join(sentences[:self.max_summary_sentences]).strip()

    def _extract_actionable_insights(self, text: str) -> str:
        """
        Attempts to extract actionable insights by looking for keywords.
        This is a very basic heuristic for demonstration.
        """
        action_keywords = ["prepare", "review", "ensure", "support", "reduce", "monitor", "secure", "update", "contribute"]
        sentences = re.split(r'(?<=[.!?])\s+', text)
        actionable_sentences = [
            s for s in sentences
            if any(keyword in s.lower() for keyword in action_keywords)
        ]
        return ' '.join(actionable_sentences[:self.max_actionable_sentences]).strip() or "No immediate action suggested."

    def digest(self, articles: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Processes a list of articles and returns a digested version.

        Args:
            articles: A list of dictionaries, each with 'title', 'content', and 'source'.

        Returns:
            A list of digested article dictionaries, each with 'title', 'summary',
            'actionable', and 'source'.
        """
        digested_articles = []
        for article in articles:
            summary = self._summarize_text(article.get('content', ''))
            actionable = self._extract_actionable_insights(article.get('content', ''))
            digested_articles.append({
                'title': article.get('title', 'Untitled'),
                'summary': summary,
                'actionable': actionable,
                'source': article.get('source', 'Unknown Source')
            })
        return digested_articles

    def format_digest_output(self, digested_articles: List[Dict[str, str]]) -> str:
        """
        Formats the digested articles into a human-readable string.
        """
        output = [
            "--- Doom-Scroll Digest ---",
            f"Date: {datetime.date.today().isoformat()}",
            ""
        ]
        for article in digested_articles:
            output.append(f"[{article['title']}]")
            output.append(f"Summary: {article['summary']}")
            output.append(f"Actionable: {article['actionable']}")
            output.append(f"Source: {article['source']}")
            output.append("")
        output.append("--- End Digest ---")
        return "\n".join(output)

def main():
    # Mock rationale: In a real-world scenario, this data would come from
    # an external news API or RSS feed. For a self-contained utility and
    # deterministic testing, we use a hardcoded list of articles.
    mock_articles = [
        {
            "title": "Global Warming Accelerates Beyond Projections",
            "content": "New scientific reports indicate that global temperatures are rising at an unprecedented rate, surpassing even the most pessimistic climate models. Polar ice caps are melting faster, contributing to accelerated sea-level rise. Urgent action is required to mitigate the long-term effects. Governments and individuals must support sustainable initiatives and reduce their carbon footprint. We need to prepare for significant environmental shifts.",
            "source": "ClimateWatch Daily"
        },
        {
            "title": "Major Cyberattack Disrupts Critical Infrastructure",
            "content": "A sophisticated, state-sponsored cyberattack has targeted critical infrastructure across several nations, leading to widespread power outages and communication disruptions. Security experts are working tirelessly to contain the threat and restore services. It is crucial for all organizations and individuals to review their cybersecurity practices, ensure strong passwords, and enable multi-factor authentication. Update your systems regularly to secure against new vulnerabilities.",
            "source": "TechSecurity News"
        },
        {
            "title": "New Strain of Super-Flu Emerges Globally",
            "content": "Health authorities are monitoring the rapid spread of a novel influenza strain with high transmissibility. While initial symptoms appear mild for most, vulnerable populations are at risk. Public health campaigns urge vaccination and adherence to hygiene protocols. Individuals should monitor local health advisories and prepare emergency kits. Contribute to community health by staying home if sick.",
            "source": "Global Health Monitor"
        },
        {
            "title": "Asteroid Near-Miss: A Wake-Up Call for Planetary Defense",
            "content": "An asteroid the size of a football field passed dangerously close to Earth last night, undetected until hours before its closest approach. This incident highlights the urgent need for enhanced planetary defense systems and better asteroid tracking capabilities. International cooperation is essential to secure our future. We must invest more in space observation.",
            "source": "Cosmic Events Weekly"
        },
        {
            "title": "Economic Downturn Deepens: Recession Fears Mount",
            "content": "Global markets are experiencing significant volatility as economic indicators point towards a deepening recession. Inflation remains high, and consumer spending is declining. Financial analysts advise individuals to review their budgets, save diligently, and diversify investments. Ensure your financial security by planning for the long term.",
            "source": "Financial Times"
        }
    ]

    digestifier = DoomScrollDigestifier()
    digested_content = digestifier.digest(mock_articles)
    print(digestifier.format_digest_output(digested_content))

if __name__ == "__main__":
    main()
