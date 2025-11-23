import argparse
import os
import re
import fnmatch
import requests
from typing import List, Tuple, Dict

# Regex to find Markdown links: [text](url)
MARKDOWN_LINK_REGEX = re.compile(r'\[.*?\]\((https?://[^\s)]+)\)')
# Regex to find raw URLs (simple, might catch false positives in code, but good for general text)
RAW_URL_REGEX = re.compile(r'(https?://(?:www\.)?[a-zA-Z0-9./\-]+(?:/[^\s]*)?)')

# File extensions to scan
SCAN_EXTENSIONS = ('.md', '.py', '.txt', '.yml', '.yaml', '.json')

def find_urls_in_file(filepath: str) -> List[Tuple[str, int, str]]:
    """Finds URLs in a given file and returns them with their line numbers."""
    urls_found = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                # Find Markdown links first
                md_matches = MARKDOWN_LINK_REGEX.findall(line)
                for url in md_matches:
                    urls_found.append((url, i + 1, filepath))
                
                # Find raw URLs, but avoid duplicates if already found by Markdown regex
                raw_matches = RAW_URL_REGEX.findall(line)
                for url in raw_matches:
                    if url not in [u[0] for u in md_matches]: # Avoid adding duplicates
                        urls_found.append((url, i + 1, filepath))
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return urls_found

def check_url(url: str) -> Tuple[bool, str]:
    """Checks if a URL is reachable and returns status."""
    try:
        # Use HEAD request for efficiency, fall back to GET if HEAD is not allowed
        response = requests.head(url, timeout=5, allow_redirects=True)
        if response.status_code >= 400 and response.status_code < 500: # Client errors
            # Some servers block HEAD, try GET if HEAD returns client error
            response = requests.get(url, timeout=5, allow_redirects=True)
        
        if 200 <= response.status_code < 400: # Success or redirect
            return True, f"{response.status_code} OK"
        else:
            return False, f"{response.status_code} {response.reason}"
    except requests.exceptions.ConnectionError:
        return False, "Connection Error"
    except requests.exceptions.Timeout:
        return False, "Timeout Error"
    except requests.exceptions.RequestException as e:
        return False, f"Request Error: {e}"
    except Exception as e:
        return False, f"Unexpected Error: {e}"

def main():
    parser = argparse.ArgumentParser(
        description="Scan files for external URLs and check their reachability."
    )
    parser.add_argument(
        '--path', 
        required=True, 
        help='The file or directory path to scan for URLs.'
    )
    parser.add_argument(
        '--exclude', 
        action='append', 
        default=[], 
        help='Glob-style pattern to exclude files or directories. Can be specified multiple times.'
    )

    args = parser.parse_args()

    files_to_scan: List[str] = []
    if os.path.isfile(args.path):
        files_to_scan.append(args.path)
    elif os.path.isdir(args.path):
        for root, dirs, files in os.walk(args.path):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(os.path.join(root, d), p) for p in args.exclude)]
            for file in files:
                filepath = os.path.join(root, file)
                if filepath.lower().endswith(SCAN_EXTENSIONS):
                    if not any(fnmatch.fnmatch(filepath, p) for p in args.exclude):
                        files_to_scan.append(filepath)
    else:
        print(f"Error: Path '{args.path}' does not exist or is not a file/directory.")
        return

    all_urls: Dict[str, List[Tuple[int, str]]] = {}
    for filepath in files_to_scan:
        print(f"Scanning: {filepath}")
        urls_in_file = find_urls_in_file(filepath)
        for url, line_num, _ in urls_in_file:
            if url not in all_urls:
                all_urls[url] = []
            all_urls[url].append((line_num, filepath))

    broken_links_count = 0
    checked_urls = set()

    for url, locations in all_urls.items():
        if url in checked_urls: # Avoid re-checking the same URL if it appears multiple times
            continue
        
        is_reachable, status = check_url(url)
        checked_urls.add(url)

        for line_num, filepath in locations:
            if is_reachable:
                print(f"  [OK] {url} (Found in {filepath}:{line_num})")
            else:
                print(f"  [BROKEN] {url} ({status}) (Found in {filepath}:{line_num})")
                broken_links_count += 1
    
    print(f"\nScan complete. Found {broken_links_count} broken links.")

if __name__ == '__main__':
    main()
