import os
import re
import argparse
import requests
from typing import List, Tuple

# Regex to find Markdown links: [text](url)
LINK_REGEX = re.compile(r'\[([^\]]+)\]\((https?://[^)]+\.[a-zA-Z0-9/\-_.~%&?#=:]+)\)')

def find_markdown_files(root_dir: str) -> List[str]:
    """Recursively finds all Markdown files in the given directory."""
    md_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.md'):
                md_files.append(os.path.join(dirpath, f))
    return md_files

def extract_links_from_markdown(filepath: str) -> List[Tuple[str, str, int]]:
    """Extracts all external links from a Markdown file, returning (text, url, line_num)."""
    links = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                for match in LINK_REGEX.finditer(line):
                    link_text, url = match.groups()
                    links.append((link_text, url, i))
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return links

def check_link(url: str) -> int:
    """Checks a single URL using an HTTP HEAD request and returns its status code."""
    try:
        # Use HEAD request for efficiency, as we only need the status code
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code
    except requests.exceptions.RequestException:
        return 0 # Indicate a network/connection error

def main():
    parser = argparse.ArgumentParser(description="Scan Markdown files for broken external links.")
    parser.add_argument('--path', type=str, default='.',
                        help='The root directory to start scanning for Markdown files. Defaults to current directory.')
    args = parser.parse_args()

    root_dir = args.path
    print(f"\n🚀 Initiating Link Blaster scan in '{os.path.abspath(root_dir)}'...")

    markdown_files = find_markdown_files(root_dir)
    if not markdown_files:
        print("No Markdown files found to scan. All links are implicitly perfect! ✨")
        return

    all_extracted_links = []
    for md_file in markdown_files:
        all_extracted_links.extend([(md_file, text, url, line_num) for text, url, line_num in extract_links_from_markdown(md_file)])

    if not all_extracted_links:
        print("No external links found in Markdown files. Your documentation is a pristine, link-free paradise! 🏝️")
        return

    unique_urls = sorted(list(set(link[2] for link in all_extracted_links))) # Get unique URLs to avoid re-checking
    url_status_map = {}

    print(f"\nChecking {len(unique_urls)} unique external links...")
    for i, url in enumerate(unique_urls):
        print(f"  [{i+1}/{len(unique_urls)}] Checking: {url}", end='\r')
        status = check_link(url)
        url_status_map[url] = status
    print("\nLink checking complete. Analyzing results...\n")

    broken_links_found = False
    for md_file, link_text, url, line_num in all_extracted_links:
        status = url_status_map.get(url)
        if status is not None and (status < 200 or status >= 300) and status != 0: # 0 for network error
            if not broken_links_found:
                print("🚨 BROKEN LINKS DETECTED! 🚨\n")
                broken_links_found = True
            print(f"  File: {md_file} (Line: {line_num})")
            print(f"    Link Text: '{link_text}'")
            print(f"    URL: {url}")
            print(f"    Status: {status} (Non-2xx)\n")
        elif status == 0:
            if not broken_links_found:
                print("🚨 BROKEN LINKS DETECTED! 🚨\n")
                broken_links_found = True
            print(f"  File: {md_file} (Line: {line_num})")
            print(f"    Link Text: '{link_text}'")
            print(f"    URL: {url}")
            print(f"    Status: Network Error (Could not connect)\n")

    if not broken_links_found:
        print("✅ All external links are sparkling clean! No broken links found. Your docs are pristine! ✨")
    else:
        print("\nFix these broken links to restore your documentation's glory! 🛠️")

if __name__ == '__main__':
    main()
