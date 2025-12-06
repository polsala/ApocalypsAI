import os
import re
import requests
import argparse
from urllib.parse import urlparse
from typing import List, Tuple, Dict

# Regex to find Markdown links: [text](url)
# It captures the URL part.
MARKDOWN_LINK_REGEX = re.compile(r'\[.*?\]\((https?://[^\s)]+)\)')

def find_links_in_markdown(markdown_content: str) -> List[str]:
    """
    Extracts all external HTTP/HTTPS links from a Markdown string.
    """
    return MARKDOWN_LINK_REGEX.findall(markdown_content)

def check_link(url: str, timeout: int = 5) -> Tuple[bool, str]:
    """
    Checks if a given URL is reachable and returns a success status and message.
    """
    try:
        # Use HEAD request first as it's lighter, but fall back to GET if HEAD is not allowed
        # Some servers don't support HEAD, or return 405 Method Not Allowed
        try:
            response = requests.head(url, timeout=timeout, allow_redirects=True)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            return True, f"{response.status_code} OK"
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 405: # Method Not Allowed, try GET
                response = requests.get(url, timeout=timeout, allow_redirects=True)
                response.raise_for_status()
                return True, f"{response.status_code} OK"
            else:
                return False, f"{e.response.status_code} {e.response.reason}"
        except requests.exceptions.RequestException as e:
            # Catch all other requests exceptions (connection error, timeout, etc.)
            return False, f"Connection Error: {e}"

    except Exception as e:
        # Catch any other unexpected errors
        return False, f"Unexpected Error: {e}"

def process_markdown_file(filepath: str, timeout: int = 5) -> List[Dict[str, str]]:
    """
    Reads a Markdown file, finds links, checks them, and returns a list of broken links.
    """
    broken_links = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        links = find_links_in_markdown(content)
        
        for link in links:
            is_valid, status_message = check_link(link, timeout)
            if not is_valid:
                broken_links.append({
                    "file": filepath,
                    "link": link,
                    "status": status_message
                })
    except FileNotFoundError:
        print(f"[WARNING] File not found: {filepath}")
    except Exception as e:
        print(f"[ERROR] Could not process file {filepath}: {e}")
    
    return broken_links

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Link Looter: Scans Markdown files for broken external links."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="Path to a Markdown file or a directory to scan recursively."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Timeout in seconds for checking each link (default: 5)."
    )
    args = parser.parse_args()

    target_path = args.path
    timeout = args.timeout
    
    print(f"Scanning for broken links in: {target_path}")
    print("-" * 50)

    all_broken_links = []

    if os.path.isfile(target_path):
        if target_path.lower().endswith(('.md', '.markdown')):
            all_broken_links.extend(process_markdown_file(target_path, timeout))
        else:
            print(f"[WARNING] Skipping non-Markdown file: {target_path}")
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for file in files:
                if file.lower().endswith(('.md', '.markdown')):
                    filepath = os.path.join(root, file)
                    all_broken_links.extend(process_markdown_file(filepath, timeout))
    else:
        print(f"[ERROR] Path does not exist: {target_path}")
        exit(1)

    print("-" * 50)
    if all_broken_links:
        for bl in all_broken_links:
            print(f"[ERROR] Broken link found in {bl['file']}:")
            print(f"    Link: {bl['link']} (Status: {bl['status']})")
        print(f"\nScan complete. Found {len(all_broken_links)} broken links.")
        exit(1) # Exit with error code if broken links are found
    else:
        print("Scan complete. No broken links found. All clear!")
        exit(0) # Exit with success code

if __name__ == "__main__":
    main()
