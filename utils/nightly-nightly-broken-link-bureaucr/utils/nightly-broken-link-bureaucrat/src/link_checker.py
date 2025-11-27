import os
import re
import requests
from urllib.parse import urlparse, urljoin

def find_markdown_files(root_dir):
    """Finds all markdown files in the given root directory and its subdirectories."""
    md_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.md'):
                md_files.append(os.path.join(dirpath, f))
    return md_files

def extract_links(markdown_content, base_path):
    """Extracts external and internal links from markdown content."""
    links = []
    # Regex for Markdown links: [text](url)
    # Also captures image links: ![alt](url)
    link_pattern = re.compile(r'\[.*?\]\((.*?)\)')
    
    for match in link_pattern.finditer(markdown_content):
        url = match.group(1).strip()
        if url:
            # Handle anchor links within the same file or other files
            if '#' in url:
                url_parts = url.split('#', 1)
                file_part = url_parts[0]
                # anchor_part = url_parts[1] # Not currently checked by this utility
                
                if file_part: # Link to another file with an anchor
                    links.append({'url': file_part, 'type': 'internal', 'base_path': base_path})
                # else: # Anchor within the same file, not checked for existence
            elif urlparse(url).scheme in ['http', 'https']:
                links.append({'url': url, 'type': 'external', 'base_path': base_path})
            elif not urlparse(url).scheme and not url.startswith('#'): # Relative path
                links.append({'url': url, 'type': 'internal', 'base_path': base_path})
    return links

def check_external_link(url):
    """Checks if an external URL is reachable."""
    try:
        # Use HEAD request for efficiency, as we only care about status
        response = requests.head(url, timeout=5, allow_redirects=True)
        return 200 <= response.status_code < 400 # Success or redirect
    except requests.exceptions.RequestException:
        return False

def check_internal_link(relative_path, base_file_path, root_dir):
    """Checks if an internal relative path points to an existing file."""
    # Construct the absolute path based on the base_file_path
    # base_file_path is the full path to the markdown file containing the link
    # relative_path is the link itself (e.g., ../foo/bar.md)
    
    # Get the directory of the base_file_path
    base_dir = os.path.dirname(base_file_path)
    
    # Join the base directory with the relative path
    absolute_path = os.path.normpath(os.path.join(base_dir, relative_path))
    
    # Ensure the resolved path is still within the root_dir to prevent directory traversal issues
    # Normalize root_dir for consistent comparison
    normalized_root_dir = os.path.normpath(root_dir)
    if not absolute_path.startswith(normalized_root_dir):
        return False # Link tries to go outside the repository root
    
    return os.path.exists(absolute_path)

def main():
    root_dir = os.getcwd() # Assume script is run from repo root
    markdown_files = find_markdown_files(root_dir)
    
    broken_links = []

    if not markdown_files:
        print("No Markdown files found to check.")
        return

    print(f"Scanning {len(markdown_files)} Markdown files for broken links...")

    for md_file in markdown_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        links = extract_links(content, md_file)
        
        for link in links:
            if link['type'] == 'external':
                if not check_external_link(link['url']):
                    broken_links.append({
                        'file': os.path.relpath(md_file, root_dir),
                        'link': link['url'],
                        'type': 'External',
                        'reason': 'Unreachable or invalid URL'
                    })
            elif link['type'] == 'internal':
                if not check_internal_link(link['url'], md_file, root_dir):
                    broken_links.append({
                        'file': os.path.relpath(md_file, root_dir),
                        'link': link['url'],
                        'type': 'Internal',
                        'reason': 'File does not exist'
                    })
    
    if broken_links:
        print("\n--- Broken Link Report ---")
        for bl in broken_links:
            print(f"File: {bl['file']}")
            print(f"  Link: {bl['link']}")
            print(f"  Type: {bl['type']}")
            print(f"  Reason: {bl['reason']}")
            print("-" * 20)
    else:
        print("\nAll links checked and found to be in perfect working order! Good job, Bureaucrat.")

if __name__ == "__main__":
    main()
