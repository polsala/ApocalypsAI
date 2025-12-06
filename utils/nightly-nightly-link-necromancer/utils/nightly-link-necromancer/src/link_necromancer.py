import re
import argparse
import requests
from typing import List, Tuple, Optional

# Regex to find Markdown links: [text](url)
MARKDOWN_LINK_REGEX = re.compile(r'\[.*?\]\((https?://[^\s)]+)\)')

def extract_links_from_markdown(content: str) -> List[str]:
    """
    Extracts all HTTP/HTTPS URLs from Markdown link syntax.
    """
    return MARKDOWN_LINK_REGEX.findall(content)

def check_url_status(url: str, timeout: float = 5.0) -> Tuple[bool, Optional[int], Optional[str]]:
    """
    Checks the status of a given URL.
    Returns (is_alive, status_code, error_message).
    """
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if response.status_code >= 400:
            return False, response.status_code, None
        return True, response.status_code, None
    except requests.exceptions.RequestException as e:
        return False, None, str(e)

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Link Necromancer: Scans Markdown files for dead external links."
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        type=str,
        nargs="+",
        help="One or more Markdown files to scan for links."
    )
    args = parser.parse_args()

    all_dead_links_found = False

    for file_path in args.files:
        print(f"Scanning {file_path}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"  ❌ Error: File not found: {file_path}")
            continue
        except Exception as e:
            print(f"  ❌ Error reading {file_path}: {e}")
            continue

        links = extract_links_from_markdown(content)
        if not links:
            print("  ℹ️ No external links found.")
            continue

        file_has_dead_links = False
        for link in links:
            is_alive, status_code, error_message = check_url_status(link)
            if not is_alive:
                all_dead_links_found = True
                file_has_dead_links = True
                if status_code:
                    print(f"  💀 Dead link found: {link} (Status: {status_code})")
                else:
                    print(f"  💀 Dead link found: {link} (Error: {error_message})")
        
        if not file_has_dead_links:
            print("  ✅ All links alive.")

    if not all_dead_links_found:
        print("\nNo dead links found across all scanned files. The documentation lives!")
    else:
        print("\nSome dead links were found. Time for some necromancy!")

if __name__ == "__main__":
    main()
