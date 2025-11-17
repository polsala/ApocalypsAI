import os
import re
import requests
from urllib.parse import urlparse

# Regex to find Markdown links: [text](url)
LINK_REGEX = re.compile(r'\[[^\]]+\]\(([^)]*)\)')

def find_markdown_files(root_dir):
    """Recursively finds all Markdown files (.md) in the given directory."""
    markdown_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.md'):
                markdown_files.append(os.path.join(dirpath, f))
    return markdown_files

def extract_links(filepath):
    """Extracts all Markdown links from a given file."""
    links = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            for match in LINK_REGEX.finditer(content):
                url = match.group(1)
                links.append(url)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return links

def check_external_link(url):
    """Checks if an external URL is reachable and returns its status."""
    try:
        # Use HEAD request for efficiency, as we only need status code
        response = requests.head(url, timeout=5, allow_redirects=True)
        # Consider 2xx and 3xx as successful
        if 200 <= response.status_code < 400:
            return True, response.status_code
        else:
            return False, response.status_code
    except requests.exceptions.RequestException as e:
        return False, str(e)

def check_internal_link(base_filepath, link_path):
    """Checks if an internal link (file or directory) exists relative to the base file."""
    # Handle anchor links within the same document or other documents
    if '#' in link_path:
        link_path = link_path.split('#')[0] # Ignore anchors for file existence check

    if not link_path: # Link was just an anchor, or empty after stripping anchor
        return True # Assume valid if it's just an anchor or empty

    base_dir = os.path.dirname(base_filepath)
    
    # If link_path starts with '/', assume it's relative to the current working directory (repo root)
    # Otherwise, it's relative to the base_dir of the Markdown file.
    if link_path.startswith('/'):
        target_path = os.path.join(os.getcwd(), link_path[1:]) # Remove leading slash
    else:
        target_path = os.path.join(base_dir, link_path)

    # Normalize path to handle '..' and '.'
    target_path = os.path.normpath(target_path)
    
    return os.path.exists(target_path)

def main():
    print("Scanning for broken links in the repository...")
    root_dir = os.getcwd() # Start scan from current directory
    markdown_files = find_markdown_files(root_dir)
    print(f"\nFound {len(markdown_files)} Markdown files.\n")

    broken_links_count = 0

    for md_file in markdown_files:
        print(f"--- File: {os.path.relpath(md_file, root_dir)} ---")
        links = extract_links(md_file)
        if not links:
            print("  No links found.")
            continue

        for link in links:
            parsed_url = urlparse(link)
            if parsed_url.scheme in ['http', 'https']:
                is_valid, status = check_external_link(link)
                if is_valid:
                    print(f"  ✅ Valid External: {link}")
                else:
                    print(f"  ❌ Broken External: {link} (Status: {status})")
                    broken_links_count += 1
            else:
                # Internal link (relative path, or absolute path within repo)
                is_valid = check_internal_link(md_file, link)
                if is_valid:
                    print(f"  ✅ Valid Internal: {link}")
                else:
                    print(f"  ❌ Broken Internal: {link} (File not found)")
                    broken_links_count += 1
        print()

    print(f"Scan complete. {broken_links_count} broken links found.")

if __name__ == '__main__':
    main()
