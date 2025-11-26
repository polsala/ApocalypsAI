import os
import re
import argparse
import requests
from typing import List, Tuple, Dict, Set

def find_markdown_files(directory: str) -> List[str]:
    """Recursively finds all Markdown files in the given directory."""
    md_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.md', '.markdown')):
                md_files.append(os.path.join(root, file))
    return md_files

def extract_links_from_markdown(filepath: str) -> List[str]:
    """Extracts all HTTP/HTTPS links from a Markdown file."""
    all_found_links: Set[str] = set() # Use a set for automatic deduplication
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

            # 1. Find links in Markdown format: [text](url)
            markdown_link_pattern = re.compile(r'\[.*?\]\((https?://[^\s)]+)\)')
            for match in markdown_link_pattern.finditer(content):
                all_found_links.add(match.group(1))
            
            # 2. Find standalone URLs (e.g., https://example.com or <https://example.com>)
            # This pattern is more general and captures URLs not necessarily in markdown link syntax.
            # It covers common URL characters including hyphens and dots.
            url_pattern = re.compile(r'https?://(?:www\.)?[a-zA-Z0-9./?#=&_%\-]+')
            for match in url_pattern.finditer(content):
                all_found_links.add(match.group(0))

    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return sorted(list(all_found_links)) # Return as sorted list for deterministic testing

def check_link_status(url: str) -> Tuple[bool, str]:
    """Checks the status of a single URL using a HEAD request."""
    try:
        # Use a timeout to prevent hanging on unresponsive servers
        response = requests.head(url, timeout=5, allow_redirects=True)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return True, f"OK (Status: {response.status_code})"
    except requests.exceptions.HTTPError as e:
        return False, f"Status: {e.response.status_code} {e.response.reason}"
    except requests.exceptions.ConnectionError:
        return False, "Error: Connection Error"
    except requests.exceptions.Timeout:
        return False, "Error: Timeout"
    except requests.exceptions.RequestException as e:
        return False, f"Error: {e}"

def main():
    parser = argparse.ArgumentParser(description="Scavenge for broken links in Markdown files.")
    parser.add_argument('--path', type=str, default='.',
                        help='The directory to scan for Markdown files. Defaults to current directory.')
    args = parser.parse_args()

    scan_directory = os.path.abspath(args.path)
    print(f"Scanning for broken links in: {scan_directory}\n")

    md_files = find_markdown_files(scan_directory)
    print(f"Found {len(md_files)} Markdown files.\n")

    broken_links_by_file: Dict[str, List[Tuple[str, str]]] = {}
    total_broken_links = 0

    for md_file in md_files:
        links = extract_links_from_markdown(md_file)
        file_broken_links = []
        for link in links:
            is_ok, status_msg = check_link_status(link)
            if not is_ok:
                file_broken_links.append((link, status_msg))
                total_broken_links += 1
        if file_broken_links:
            broken_links_by_file[md_file] = file_broken_links

    if total_broken_links > 0:
        print("--- Broken Links Found ---")
        for filepath, links_info in broken_links_by_file.items():
            print(f"\nFile: {filepath}")
            for link, status_msg in links_info:
                print(f"  - {link} ({status_msg})")
        print("\n--- Scan Complete ---")
    else:
        print("--- Scan Complete ---")
        print("No broken links found. All clear!")
        print("---")

if __name__ == '__main__':
    main()
