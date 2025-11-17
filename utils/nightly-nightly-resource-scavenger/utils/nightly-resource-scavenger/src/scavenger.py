import argparse
import os
import re
import requests
from pathlib import Path
from typing import List, Tuple, Dict

# Regex to find markdown links: [text](url) or <url>
# Group 1 captures from [text](url), Group 2 captures from <url>
LINK_REGEX = re.compile(r'\[.*?\]\((.*?)\)|<(https?://.*?)>')

def find_markdown_files(root_dir: Path) -> List[Path]:
    """Recursively finds all markdown files in the given directory."""
    return list(root_dir.rglob('*.md'))

def extract_links(file_content: str) -> List[Tuple[str, int]]:
    """Extracts all links from markdown content, along with their line numbers."""
    links = []
    for i, line in enumerate(file_content.splitlines()):
        for match in LINK_REGEX.finditer(line):
            url = match.group(1) or match.group(2) # Group 1 for [text](url), Group 2 for <url>
            if url:
                links.append((url, i + 1))
    return links

def check_external_link(url: str) -> bool:
    """Checks if an external URL is reachable."""
    try:
        # Use HEAD request for efficiency, only checking headers
        response = requests.head(url, timeout=5, allow_redirects=True)
        return 200 <= response.status_code < 400
    except requests.exceptions.RequestException:
        return False

def check_internal_link(base_path: Path, link_path: str) -> bool:
    """Checks if an internal file path exists relative to the base_path."""
    # Remove anchor part if present (e.g., 'file.md#section' -> 'file.md')
    link_path_no_anchor = link_path.split('#')[0]

    if not link_path_no_anchor: # Link is just an anchor (e.g., '#section')
        # For simplicity, pure anchor links are considered valid if the file itself exists.
        # A more complex check would parse the target file for the anchor.
        return True

    # Resolve the target path relative to the directory of the base_path (the current markdown file)
    target_path = (base_path.parent / link_path_no_anchor).resolve()

    # Check if the target path exists on the filesystem
    return target_path.exists()

def main():
    parser = argparse.ArgumentParser(description="Scavenge markdown files for broken links.")
    parser.add_argument('--path', type=str, default='.',
                        help='The root directory to start scanning from.')
    args = parser.parse_args()

    root_dir = Path(args.path)
    if not root_dir.is_dir():
        print(f"Error: '{root_dir}' is not a valid directory.")
        exit(1)

    print(f"Scanning directory: {root_dir}")
    markdown_files = find_markdown_files(root_dir)
    broken_links: List[Dict[str, str]] = []

    for md_file in markdown_files:
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Warning: Could not read file {md_file}: {e}")
            continue

        links = extract_links(content)

        for link_url, line_num in links:
            if link_url.startswith(('http://', 'https://')):
                if not check_external_link(link_url):
                    broken_links.append({
                        'file': str(md_file.relative_to(root_dir)),
                        'line': line_num,
                        'type': 'External',
                        'link': link_url,
                        'reason': 'Unreachable'
                    })
            elif not link_url.startswith('#'): # Ignore pure anchor links for now, handled in check_internal_link
                if not check_internal_link(md_file, link_url):
                    broken_links.append({
                        'file': str(md_file.relative_to(root_dir)),
                        'line': line_num,
                        'type': 'Internal',
                        'link': link_url,
                        'reason': 'File not found'
                    })

    if broken_links:
        print("\nBroken Links Found:")
        print("--------------------")
        for bl in broken_links:
            print(f"File: {bl['file']}, Line: {bl['line']} - {bl['type']}: {bl['link']} (Status: {bl['reason']})")
        print("--------------------")
        print(f"Scan complete. {len(broken_links)} broken links found.")
        exit(1) # Exit with non-zero for CI/CD to detect issues
    else:
        print("\nScan complete. No broken links found. All clear!")
        exit(0)

if __name__ == '__main__':
    main()
