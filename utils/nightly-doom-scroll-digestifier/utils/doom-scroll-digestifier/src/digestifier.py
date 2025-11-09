import argparse
import re
import requests
import random
from typing import List

class DoomScrollDigestifier:
    DOOM_KEYWORDS = [
        'crisis', 'collapse', 'threat', 'warning', 'catastrophe', 'disaster',
        'apocalypse', 'doom', 'gloom', 'struggle', 'decline', 'peril', 'emergency'
    ]
    WHIMSICAL_SPINS = [
        "Remember, every cloud has a silver lining, even if it's radioactive. Stay vigilant, but don't forget to hydrate!",
        "Well, that escalated quickly! But hey, at least the sun came up today... probably.",
        "It's not the end of the world, just a particularly spicy Tuesday. Keep calm and carry on (or run).",
        "Looks like we're all in this together. Time to practice those survival skills, or just enjoy a nice cup of tea."
    ]

    def __init__(self):
        pass

    def _extract_text_from_html(self, html_content: str) -> str:
        """Basic HTML tag stripping to get plain text."""
        # Remove script and style tags first
        cleaned = re.sub(r'<script.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        cleaned = re.sub(r'<style.*?</style>', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
        # Remove all other HTML tags
        cleaned = re.sub(r'<[^>]+>', '', cleaned)
        # Replace multiple newlines/spaces with single space
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    def _split_into_sentences(self, text: str) -> List[str]:
        """Splits text into sentences using common delimiters."""
        # Simple regex for sentence splitting (handles . ! ? followed by space or end of string)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def digest(self, url: str) -> str:
        """
        Fetches content from the URL, extracts doom-laden sentences, and adds a whimsical spin.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.exceptions.RequestException as e:
            return f"Error fetching URL {url}: {e}"

        html_content = response.text
        plain_text = self._extract_text_from_html(html_content)
        sentences = self._split_into_sentences(plain_text)

        doom_sentences = []
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in self.DOOM_KEYWORDS):
                doom_sentences.append(sentence)
            if len(doom_sentences) >= 5: # Limit to top 5 doom sentences for brevity
                break
        
        if not doom_sentences:
            return (
                "--- Doom Scroll Digest --- \n\n" +
                "No significant signs of impending doom detected today! " +
                "Perhaps the apocalypse is taking a coffee break. Enjoy the peace while it lasts!"
            )

        digest_output = "--- Doom Scroll Digest --- \n\nDetected signals of impending doom:\n"
        for s in doom_sentences:
            digest_output += f"- \"{s}\" \n"
        
        whimsical_spin = random.choice(self.WHIMSICAL_SPINS)
        digest_output += f"\n{whimsical_spin}\n"

        return digest_output

def main():
    parser = argparse.ArgumentParser(
        description="Digest doom-laden news from a URL with a whimsical spin."
    )
    parser.add_argument("--url", required=True, help="The URL to fetch and digest.")
    args = parser.parse_args()

    digestifier = DoomScrollDigestifier()
    print(digestifier.digest(args.url))

if __name__ == "__main__":
    main()
