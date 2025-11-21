import os
import re
import requests
import argparse
from typing import List, Dict, Tuple

# Regex to find markdown links: [text](url) or <url>
# Group 1 captures the URL from [text](url)
# Group 2 captures the URL from <url>
LINK_REGEX = re.compile(r'\[.*?\]\((.*?)\)|<(\S+?)>')

def find_markdown_files(root_dir: str) -> List[str]:
    """Recursively finds all markdown files (.md) in the given directory."""
    markdown_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.md'):
                markdown_files.append(os.path.join(dirpath, f))
    return markdown_files

def extract_links(filepath: str) -> List[Tuple[int, str]]:
    """Extracts all links from a markdown file, returning (line_num, url) tuples."""
    links = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                for match in LINK_REGEX.finditer(line):
                    url = match.group(1) or match.group(2)
                    if url:
                        links.append((i, url))
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return links

def check_external_link(url: str) -> bool:
    """Checks if an external URL is reachable using a HEAD request."""
    # Mock rationale: In tests, we don't want to make actual network requests.
    # We'll mock requests.head to return predefined responses.
    try:
        # Use a short timeout to avoid hanging
        response = requests.head(url, timeout=5, allow_redirects=True)
        return 200 <= response.status_code < 400
    except requests.exceptions.RequestException:
        return False

def check_internal_link(base_filepath: str, target_path: str) -> bool:
    """Checks if an internal link (file or anchor) exists."""
    # Mock rationale: In tests, we don't want to rely on the actual filesystem.
    # We'll mock os.path.exists and os.path.join to simulate file existence.

    # Handle anchor links within the same file (e.g., #section)
    if target_path.startswith('#'):
        # For simplicity, we assume if the file exists, the anchor might exist.
        # A more robust check would parse the markdown for headers.
        # For this utility, we'll consider intra-file anchors valid if the file itself exists.
        return True

    # Remove anchor part from path if present (e.g., path/to/file.md#section -> path/to/file.md)
    target_path_no_anchor = target_path.split('#')[0]

    # Resolve relative path
    base_dir = os.path.dirname(base_filepath)
    full_target_path = os.path.normpath(os.path.join(base_dir, target_path_no_anchor))

    # Check if the file or directory exists
    return os.path.exists(full_target_path)

def is_external_url(url: str) -> bool:
    """Determines if a URL is external (starts with http/https)."""
    return url.startswith('http://') or url.startswith('https://')

def main():
    parser = argparse.ArgumentParser(
        description="Scans markdown files for broken external and internal links."
    )
    parser.add_argument(
        '--repo',
        type=str,
        default='.',
        help='The root directory of the repository to scan (e.g., "." for current dir).'
    )
    args = parser.parse_args()

    root_dir = args.repo
    if not os.path.isdir(root_dir):
        print(f"Error: Repository directory '{root_dir}' not found.")
        exit(1)

    print(f"Scanning '{os.path.abspath(root_dir)}' for broken links...")
    markdown_files = find_markdown_files(root_dir)
    broken_links_found = False

    for md_file in markdown_files:
        links = extract_links(md_file)
        for line_num, url in links:
            is_broken = False
            if is_external_url(url):
                if not check_external_link(url):
                    is_broken = True
                    print(f"🚨 BROKEN EXTERNAL LINK: {md_file}:{line_num} -> {url}")
            else:
                # Assume internal if not external. Could be relative path or absolute path within repo.
                if not check_internal_link(md_file, url):
                    is_broken = True
                    print(f"🚨 BROKEN INTERNAL LINK: {md_file}:{line_num} -> {url}")
            
            if is_broken:
                broken_links_found = True

    if not broken_links_found:
        print("\n✨ All links appear to be in order. The digital garden is well-tended.")
    else:
        print("\n⚠️ Some broken links were found. Time to get scavenging!")
        exit(1) # Exit with error code if broken links are found

if __name__ == '__main__':
    main()
