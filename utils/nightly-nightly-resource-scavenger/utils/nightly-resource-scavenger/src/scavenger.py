import os
import re
import requests
import argparse
import sys
from typing import List, Tuple, Dict

# Regex to find Markdown links: [text](url)
# Captures the URL part, ensuring it starts with http or https
LINK_REGEX = re.compile(r'\[.*?\]\((https?://[^\s)]+)\)')

def find_links(content: str) -> List[str]:
    """Extracts all http(s) links from a given string content."""
    return LINK_REGEX.findall(content)

def check_link(url: str) -> Tuple[bool, str]:
    """Checks if a given URL is accessible and returns its status.

    Returns: (is_ok, status_message)
    """
    try:
        # Use HEAD request for efficiency, fall back to GET if HEAD is not allowed
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code >= 400 and response.status_code < 500 and response.request.method == 'HEAD':
            # Some servers disallow HEAD for certain resources, try GET
            response = requests.get(url, allow_redirects=True, timeout=5)

        if 200 <= response.status_code < 300:
            return True, f"Status: {response.status_code} OK"
        else:
            return False, f"Status: {response.status_code} {response.reason}"
    except requests.exceptions.Timeout:
        return False, "Error: Connection timed out"
    except requests.exceptions.ConnectionError:
        return False, "Error: Connection failed"
    except requests.exceptions.RequestException as e:
        return False, f"Error: {e}"

def scan_directory(
    root_dir: str,
    file_extensions: List[str]
) -> Dict[str, List[Tuple[str, str]]]:
    """Scans a directory for Markdown files and checks their links.

    Returns: A dictionary where keys are file paths and values are lists of
             (broken_link_url, error_message) tuples.
    """
    broken_links_by_file: Dict[str, List[Tuple[str, str]]] = {}
    print(f"Scanning directory: {root_dir}")

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in file_extensions):
                filepath = os.path.join(dirpath, filename)
                print(f"Checking file: {filepath}")
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    links = find_links(content)
                    file_broken_links: List[Tuple[str, str]] = []
                    for link in links:
                        is_ok, status_message = check_link(link)
                        if not is_ok:
                            print(f"  [BROKEN] {link} ({status_message})")
                            file_broken_links.append((link, status_message))
                        else:
                            print(f"  [OK] {link}")
                    if file_broken_links:
                        broken_links_by_file[filepath] = file_broken_links
                except Exception as e:
                    print(f"  [ERROR] Could not process {filepath}: {e}")

    return broken_links_by_file

def main():
    parser = argparse.ArgumentParser(
        description="Scans Markdown files for broken external links."
    )
    parser.add_argument(
        "--root-dir",
        type=str,
        required=True,
        help="The root directory from which to start scanning for Markdown files."
    )
    parser.add_argument(
        "--file-extensions",
        nargs='*', # 0 or more arguments
        default=['.md', '.markdown'],
        help="A space-separated list of file extensions to scan (e.g., .md .markdown). Defaults to .md .markdown."
    )

    args = parser.parse_args()

    broken_links = scan_directory(args.root_dir, args.file_extensions)

    print("\n--- Scan Complete ---")
    total_broken = sum(len(links) for links in broken_links.values())
    if total_broken > 0:
        print(f"Found {total_broken} broken links across {len(broken_links)} files.")
        sys.exit(1) # Exit with non-zero for CI/CD failure
    else:
        print("No broken links found. All resources are accounted for!")
        sys.exit(0)

if __name__ == "__main__":
    main()
