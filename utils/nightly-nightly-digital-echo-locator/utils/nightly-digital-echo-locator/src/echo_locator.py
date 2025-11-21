import argparse
import os
import re
import requests
from typing import List, Tuple

# Regex to find URLs. This is a simplified version; real-world might need more robustness.
URL_REGEX = re.compile(r'https?://(?:www\.)?[a-zA-Z0-9./?#&_=-]+')

def find_urls_in_text(text: str) -> List[str]:
    """Finds all unique URLs in a given string of text."""
    return sorted(list(set(URL_REGEX.findall(text))))

def check_url(url: str, timeout: int = 5) -> Tuple[bool, int]:
    """Checks if a URL is reachable and returns its status code.
    Returns (True, status_code) for success (2xx), (False, status_code) otherwise.
    """
    try:
        # Use HEAD request for efficiency, fall back to GET if HEAD is not allowed
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if response.status_code >= 400 and response.status_code != 405: # 405 Method Not Allowed
            # If HEAD fails with a client error, try GET
            response = requests.get(url, timeout=timeout, allow_redirects=True)
        
        return 200 <= response.status_code < 300, response.status_code
    except requests.exceptions.RequestException as e:
        # Network error, timeout, DNS error, etc.
        if isinstance(e, requests.exceptions.Timeout):
            return False, 408 # Request Timeout
        elif isinstance(e, requests.exceptions.ConnectionError):
            return False, 503 # Service Unavailable (or similar network issue)
        else:
            return False, 0 # Unknown error

def scan_file(filepath: str, timeout: int = 5, verbose: bool = False) -> List[Tuple[str, int]]:
    """Scans a single file for URLs and checks their reachability.
    Returns a list of (broken_url, status_code) tuples.
    """
    broken_links = []
    if verbose:
        print(f"Scanning file: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        urls = find_urls_in_text(content)
        
        if not urls and verbose:
            print(f"  No URLs found in {filepath}")
            
        for url in urls:
            is_reachable, status_code = check_url(url, timeout)
            if not is_reachable:
                broken_links.append((url, status_code))
                if verbose:
                    print(f"  [BROKEN] {url} (Status: {status_code})")
            elif verbose:
                print(f"  [OK] {url} (Status: {status_code})")
    except Exception as e:
        if verbose:
            print(f"Error processing file {filepath}: {e}")
        # Consider logging the error but not failing the entire scan
    return broken_links

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Digital Echo Locator: Scans files for URLs and checks their reachability."
    )
    parser.add_argument(
        "--path", 
        required=True, 
        help="The file or directory to scan. If a directory, it will be scanned recursively."
    )
    parser.add_argument(
        "--extensions", 
        type=str, 
        default="", 
        help="Comma-separated list of file extensions to include (e.g., md,py,txt)."
    )
    parser.add_argument(
        "--timeout", 
        type=int, 
        default=5, 
        help="Maximum time in seconds to wait for a URL to respond. Default is 5."
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Print more detailed output during the scan."
    )

    args = parser.parse_args()

    target_extensions = {f".{ext.strip().lower()}" for ext in args.extensions.split(',') if ext.strip()}

    all_broken_links = []

    if os.path.isfile(args.path):
        if not target_extensions or os.path.splitext(args.path)[1].lower() in target_extensions:
            all_broken_links.extend(scan_file(args.path, args.timeout, args.verbose))
    elif os.path.isdir(args.path):
        if args.verbose:
            print(f"Scanning directory: {args.path}")
        for root, _, files in os.walk(args.path):
            for filename in files:
                if not target_extensions or os.path.splitext(filename)[1].lower() in target_extensions:
                    filepath = os.path.join(root, filename)
                    all_broken_links.extend(scan_file(filepath, args.timeout, args.verbose))
    else:
        print(f"Error: Path '{args.path}' does not exist or is not a valid file/directory.")
        exit(1)

    if all_broken_links:
        print("\n--- Broken Links Report ---")
        for url, status in all_broken_links:
            print(f"[BROKEN] {url} (Status: {status})")
        print(f"\nFound {len(all_broken_links)} broken links.")
        exit(1) # Exit with error code if broken links are found
    else:
        print("\nAll digital echoes are strong! No broken links found.")
        exit(0)

if __name__ == "__main__":
    main()
