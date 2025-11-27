import os
import re
import requests
from typing import List, Tuple, Dict

def find_markdown_files(root_dir: str) -> List[str]:
    """Recursively finds all Markdown files (.md) in a given directory."""
    markdown_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.md'):
                markdown_files.append(os.path.join(dirpath, f))
    return markdown_files

def extract_urls_from_markdown(file_path: str) -> List[str]:
    """Extracts HTTP/HTTPS URLs from a Markdown file."""
    urls = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Regex to find URLs in Markdown: [text](url) or just raw http(s)://
            # This regex is simplified and might not catch all edge cases, but covers common patterns.
            # It looks for (http(s)://...) or standalone http(s)://...
            url_pattern = re.compile(r'\((https?://[^)]+)\)|\b(https?://\S+)')
            for match in url_pattern.finditer(content):
                if match.group(1): # From [text](url) pattern
                    urls.append(match.group(1))
                elif match.group(2): # From raw http(s):// pattern
                    urls.append(match.group(2))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return list(set(urls)) # Return unique URLs

def check_url_reachability(url: str, timeout: int = 5) -> Tuple[bool, str]:
    """Checks if a URL is reachable and returns its status or error message."""
    try:
        # Use HEAD request for efficiency, as we only care about status, not content
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if 200 <= response.status_code < 400: # Success or redirection
            return True, f"Status: {response.status_code}"
        else:
            return False, f"Status: {response.status_code} - {response.reason}"
    except requests.exceptions.Timeout:
        return False, "Error: Timeout"
    except requests.exceptions.ConnectionError:
        return False, "Error: Connection refused or DNS error"
    except requests.exceptions.RequestException as e:
        return False, f"Error: {e}"

def main(root_dir: str):
    """Main function to orchestrate the link checking process."""
    print(f"Scanning directory: {root_dir}")
    markdown_files = find_markdown_files(root_dir)
    print(f"Found {len(markdown_files)} Markdown files.\n")

    broken_links_count = 0

    for md_file in markdown_files:
        print(f"Checking links in {os.path.relpath(md_file, root_dir)}:")
        urls = extract_urls_from_markdown(md_file)
        if not urls:
            print("  No external links found.")
            continue

        for url in urls:
            is_reachable, status_message = check_url_reachability(url)
            if is_reachable:
                print(f"  ✅ {url} ({status_message})")
            else:
                print(f"  ❌ {url} ({status_message})")
                broken_links_count += 1
        print()

    print(f"Scan complete. Found {broken_links_count} broken/unreachable links.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 src/link_checker.py <path_to_repository_root>")
        sys.exit(1)
    
    repo_root = sys.argv[1]
    if not os.path.isdir(repo_root):
        print(f"Error: Directory '{repo_root}' not found.")
        sys.exit(1)

    main(repo_root)
