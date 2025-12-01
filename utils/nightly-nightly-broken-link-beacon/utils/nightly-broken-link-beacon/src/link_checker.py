import argparse
import os
import re
import requests
from typing import List, Tuple, Dict

# Regex to find markdown links: [text](url)
# It captures the URL part, ensuring it starts with http:// or https://
LINK_REGEX = re.compile(r'\[.*?\]\((https?://[^)]+?)\)')

class LinkChecker:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def extract_links_from_markdown(self, markdown_content: str) -> List[str]:
        """Extracts HTTP/HTTPS links from markdown content."""
        return LINK_REGEX.findall(markdown_content)

    def check_link_status(self, url: str) -> Tuple[str, str]:
        """Checks the HTTP status of a given URL."""
        try:
            # Use stream=True for efficiency (don't download entire body)
            # allow_redirects=True is default, but explicit for clarity
            with requests.get(url, timeout=self.timeout, stream=True, allow_redirects=True) as response:
                response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                return f"{response.status_code} {response.reason}", response.url # Return final URL after redirects
        except requests.exceptions.HTTPError as e:
            # If an HTTPError occurred, use its response's status and reason
            if e.response:
                return f"{e.response.status_code} {e.response.reason}", url
            return f"HTTP Error: {e}", url
        except requests.exceptions.ConnectionError:
            return "Connection Error", url
        except requests.exceptions.Timeout:
            return "Timeout Error", url
        except requests.exceptions.RequestException as e:
            return f"Request Error: {e}", url

    def scan_directory_for_markdown_files(self, directory: str) -> List[str]:
        """Finds all .md files in the given directory and its subdirectories."""
        markdown_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):
                    markdown_files.append(os.path.join(root, file))
        return markdown_files

    def run_scan(self, target_directory: str) -> Dict[str, List[Tuple[str, str, str]]]:
        """Runs the link checking scan and returns a report."""
        print(f"Scanning directory: {target_directory}\n")
        markdown_files = self.scan_directory_for_markdown_files(target_directory)
        report: Dict[str, List[Tuple[str, str, str]]] = {}
        broken_links_count = 0
        error_links_count = 0

        if not markdown_files:
            print("No markdown files found in the specified directory.")
            return {}

        for md_file in markdown_files:
            relative_path = os.path.relpath(md_file, target_directory)
            print(f"--- Checking links in {relative_path} ---")
            file_broken_links = []
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                links = self.extract_links_from_markdown(content)

                if not links:
                    print("  No external links found.")
                    report[md_file] = []
                    print()
                    continue

                for link in links:
                    status, final_url = self.check_link_status(link)
                    status_prefix = ""
                    if "200 OK" in status:
                        status_prefix = "[SUCCESS]"
                    elif "30" in status: # Covers 301, 302, etc.
                        status_prefix = "[REDIRECT]"
                    elif "40" in status or "50" in status: # Covers 4xx and 5xx errors
                        status_prefix = "[BROKEN ]"
                        broken_links_count += 1
                    else:
                        status_prefix = "[ERROR  ]"
                        error_links_count += 1

                    # Only show final_url if it's different from the original link (i.e., a redirect occurred)
                    display_url_info = f" -> {final_url}" if final_url != link else ""
                    print(f"{status_prefix} {link} ({status}{display_url_info})")
                    file_broken_links.append((link, status, final_url))

            except FileNotFoundError:
                print(f"  Error: File not found: {relative_path}")
            except Exception as e:
                print(f"  Error processing {relative_path}: {e}")
            report[md_file] = file_broken_links
            print()

        print(f"Scan complete. Found {broken_links_count} broken link(s) and {error_links_count} error(s).")
        return report

def main():
    parser = argparse.ArgumentParser(
        description="Scan markdown files for broken external links."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Directory to scan for markdown files (default: current directory)."
    )
    args = parser.parse_args()

    checker = LinkChecker()
    checker.run_scan(args.path)

if __name__ == "__main__":
    main()
