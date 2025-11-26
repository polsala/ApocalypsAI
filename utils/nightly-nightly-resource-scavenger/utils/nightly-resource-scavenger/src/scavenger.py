import os
import re
import argparse
import requests
from typing import List, Dict, Tuple

def find_links_in_file(filepath: str) -> List[str]:
    """
    Extracts HTTP/HTTPS links from a given file.
    """
    links = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Regex to find http(s):// links
            # This regex is basic and might miss some edge cases, but covers most common URLs.
            # It looks for http or https, followed by ://, then non-whitespace characters.
            # It tries to be non-greedy and stops at common delimiters like space, newline, or closing parenthesis.
            url_pattern = re.compile(r'https?://[^\s)"\'\\]+?')
            links.extend(url_pattern.findall(content))
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return links

def check_link(url: str, timeout: int = 5) -> Tuple[str, int, str]:
    """
    Checks a single URL for its status.
    Returns (url, status_code, error_message).
    """
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        # Use HEAD request for efficiency, but allow redirects to get final status
        # If HEAD is not allowed or returns a client/server error, fall back to GET
        if response.status_code >= 400 and response.request.method == 'HEAD':
            response = requests.get(url, timeout=timeout, allow_redirects=True)
        return url, response.status_code, ""
    except requests.exceptions.ConnectionError:
        return url, 0, "Connection Error"
    except requests.exceptions.Timeout:
        return url, 0, "Timeout"
    except requests.exceptions.RequestException as e:
        return url, 0, f"Request Error: {e}"
    except Exception as e:
        return url, 0, f"Unexpected Error: {e}"

def scavenge_directory(
    directory: str,
    file_extensions: List[str],
    timeout: int = 5,
    ignore_patterns: List[str] = None
) -> Dict[str, List[Tuple[str, int, str]]]:
    """
    Scans a directory for files, extracts links, and checks their status.
    Returns a dictionary where keys are file paths and values are lists of
    (url, status_code, error_message) tuples for broken links.
    """
    broken_links_by_file: Dict[str, List[Tuple[str, int, str]]] = {}
    compiled_ignore_patterns = [re.compile(p) for p in (ignore_patterns or [])]

    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(f".{ext}") for ext in file_extensions):
                filepath = os.path.join(root, file)
                print(f"Scanning {filepath}...")
                links = find_links_in_file(filepath)
                
                file_broken_links = []
                for link in links:
                    should_ignore = False
                    for pattern in compiled_ignore_patterns:
                        if pattern.search(link):
                            should_ignore = True
                            break
                    
                    if should_ignore:
                        print(f"  Ignoring link: {link}")
                        continue

                    _, status, error = check_link(link, timeout)
                    if not (200 <= status < 300):
                        file_broken_links.append((link, status, error))
                        print(f"  Broken link found: {link} (Status: {status}, Error: {error})")
                    else:
                        print(f"  Link OK: {link}")
                
                if file_broken_links:
                    broken_links_by_file[filepath] = file_broken_links
    
    return broken_links_by_file

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Resource Scavenger: Checks for broken links in specified files."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="The root directory to start scanning from. Defaults to current directory."
    )
    parser.add_argument(
        "--extensions",
        nargs='+',
        default=["md"],
        help="A space-separated list of file extensions to check (e.g., md txt). Defaults to md."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Connection timeout for HTTP requests in seconds. Defaults to 5."
    )
    parser.add_argument(
        "--ignore-patterns",
        nargs='*', # 0 or more arguments
        default=[],
        help="A space-separated list of regex patterns for URLs to ignore."
    )

    args = parser.parse_args()

    print(f"Starting Nightly Resource Scavenger in '{args.path}' for extensions {args.extensions}...")
    
    broken_links = scavenge_directory(
        args.path,
        args.extensions,
        args.timeout,
        args.ignore_patterns
    )

    if broken_links:
        print("\n--- Broken Links Report ---")
        for filepath, links in broken_links.items():
            print(f"\nFile: {filepath}")
            for link, status, error in links:
                print(f"  - URL: {link}")
                print(f"    Status: {status if status != 0 else 'Error'}")
                if error:
                    print(f"    Details: {error}")
        print("\nScavenging complete. Broken links found.")
        exit(1) # Indicate failure if broken links are found
    else:
        print("\nScavenging complete. No broken links found. Repository is pristine!")
        exit(0) # Indicate success

if __name__ == "__main__":
    main()
