import argparse
import os
import re
import requests
import sys
from typing import List, Dict, Tuple

# Regex to find common HTTP/HTTPS URLs. This is a simplified version
# and primarily looks for standalone links, not necessarily embedded in HTML tags or Markdown syntax.
URL_REGEX = re.compile(r'https?://[\w./\-#?=&%~_@:;]+')

def check_link(url: str, timeout: int = 5) -> Tuple[bool, str]:
    """
    Checks if a given URL is accessible.
    Returns (True, 'OK') for success, or (False, error_message) for failure.
    """
    try:
        # Use HEAD request for efficiency, fall back to GET if HEAD is not allowed/supported
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if response.status_code >= 400:
            # Some servers might block HEAD requests (e.g., 405 Method Not Allowed, 403 Forbidden)
            # or return a generic 4xx/5xx for HEAD but a more specific one for GET.
            # Try GET as a fallback for these cases.
            if response.status_code in [405, 403] or (response.status_code >= 400 and response.status_code < 500):
                response = requests.get(url, timeout=timeout, allow_redirects=True)
                if response.status_code >= 400:
                    return False, f"HTTP {response.status_code} (after GET fallback)"
            else:
                return False, f"HTTP {response.status_code}"
        return True, 'OK'
    except requests.exceptions.ConnectionError:
        return False, "Connection Error"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except requests.exceptions.RequestException as e:
        return False, f"Request Error: {e}"
    except Exception as e:
        return False, f"Unexpected Error: {e}"

def find_links_in_file(filepath: str) -> List[str]:
    """
    Reads a file and extracts all unique URLs.
    """
    links = set()
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for match in URL_REGEX.finditer(content):
                links.add(match.group(0))
    except IOError as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
    return list(links)

def scan_directory_for_broken_links(root_dir: str, file_types: List[str], timeout: int) -> Dict[str, List[Tuple[str, str]]]:
    """
    Scans a directory for files of specified types, extracts links, and checks their accessibility.
    Returns a dictionary mapping file paths to a list of (broken_link, error_message) tuples.
    """
    broken_links_report: Dict[str, List[Tuple[str, str]]] = {}

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(filename.endswith(f'.{ext}') for ext in file_types):
                filepath = os.path.join(dirpath, filename)
                print(f"Scanning {filepath}...")
                links_in_file = find_links_in_file(filepath)
                
                for link in links_in_file:
                    is_ok, error_msg = check_link(link, timeout)
                    if not is_ok:
                        if filepath not in broken_links_report:
                            broken_links_report[filepath] = []
                        broken_links_report[filepath].append((link, error_msg))
                        print(f"  Broken link found: {link} ({error_msg})")

    return broken_links_report

def main():
    parser = argparse.ArgumentParser(
        description="Scan directories for broken HTTP/HTTPS links."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        required=True, 
        help='The root directory to start scanning from.'
    )
    parser.add_argument(
        '--file-types', 
        nargs='*', 
        default=['md', 'html', 'rst'], 
        help='Space-separated list of file extensions to scan (e.g., md html).'
    )
    parser.add_argument(
        '--timeout', 
        type=int, 
        default=5, 
        help='Timeout for each HTTP request in seconds.'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    print(f"Starting link scan in '{args.path}' for file types: {', '.join(args.file_types)}")
    report = scan_directory_for_broken_links(args.path, args.file_types, args.timeout)

    if report:
        print("\n--- Broken Link Report ---")
        for filepath, broken_links in report.items():
            print(f"File: {filepath}")
            for link, error_msg in broken_links:
                print(f"  - {link} ({error_msg})")
        sys.exit(1) # Exit with error code if broken links are found
    else:
        print("\nNo broken links found. All clear!")
        sys.exit(0)

if __name__ == '__main__':
    main()
