import argparse
import os
import re
import requests
import sys
from typing import List, Dict, Tuple

# Regex to find HTTP/HTTPS links in Markdown.
# It looks for [text](url) or just plain http(s)://url
LINK_REGEX = re.compile(r'\[.*?\]\((https?://[^\s)]+)\)|(https?://[^\s)]+)')

def find_markdown_files(directory: str) -> List[str]:
    """Recursively finds all Markdown files in the given directory."""
    md_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def extract_links_from_markdown(filepath: str) -> List[str]:
    """Extracts all HTTP/HTTPS links from a Markdown file."""
    links = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            for match in LINK_REGEX.finditer(content):
                # Group 1 is for [text](url), Group 2 is for plain url
                link = match.group(1) or match.group(2)
                if link:
                    links.append(link)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return list(set(links)) # Return unique links

def check_link_status(url: str) -> Tuple[int, str]:
    """Checks the HTTP status of a given URL."""
    try:
        # Use HEAD request first for efficiency. requests.head does not follow redirects by default.
        response = requests.head(url, timeout=5)
        
        # If HEAD returns a redirect, follow it with GET to ensure final destination is OK
        if 300 <= response.status_code < 400:
            response = requests.get(url, timeout=5)
        
        return response.status_code, response.reason
    except requests.exceptions.RequestException as e:
        # Catch all requests-related exceptions (connection error, timeout, etc.)
        return 0, str(e) # Use 0 for network errors

def main():
    parser = argparse.ArgumentParser(
        description="Scans Markdown files for broken external HTTP/HTTPS links."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="The directory to scan for Markdown files (default: current directory)."
    )
    args = parser.parse_args()

    scan_directory = args.path
    print(f"Scanning directory: {scan_directory}")

    md_files = find_markdown_files(scan_directory)
    print(f"Found {len(md_files)} Markdown files.")

    broken_links_report: Dict[str, List[Tuple[str, int, str]]] = {}
    total_broken_links = 0

    for md_file in md_files:
        links = extract_links_from_markdown(md_file)
        if not links:
            continue

        file_broken_links = []
        for link in links:
            status_code, reason = check_link_status(link)
            if status_code >= 400 or status_code == 0: # 0 for network errors
                file_broken_links.append((link, status_code, reason))
                total_broken_links += 1
        
        if file_broken_links:
            broken_links_report[md_file] = file_broken_links

    print("\n--- Broken Link Report ---\n")
    if not broken_links_report:
        print("No broken links found. All paths lead to glory!")
    else:
        for filepath, broken_links in broken_links_report.items():
            print(f"File: {filepath}")
            for link, status, reason in broken_links:
                status_str = f"{status} {reason}" if status != 0 else f"Network Error: {reason}"
                print(f"  - [Broken Link] {link} (Status: {status_str})")
            print() # Newline for readability

    print(f"--- Scan Complete ---")
    print(f"Total broken links found: {total_broken_links}")

    if total_broken_links > 0:
        sys.exit(1) # Indicate failure if broken links are found
    else:
        sys.exit(0) # Indicate success

if __name__ == "__main__":
    main()
