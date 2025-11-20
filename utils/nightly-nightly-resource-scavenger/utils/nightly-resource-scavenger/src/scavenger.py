import argparse
import os
import re
import requests
from typing import List, Tuple, Set

# Regex to find HTTP/HTTPS URLs
URL_REGEX = re.compile(r'https?://(?:www\.)?[a-zA-Z0-9./?#=\-_&%]+')

def find_urls_in_file(filepath: str) -> List[str]:
    """Extracts all HTTP/HTTPS URLs from a given file."""
    urls = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            urls.extend(URL_REGEX.findall(content))
    except Exception as e:
        print(f"Warning: Could not read file {filepath}: {e}")
    return list(set(urls)) # Return unique URLs from this file

def check_url(url: str, timeout: int = 5) -> Tuple[bool, str]:
    """Checks if a URL is reachable and returns its status."""
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        if 200 <= response.status_code < 300:
            return True, "OK"
        else:
            return False, f"Status: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Error: ConnectionError"
    except requests.exceptions.Timeout:
        return False, "Error: Timeout"
    except requests.exceptions.RequestException as e:
        return False, f"Error: {type(e).__name__}"

def main():
    parser = argparse.ArgumentParser(
        description="Scans a directory for HTTP/HTTPS links and reports broken ones."
    )
    parser.add_argument(
        "--path", 
        type=str, 
        required=True, 
        help="The root directory to start scanning for files and links."
    )
    parser.add_argument(
        "--file-extensions",
        type=str,
        default="md,txt,py,js,ts,json,yml,yaml,xml,html,css,sh",
        help="Comma-separated list of file extensions to scan."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Timeout for each HTTP request in seconds."
    )

    args = parser.parse_args()

    target_dir = args.path
    allowed_extensions = {f".{ext.strip().lower()}` for ext in args.file_extensions.split(',')}
    request_timeout = args.timeout

    if not os.path.isdir(target_dir):
        print(f"Error: Directory '{target_dir}' not found.")
        exit(1)

    print(f"Scanning directory: {target_dir}")
    all_urls_with_sources: List[Tuple[str, str]] = [] # (url, filepath)
    files_scanned_count = 0

    for root, _, files in os.walk(target_dir):
        for file in files:
            if os.path.splitext(file)[1].lower() in allowed_extensions:
                filepath = os.path.join(root, file)
                files_scanned_count += 1
                urls = find_urls_in_file(filepath)
                for url in urls:
                    all_urls_with_sources.append((url, filepath))
    
    print(f"Found {files_scanned_count} files to scan.")
    
    # Check unique URLs to avoid redundant requests, but keep track of all sources
    unique_urls_to_check: Set[str] = set(url for url, _ in all_urls_with_sources)
    print(f"Found {len(unique_urls_to_check)} unique URLs across all files.")

    url_status_cache = {}
    for url in unique_urls_to_check:
        is_ok, status_msg = check_url(url, request_timeout)
        url_status_cache[url] = (is_ok, status_msg)
        print(f"Checking URL: {url} ({status_msg})")

    broken_links_report: List[Tuple[str, str, str]] = [] # (url, filepath, status_message)
    for url, filepath in all_urls_with_sources:
        is_ok, status_msg = url_status_cache.get(url, (False, "Unknown Error"))
        if not is_ok:
            broken_links_report.append((url, filepath, status_msg))

    print("\n--- Broken Links Report ---")
    if not broken_links_report:
        print("No broken links found. All systems nominal!")
    else:
        for url, filepath, status_msg in broken_links_report:
            print(f"{url} (Source: {filepath}) (Status: {status_msg})")

    print(f"\nScan complete. Found {len(broken_links_report)} broken links.")
    if broken_links_report:
        exit(1) # Indicate failure if broken links are found
    else:
        exit(0)

if __name__ == "__main__":
    main()
