import re
import sys
import os
import requests
from typing import List, Tuple

# Define a User-Agent to avoid being blocked by some servers
HEADERS = {
    'User-Agent': 'ApocalypsAI/NightlyResourceScavengerLinkChecker (https://github.com/polsala/ApocalypsAI)'
}

def extract_links_from_markdown(markdown_content: str) -> List[str]:
    """
    Extracts all HTTP/HTTPS links from a given Markdown content.
    Supports inline links `[text](url)` and reference links `[text]: url`.
    """
    links = []

    # Regex for inline links: [text](url)
    inline_link_pattern = re.compile(r'\[.*?\]\((https?://[^\s)]+)\)')
    links.extend(inline_link_pattern.findall(markdown_content))

    # Regex for reference links: [text]: url
    reference_link_pattern = re.compile(r'^\s*\[.*?\]:\s*(https?://[^\s]+)', re.MULTILINE)
    links.extend(reference_link_pattern.findall(markdown_content))

    # Regex for bare URLs (e.g., just "http://example.com" in text)
    bare_url_pattern = re.compile(r'(?<!\]\()(https?://[^\s)]+)')
    links.extend(bare_url_pattern.findall(markdown_content))

    return sorted(list(set(links))) # Return unique and sorted links

def check_link(url: str, timeout: int = 10) -> Tuple[bool, str]:
    """
    Checks if a given URL is accessible.
    Returns (True, "OK") for success, or (False, "Error message") for failure.
    """
    try:
        response = requests.head(url, timeout=timeout, headers=HEADERS, allow_redirects=True)
        # Use HEAD request for efficiency, but allow redirects to get final status
        if response.status_code >= 200 and response.status_code < 400:
            return True, "OK"
        else:
            return False, f"Status: {response.status_code} {response.reason}"
    except requests.exceptions.ConnectionError:
        return False, "Error: Connection refused/failed"
    except requests.exceptions.Timeout:
        return False, "Error: Timeout"
    except requests.exceptions.RequestException as e:
        return False, f"Error: {e}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/link_checker.py <markdown_file1> [<markdown_file2> ...]")
        sys.exit(1)

    markdown_files = sys.argv[1:]
    all_links_ok = True

    for file_path in markdown_files:
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            all_links_ok = False
            continue

        print(f"Scanning: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}", file=sys.stderr)
            all_links_ok = False
            continue

        links = extract_links_from_markdown(content)

        if not links:
            print("  No external links found.")
            continue

        for link in links:
            is_ok, message = check_link(link)
            if is_ok:
                print(f"  [✓] {link}")
            else:
                print(f"  [✗] {link} ({message})")
                all_links_ok = False
        print() # Newline for readability between files

    if not all_links_ok:
        sys.exit(1) # Exit with error code if any link was broken

if __name__ == "__main__":
    main()
