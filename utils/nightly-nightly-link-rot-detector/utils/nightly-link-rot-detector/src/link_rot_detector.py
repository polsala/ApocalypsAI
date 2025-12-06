import os
import re
import sys
import requests
from typing import List, Tuple, Dict

# Regex to find Markdown links: [text](url)
# It specifically targets http/https URLs.
LINK_REGEX = re.compile(r'\[.*?\]\((https?://[^\s)]+)\)')

def find_markdown_files(directory: str) -> List[str]:
    """Recursively finds all .md files in the given directory."""
    markdown_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def extract_links_from_markdown(filepath: str) -> List[str]:
    """Extracts external HTTP/HTTPS links from a Markdown file."""
    links = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            for match in LINK_REGEX.finditer(content):
                links.append(match.group(1))
    except Exception as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
    return list(set(links)) # Return unique links

def check_link_status(url: str) -> Tuple[bool, str]:
    """Checks the status of a given URL using a HEAD request."""
    try:
        # Use a short timeout to prevent hangs
        response = requests.head(url, timeout=5, allow_redirects=True)
        if 200 <= response.status_code < 300:
            return True, "OK"
        else:
            return False, f"{response.status_code} {response.reason}"
    except requests.exceptions.ConnectionError:
        return False, "Connection Error: Could not connect to host."
    except requests.exceptions.Timeout:
        return False, "Timeout Error: Request timed out."
    except requests.exceptions.RequestException as e:
        return False, f"Request Error: {e}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/link_rot_detector.py <path_to_directory>", file=sys.stderr)
        sys.exit(1)

    target_directory = sys.argv[1]
    if not os.path.isdir(target_directory):
        print(f"Error: Directory '{target_directory}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning directory: {target_directory}\n")

    markdown_files = find_markdown_files(target_directory)
    broken_links_found = 0
    report: Dict[str, List[Tuple[str, str]]] = {}

    for filepath in markdown_files:
        links = extract_links_from_markdown(filepath)
        file_broken_links = []
        for link in links:
            is_ok, status = check_link_status(link)
            if not is_ok:
                file_broken_links.append((link, status))
                broken_links_found += 1
        if file_broken_links:
            report[filepath] = file_broken_links

    if report:
        for filepath, links_data in report.items():
            print(f"File: {filepath}")
            for link, status in links_data:
                print(f"  - Broken Link: {link} (Status: {status})")
        print(f"\nSummary: Found {broken_links_found} broken links in {len(report)} files.")
        sys.exit(1) # Exit with 1 to indicate issues
    else:
        print("All external links checked. No link rot detected. The digital garden is thriving!")
        sys.exit(0)

if __name__ == "__main__":
    main()
