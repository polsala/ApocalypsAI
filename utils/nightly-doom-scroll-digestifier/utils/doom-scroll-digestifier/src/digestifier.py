import requests
import re
import sys
import argparse

DOOM_KEYWORDS = [
    'crisis', 'disaster', 'catastrophe', 'collapse', 'warning', 'threat', 'emergency',
    'apocalypse', 'doom', 'dire', 'grave', 'peril', 'risk', 'danger', 'unprecedented',
    'alarming', 'devastating', 'extinction', 'famine', 'epidemic', 'war', 'conflict',
    'meltdown', 'breakdown', 'struggle', 'suffering', 'tragedy', 'calamity'
]

DOOM_LEVEL_MAP = {
    0: 'Serene', 1: 'Calm', 2: 'Mild', 3: 'Moderate', 4: 'Elevated', 5: 'Concerning',
    6: 'High', 7: 'Severe', 8: 'Critical', 9: 'Cataclysmic', 10: 'Apocalyptic'
}

def fetch_url_content(url: str) -> str:
    """Fetches the HTML content from a given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}", file=sys.stderr)
        return ""

def strip_html(html_content: str) -> str:
    """Strips HTML tags and extracts plain text content."""
    # Remove script and style tags first
    cleaned_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    cleaned_content = re.sub(r'<style[^>]*>.*?</style>', '', cleaned_content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove all other HTML tags
    cleaned_content = re.sub(r'<[^>]+>', '', cleaned_content)
    
    # Replace multiple newlines/spaces with single ones
    cleaned_content = re.sub(r'\n\s*\n', '\n\n', cleaned_content)
    cleaned_content = re.sub(r'\s+', ' ', cleaned_content).strip()
    
    return cleaned_content

def analyze_doom_level(text: str) -> int:
    """Analyzes text for doom keywords and returns a doom level (0-10)."""
    text_lower = text.lower()
    
    # Count unique doom keywords found in the text
    unique_keywords_found = len(set(kw for kw in DOOM_KEYWORDS if kw in text_lower))

    # Scale directly: 1 unique keyword found = 1 point, up to a maximum of 10.
    # This provides a more intuitive 0-10 scale for 'doom level'.
    doom_level = min(unique_keywords_found, 10)
    return doom_level

def summarize_text(text: str, max_sentences: int = 3) -> str:
    """Summarizes the text by taking the first few sentences."""
    # Split by common sentence terminators, keeping the terminator with the sentence
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Filter out empty strings that might result from splitting
    sentences = [s.strip() for s in sentences if s.strip()]

    return ' '.join(sentences[:max_sentences])

def main():
    parser = argparse.ArgumentParser(
        description="Digest news articles, calculate a 'doom level', and provide a concise summary."
    )
    parser.add_argument('--url', type=str, required=True, help="URL of the news article to digest.")
    args = parser.parse_args()

    print(f"Fetching content from: {args.url}")
    html_content = fetch_url_content(args.url)
    if not html_content:
        sys.exit(1)

    plain_text = strip_html(html_content)
    if not plain_text:
        print("Could not extract plain text from the URL.", file=sys.stderr)
        sys.exit(1)

    doom_level = analyze_doom_level(plain_text)
    summary = summarize_text(plain_text)

    doom_description = DOOM_LEVEL_MAP.get(doom_level, 'Unknown')

    print(f"\nURL: {args.url}")
    print(f"Doom Level: {doom_level}/10 ({doom_description})")
    print(f"Summary: {summary}")

if __name__ == '__main__':
    main()
