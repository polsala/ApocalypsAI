import argparse
import re
import os
import sys
from urllib.parse import urlparse
import requests

# Whitelist for domains that are intentionally unreachable or local
# Mock rationale: In a real scenario, you might want to ignore certain internal or known-broken links.
# For deterministic testing, this also helps control which URLs are considered 'external' and thus checked.
IGNORED_DOMAINS = [
    'localhost',
    '127.0.0.1',
    'example.com', # Often used in documentation as a placeholder
    'unreachable-domain.com', # Used for testing connection errors
]

def find_urls_in_markdown(content: str) -> list[str]:
    """
    Finds all URLs in Markdown content, including [text](url) and bare URLs.
    """
    urls = []
    # Markdown links: [text](url)
    markdown_link_pattern = re.compile(r'\[[^\]]+\]\((https?://[^\)]+)\)')
    urls.extend(markdown_link_pattern.findall(content))

    # Bare URLs: https://example.com or http://example.com
    # This pattern is designed to capture common URL structures without being overly greedy.
    bare_url_pattern = re.compile(r'(https?://[\w./?#=&;%\-]+)')
    urls.extend(bare_url_pattern.findall(content))

    # Filter out duplicates and ensure unique URLs, then sort for deterministic output
    return sorted(list(set(urls)))

def check_url(url: str) -> tuple[bool, int | str]:
    """
    Checks if a URL is reachable. Returns (is_reachable, status_code/error_message).
    # Mock rationale: Network requests are non-deterministic and slow. This function is designed
    # to be easily mocked in tests to simulate various network conditions (success, 404, connection error).
    """
    parsed_url = urlparse(url)
    if parsed_url.netloc in IGNORED_DOMAINS:
        return True, 'IGNORED'

    try:
        # Use a short timeout to avoid hanging on unresponsive servers
        response = requests.head(url, timeout=5, allow_redirects=True)
        # Consider 2xx and 3xx as successful
        if 200 <= response.status_code < 400:
            return True, response.status_code
        else:
            return False, response.status_code
    except requests.exceptions.ConnectionError:
        return False, 'Connection Error'
    except requests.exceptions.Timeout:
        return False, 'Timeout'
    except requests.exceptions.RequestException as e:
        return False, f'Request Error: {e}'
    except Exception as e:
        return False, f'Unexpected Error: {e}'

def scan_directory_for_broken_links(directory_path: str):
    """
    Scans a directory for Markdown files and checks for broken links.
    Exits with 1 if any broken links are found, 0 otherwise.
    """
    print(f"Scanning directory: {directory_path}\n")
    broken_links_found = 0
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(('.md', '.markdown')):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    urls = find_urls_in_markdown(content)
                    if not urls:
                        continue

                    file_has_broken_links = False
                    for url in urls:
                        is_reachable, status_or_error = check_url(url)
                        if not is_reachable:
                            if not file_has_broken_links:
                                print(f"File: {file_path}")
                                file_has_broken_links = True
                            print(f"  [BROKEN] {url} (Status: {status_or_error})")
                            broken_links_found += 1
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
    
    print(f"\nScan complete. Found {broken_links_found} broken/unreachable links.")
    if broken_links_found > 0:
        sys.exit(1) # Indicate failure if broken links are found
    else:
        sys.exit(0) # Indicate success


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Scan Markdown files for broken external links.'
    )
    parser.add_argument(
        '--path', 
        type=str, 
        default='.', 
        help='The directory path to scan for Markdown files.'
    )
    args = parser.parse_args()
    scan_directory_for_broken_links(args.path)
