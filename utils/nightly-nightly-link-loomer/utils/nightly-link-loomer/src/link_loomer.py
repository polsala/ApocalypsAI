import os
import re
import sys
import requests
from typing import List, Tuple, Dict

# Regex to find Markdown links: [text](url) or <url>
# It captures the URL in group 1 (for [text](url)) or group 2 (for <url>)
LINK_REGEX = re.compile(r'(?:\[[^\]]*\]\((https?://[^\s)]+)\)|<(https?://[^>]+)>)')

def find_markdown_files(directory: str) -> List[str]:
    """Recursively finds all Markdown files (.md) in the given directory."""
    markdown_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def extract_external_links(filepath: str) -> List[str]:
    """Extracts all unique external HTTP/HTTPS links from a Markdown file."""
    links = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            for match in LINK_REGEX.finditer(content):
                # Group 1 is for [text](url), Group 2 is for <url>
                link = match.group(1) or match.group(2)
                if link and (link.startswith('http://') or link.startswith('https://')):
                    links.add(link)
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return sorted(list(links))

def check_link(url: str) -> Tuple[bool, int]:
    """Checks if a given URL is accessible using a HEAD request."""
    try:
        # Use a short timeout to avoid hanging on unresponsive servers
        # Add a User-Agent header to be polite and avoid some blocking
        headers = {'User-Agent': 'ApocalypsAI/NightlyLinkLoomer (https://github.com/polsala/ApocalypsAI)'}
        response = requests.head(url, timeout=5, allow_redirects=True, headers=headers)
        # Consider 2xx and 3xx as successful (including redirects)
        return 200 <= response.status_code < 400, response.status_code
    except requests.exceptions.RequestException:
        # Catch all requests-related exceptions (connection errors, timeouts, etc.)
        return False, 0 # 0 indicates a network/request error
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error checking link {url}: {e}")
        return False, -1 # -1 indicates an unknown error

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/link_loomer.py <directory_path>")
        sys.exit(1)

    target_directory = sys.argv[1]
    if not os.path.isdir(target_directory):
        print(f"Error: Directory not found: {target_directory}")
        sys.exit(1)

    print(f"\nScanning '{target_directory}' for broken links...\n")

    all_markdown_files = find_markdown_files(target_directory)
    broken_links_found: Dict[str, List[Tuple[str, int]]] = {}

    if not all_markdown_files:
        print("No Markdown files found to scan.")
        sys.exit(0)

    for md_file in all_markdown_files:
        print(f"  Processing {md_file}...")
        external_links = extract_external_links(md_file)
        file_broken_links = []
        for link in external_links:
            is_valid, status_code = check_link(link)
            if not is_valid:
                status_msg = f" (Status: {status_code})" if status_code > 0 else " (Network Error)"
                file_broken_links.append((link, status_code))
                print(f"    ❌ Broken link found: {link}{status_msg}")
            # else:
            #     print(f"    ✅ Valid link: {link}") # Uncomment for verbose output
        if file_broken_links:
            broken_links_found[md_file] = file_broken_links

    print("\n--- Scan Complete ---\n")

    if broken_links_found:
        print("The Nightly Link-Loomer has detected the following digital decay:\n")
        for file, links in broken_links_found.items():
            print(f"File: {file}")
            for link, status in links:
                status_msg = f" (Status: {status})" if status > 0 else " (Network Error)"
                print(f"  - {link}{status_msg}")
        sys.exit(1) # Exit with 1 to indicate issues found
    else:
        print("All external links are robust! The digital fabric holds strong. ✅")
        sys.exit(0)

if __name__ == '__main__':
    main()
