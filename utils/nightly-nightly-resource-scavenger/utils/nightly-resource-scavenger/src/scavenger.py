import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict

import requests

# Regex to find HTTP/HTTPS links. It's basic and might miss some edge cases,
# but covers common Markdown/HTML link patterns.
LINK_REGEX = re.compile(r'https?://(?:www\.)?[a-zA-Z0-9./?#=\-_&%]+')

def extract_links(content: str) -> List[str]:
    """Extracts all unique HTTP/HTTPS links from a given string content."""
    return sorted(list(set(LINK_REGEX.findall(content))))

def check_link(url: str) -> Tuple[bool, int]:
    """Checks if a given URL is reachable and returns its status code.

    Returns: (is_ok, status_code)
    """
    try:
        # Use a short timeout to avoid hanging on unresponsive servers
        # and disable SSL verification for broader compatibility, though
        # in a real-world scenario, this might be configurable.
        response = requests.head(url, timeout=5, allow_redirects=True, verify=False)
        # Consider 2xx and 3xx as 'OK' for a link checker
        return 200 <= response.status_code < 400, response.status_code
    except requests.exceptions.RequestException:
        return False, 0  # 0 indicates a network error or timeout

def scan_file(filepath: Path) -> Dict[str, Tuple[bool, int]]:
    """Scans a single file for links and checks their status."""
    if not filepath.is_file():
        print(f"Warning: File not found: {filepath}", file=sys.stderr)
        return {}

    try:
        content = filepath.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        print(f"Warning: Could not decode file {filepath}. Skipping.", file=sys.stderr)
        return {}

    links = extract_links(content)
    results = {}
    for link in links:
        is_ok, status_code = check_link(link)
        results[link] = (is_ok, status_code)
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Scans files for external HTTP/HTTPS links and reports broken ones."
    )
    parser.add_argument(
        "--files",
        nargs='+',
        required=True,
        help="One or more file paths to scan for broken links."
    )

    args = parser.parse_args()
    all_files = [Path(f) for f in args.files]

    print("Scanning files for broken links...\n")

    total_broken_links = 0
    for filepath in all_files:
        print(f"File: {filepath}")
        file_results = scan_file(filepath)
        if not file_results:
            print("  No links found or file could not be processed.")
            continue

        file_broken_count = 0
        for link, (is_ok, status_code) in file_results.items():
            status_icon = '✅' if is_ok else '❌'
            status_text = f"{status_code} OK" if is_ok else f"{status_code} Not Found" if status_code == 404 else f"{status_code} Error"
            if not is_ok and status_code == 0: # Network error
                status_text = "Network Error/Timeout"

            print(f"  {status_icon} {link} ({status_text})")
            if not is_ok:
                file_broken_count += 1
        total_broken_links += file_broken_count
        print()

    print(f"Scan complete. Found {total_broken_links} broken link{'s' if total_broken_links != 1 else ''} across {len(all_files)} file{'s' if len(all_files) != 1 else ''}.")


if __name__ == "__main__":
    main()
