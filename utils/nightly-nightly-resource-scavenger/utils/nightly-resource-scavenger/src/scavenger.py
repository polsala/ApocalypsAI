import os
import re
import requests
import argparse
from typing import List, Tuple, Optional

# Install markdown-it-py: pip install markdown-it-py
from markdown_it import MarkdownIt

class LinkChecker:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.md = MarkdownIt()

    def extract_links_from_markdown(self, markdown_content: str) -> List[str]:
        """Extracts HTTP/HTTPS links from markdown content."""
        links = []
        tokens = self.md.parse(markdown_content)
        for token in tokens:
            if token.type == 'link_open':
                href = token.attrGet('href')
                if href and (href.startswith('http://') or href.startswith('https://')):
                    links.append(href)
        return links

    def check_link(self, url: str) -> Tuple[bool, str]:
        """Checks if a URL is reachable and returns its status."""
        try:
            response = requests.head(url, timeout=self.timeout, allow_redirects=True)
            # For HEAD requests, 2xx is success. Some servers might not support HEAD.
            # If HEAD returns a client/server error (>=400) and it's not a 405 (Method Not Allowed),
            # we try GET as a fallback to get a more accurate status.
            if response.status_code >= 400 and response.status_code != 405:
                response = requests.get(url, timeout=self.timeout, allow_redirects=True)

            if 200 <= response.status_code < 400:
                return True, f"{response.status_code} OK"
            else:
                return False, f"{response.status_code} {response.reason}"
        except requests.exceptions.ConnectionError:
            return False, "Connection Error"
        except requests.exceptions.Timeout:
            return False, "Timeout"
        except requests.exceptions.RequestException as e:
            return False, f"Request Error: {e}"

    def scan_directory(self, path: str) -> List[Tuple[str, str]]:
        """Scans a directory for markdown files and checks their links."""
        broken_links: List[Tuple[str, str]] = []
        all_checked_links: List[str] = []

        print(f"Scanning directory: {path}\n")

        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(('.md', '.markdown')):
                    filepath = os.path.join(root, file)
                    print(f"Processing file: {filepath}")
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        links = self.extract_links_from_markdown(content)
                        if not links:
                            print("  No external links found.")
                            continue

                        for link in links:
                            all_checked_links.append(link)
                            is_ok, status = self.check_link(link)
                            print(f"  Checking: {link} (Status: {status})")
                            if not is_ok:
                                broken_links.append((link, status))
                    except Exception as e:
                        print(f"  Error processing {filepath}: {e}")
        
        print("\n--- Scan Summary ---")
        print(f"Total links checked: {len(set(all_checked_links))}") # Use set to count unique links
        print(f"Broken links found: {len(broken_links)}")

        if broken_links:
            print("\nBroken Links:")
            for link, status in broken_links:
                print(f"- {link} ({status})")
        else:
            print("\nNo broken links found. The digital landscape is pristine!")

        return broken_links

def main():
    parser = argparse.ArgumentParser(
        description="Scans Markdown files for broken external links."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="The directory to scan for Markdown files. Defaults to current directory."
    )
    args = parser.parse_args()

    checker = LinkChecker()
    checker.scan_directory(args.path)

if __name__ == "__main__":
    main()
