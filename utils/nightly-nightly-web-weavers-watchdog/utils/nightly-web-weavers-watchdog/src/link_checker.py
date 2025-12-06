import argparse
import os
import re
import requests
from typing import List, Dict, Tuple, Set

# Whimsical ASCII art for the Watchdog
WATCHDOG_BANNER = """
  _   _   _   _   _   _   _   _   _   _   _   _   _   _   _
 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \
( W | e | b |   | W | e | a | v | e | r | ' | s |   | W | D )
 \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/

"""

def find_markdown_files(root_dir: str) -> List[str]:
    """Recursively finds all Markdown files (.md) in the given directory."""
    markdown_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.md'):
                markdown_files.append(os.path.join(dirpath, f))
    return markdown_files

def extract_links(markdown_content: str) -> Set[str]:
    """Extracts unique external HTTP/HTTPS links from Markdown content."""
    # Regex to find Markdown links: [text](url) or ![alt](url)
    # Also captures raw URLs that might not be in link format but are common
    link_pattern = re.compile(r'\[.*?\]\((https?://[^)]+)\)|(https?://\S+)')
    links = set()
    for match in link_pattern.finditer(markdown_content):
        url = match.group(1) or match.group(2)
        if url:
            # Basic cleanup: remove trailing punctuation if it's a raw URL
            url = url.strip('.,;"\'')
            links.add(url)
    return links

def check_link(url: str) -> Tuple[str, str]:
    """Checks a single URL for accessibility and returns its status.
    Returns (url, status_message).
    """
    try:
        # Use a short timeout to avoid hanging on unresponsive servers
        # stream=True and allow_redirects=True are good defaults for link checking
        response = requests.get(url, timeout=5, stream=True, allow_redirects=True)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return url, f"{response.status_code} OK"
    except requests.exceptions.HTTPError as e:
        return url, f"{e.response.status_code} {e.response.reason}"
    except requests.exceptions.ConnectionError:
        return url, "Connection Error"
    except requests.exceptions.Timeout:
        return url, "Timeout"
    except requests.exceptions.RequestException as e:
        return url, f"Request Error: {e}"
    except Exception as e:
        return url, f"Unexpected Error: {e}"

def main():
    parser = argparse.ArgumentParser(
        description="Web Weaver's Watchdog: Scans Markdown files for broken external links."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        default='.', 
        help='The root directory to start scanning for Markdown files.'
    )
    args = parser.parse_argument()

    root_dir = os.path.abspath(args.path)

    print(WATCHDOG_BANNER)
    print(f"Scanning directory: {root_dir}\n")

    markdown_files = find_markdown_files(root_dir)
    if not markdown_files:
        print("No Markdown files found. The web is calm, for now.")
        return

    print(f"Found {len(markdown_files)} Markdown files.")

    all_links: Dict[str, List[str]] = {}
    unique_external_links: Set[str] = set()

    for md_file in markdown_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            extracted_links = extract_links(content)
            for link in extracted_links:
                if link.startswith(('http://', 'https://')):
                    unique_external_links.add(link)
                    all_links.setdefault(link, []).append(os.path.relpath(md_file, root_dir))
        except Exception as e:
            print(f"Warning: Could not process {os.path.relpath(md_file, root_dir)}: {e}")

    if not unique_external_links:
        print("No external links found to check. The web is perfectly spun!")
        return

    print(f"Checking {len(unique_external_links)} unique external links...\n")

    broken_links_report: List[Tuple[str, str, List[str]]] = []

    for link in sorted(list(unique_external_links)):
        url, status = check_link(link)
        if not status.endswith("OK"):
            broken_links_report.append((url, status, all_links.get(url, [])))

    if broken_links_report:
        print("🚨 BROKEN LINKS DETECTED! 🚨\n")
        for url, status, files in broken_links_report:
            print(f"[{status}] {url}")
            for f in files:
                print(f"  - Found in: {f}")
        print("\nTime to re-weave some threads!\n")
        exit(1) # Indicate failure if broken links are found
    else:
        print("All links are holding strong! The web is perfectly intact!\n")

if __name__ == '__main__':
    main()
