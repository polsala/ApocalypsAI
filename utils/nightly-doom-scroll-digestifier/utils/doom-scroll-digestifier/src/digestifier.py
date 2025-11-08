import requests
from bs4 import BeautifulSoup
import argparse
import re

class Digestifier:
    DOOM_KEYWORDS = ['crisis', 'catastrophe', 'collapse', 'threat', 'disaster', 'apocalypse', 'doom', 'warning', 'emergency', 'famine', 'war', 'extinction']
    SILVER_LINING_KEYWORDS = ['hope', 'solution', 'progress', 'recovery', 'breakthrough', 'innovation', 'resilience', 'opportunity', 'improvement', 'peace', 'growth']

    def fetch_article_content(self, url: str) -> str:
        """Fetches the HTML content of a given URL."""
        try:
            headers = {'User-Agent': 'ApocalypsAI-DoomScrollDigestifier/1.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return ""

    def extract_main_text(self, html_content: str) -> str:
        """Extracts the main readable text from HTML content."""
        if not html_content:
            return ""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script, style, and other non-content elements
        for script_or_style in soup(['script', 'style', 'header', 'footer', 'nav', 'aside', 'form', 'img', 'svg']):
            script_or_style.decompose()

        # Find common article containers or just all paragraphs
        article_body = soup.find('article') or soup.find('main') or soup.find('div', class_=re.compile(r'article|content|body', re.I))

        if article_body:
            text_elements = article_body.find_all(['p', 'h1', 'h2', 'h3', 'li'])
        else:
            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])

        text = '\n\n'.join([elem.get_text(separator=' ', strip=True) for elem in text_elements])
        return text.strip()

    def summarize_text(self, text: str, num_sentences: int = 3) -> str:
        """Summarizes text by returning the first N sentences."""
        if not text:
            return ""
        # Split by common sentence terminators, keeping the terminator with the sentence
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return ' '.join(sentences[:num_sentences])

    def analyze_sentiment(self, text: str) -> tuple[str, list[str]]:
        """Analyzes text for doom or silver lining keywords."""
        if not text:
            return "Neutral", []

        text_lower = text.lower()
        found_doom = [k for k in self.DOOM_KEYWORDS if k in text_lower]
        found_silver_lining = [k for k in self.SILVER_LINING_KEYWORDS if k in text_lower]

        if len(found_doom) > len(found_silver_lining):
            return "Doom-laden", found_doom
        elif len(found_silver_lining) > len(found_doom):
            return "Hopeful", found_silver_lining
        else:
            return "Neutral", []

def main():
    parser = argparse.ArgumentParser(description="Digest a news article for summary and sentiment.")
    parser.add_argument('--url', type=str, required=True, help="The URL of the article to digest.")
    parser.add_argument('--sentences', type=int, default=3, help="Number of sentences for the summary.")

    args = parser.parse_args()

    digestifier = Digestifier()

    print(f"Article URL: {args.url}\n")

    html_content = digestifier.fetch_article_content(args.url)
    if not html_content:
        print("Could not fetch article content.")
        return

    main_text = digestifier.extract_main_text(html_content)
    if not main_text:
        print("Could not extract main text from the article.")
        return

    summary = digestifier.summarize_text(main_text, args.sentences)
    sentiment, keywords = digestifier.analyze_sentiment(main_text)

    print("--- Summary ---")
    print(summary)
    print("\n--- Sentiment Analysis ---")
    if keywords:
        print(f"Overall Mood: {sentiment} (Keywords: {', '.join(keywords)})\n")
    else:
        print(f"Overall Mood: {sentiment}\n")

    print("--- Full Article Snippet ---")
    print(main_text[:500] + ('...' if len(main_text) > 500 else ''))

if __name__ == '__main__':
    main()
