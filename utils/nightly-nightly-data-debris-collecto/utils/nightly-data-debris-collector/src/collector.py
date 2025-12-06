import os
import re
import argparse
import requests
from typing import List, Dict, Tuple

# Regex to find URLs: Markdown links and raw URLs
# Group 1 captures URL from markdown link [text](url)
# Group 2 captures raw URL https://example.com
URL_REGEX = re.compile(r'\[.*?\]\((https?://[^\s)]+)\)|(https?://[^\s]+)')

def find_urls_in_text(text: str) -> List[str]:
    """Extracts unique URLs from a given text using regex."""
    urls = []
    for match in URL_REGEX.finditer(text):
        if match.group(1): # Markdown link URL
            urls.append(match.group(1))
        elif match.group(2): # Raw URL
            urls.append(match.group(2))
    return list(set(urls)) # Return unique URLs

def check_url_reachability(url: str, timeout: float = 5.0) -> bool:
    """Checks if a URL is reachable by making a HEAD request, falling back to GET if HEAD is not allowed.
    Returns True if reachable (2xx status), False otherwise."""
    try:
        # Try HEAD request first for efficiency and to avoid downloading content
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return True
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 405: # Method Not Allowed, try GET
            try:
                response = requests.get(url, timeout=timeout, allow_redirects=True)
                response.raise_for_status()
                return True
            except requests.exceptions.RequestException:
                return False
        return False # Other HTTP errors (e.g., 404, 500) are considered unreachable
    except requests.exceptions.RequestException:
        # Catch all other requests exceptions (ConnectionError, Timeout, TooManyRedirects, etc.)
        return False

def collect_broken_links(root_dir: str, file_types: List[str], timeout: float = 5.0) -> Dict[str, List[str]]:
    """Collects broken links from files within the specified directory.
    Returns a dictionary where keys are file paths and values are lists of broken URLs."""
    broken_links: Dict[str, List[str]] = {}

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if file extension matches any of the specified types
            if any(filename.endswith(f'.{ext}') for ext in file_types):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    urls = find_urls_in_text(content)
                    for url in urls:
                        if not check_url_reachability(url, timeout):
                            if filepath not in broken_links:
                                broken_links[filepath] = []
                            broken_links[filepath].append(url)
                except Exception as e:
                    # Print error for file access issues but continue processing other files
                    print(f"Error processing file {filepath}: {e}")

    return broken_links

def main():
    parser = argparse.ArgumentParser(description="Collects broken external links from repository files.")
    parser.add_argument('--path', type=str, default='.',
                        help='Root directory to start scanning from. Defaults to current directory.')
    parser.add_argument('--file-types', type=str, default='md,py,txt',
                        help='Comma-separated list of file extensions to scan (e.g., md,py,txt).')
    parser.add_argument('--timeout', type=float, default=5.0,
                        help='Timeout in seconds for checking URL reachability. Defaults to 5.0.')

    args = parser.parse_args()

    file_types = [ft.strip() for ft in args.file_types.split(',')]

    print(f"Scanning '{args.path}' for broken links in {file_types} files with a {args.timeout}s timeout...")
    broken_links = collect_broken_links(args.path, file_types, args.timeout)

    if broken_links:
        print("\n--- Broken Links Found ---")
        for filepath, urls in broken_links.items():
            for url in urls:
                print(f"Broken Link in {filepath}: {url}")
        print("\n--- End of Report ---")
        exit(1) # Indicate failure if broken links are found
    else:
        print("\nNo broken links found. Repository is pristine!")
        exit(0) # Indicate success

if __name__ == '__main__':
    main()
