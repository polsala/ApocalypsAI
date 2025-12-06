import re
import argparse
import requests
from typing import List, Tuple, Dict
import sys

# Regex to find URLs. This is a simplified version and might not catch all edge cases,
# but covers common HTTP/HTTPS links in text and Markdown.
URL_REGEX = re.compile(r'https?://[\w./#?=&%~-]+')

def extract_urls(content: str) -> List[str]:
    """Extracts unique URLs from a given string content."""
    return sorted(list(set(URL_REGEX.findall(content))))

def check_url(url: str, timeout: float = 5.0) -> Tuple[bool, int]:
    """Checks if a URL is reachable and returns its status code.
    Uses HEAD request for efficiency, falls back to GET if HEAD is not allowed.
    """
    try:
        # Try HEAD request first
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if response.status_code >= 400 and response.status_code not in [405, 501]:
            # If HEAD fails with a client/server error, it's likely broken
            return False, response.status_code
        elif response.status_code in [405, 501]: # Method Not Allowed, Not Implemented
            # Fallback to GET if HEAD is not supported
            response = requests.get(url, timeout=timeout, allow_redirects=True, stream=True)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            return True, response.status_code
        else:
            return True, response.status_code
    except requests.exceptions.HTTPError as e:
        return False, e.response.status_code if e.response is not None else 0
    except requests.exceptions.ConnectionError:
        return False, 0 # Connection error (e.g., DNS failure, refused connection)
    except requests.exceptions.Timeout:
        return False, 0 # Request timed out
    except requests.exceptions.RequestException:
        return False, 0 # Other requests-related errors
    except Exception:
        return False, 0 # Catch any other unexpected errors

def scan_files(file_paths: List[str], timeout: float = 5.0) -> Dict[str, List[Tuple[str, int]]]:
    """Scans multiple files for broken links and returns a dictionary of results.
    Returns: { 'file_path': [('broken_url', status_code), ...] }
    """
    broken_links_by_file: Dict[str, List[Tuple[str, int]]] = {}

    for file_path in file_paths:
        print(f"Scanning {file_path}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            urls = extract_urls(content)
            file_broken_links: List[Tuple[str, int]] = []

            for url in urls:
                is_reachable, status_code = check_url(url, timeout)
                if not is_reachable:
                    file_broken_links.append((url, status_code))
                    print(f"  [BROKEN] {url} (Status: {status_code})")
                else:
                    print(f"  [OK] {url} (Status: {status_code})")

            if file_broken_links:
                broken_links_by_file[file_path] = file_broken_links

        except FileNotFoundError:
            print(f"Error: File not found: {file_path}", file=sys.stderr)
        except Exception as e:
            print(f"Error processing {file_path}: {e}", file=sys.stderr)

    return broken_links_by_file

def main():
    parser = argparse.ArgumentParser(
        description="Echoes of the Void - Dead Link Detector: Scans files for broken URLs."
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs='+',
        help="One or more files to scan for URLs."
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Timeout in seconds for each URL request (default: 5.0)."
    )

    args = parser.parse_args()

    print("\n--- Echoes of the Void - Dead Link Detector ---")
    results = scan_files(args.files, args.timeout)

    if results:
        print("\n--- Summary of Broken Links ---")
        for file_path, broken_links in results.items():
            print(f"File: {file_path}")
            for url, status_code in broken_links:
                print(f"  - {url} (Status: {status_code})")
        print("\nDetected broken links. Please investigate.")
        sys.exit(1) # Exit with error code if broken links are found
    else:
        print("\nAll links checked appear to be functional. The void is quiet... for now.")
        sys.exit(0)

if __name__ == "__main__":
    main()
