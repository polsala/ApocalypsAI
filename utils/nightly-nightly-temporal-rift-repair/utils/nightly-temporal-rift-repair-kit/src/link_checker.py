import os
import re
import requests
import json
import argparse
from urllib.parse import urlparse, urljoin

# Regex to find Markdown links: [text](url) or <url>
# Group 1: link text, Group 2: URL for [text](url), Group 3: URL for <url>
LINK_REGEX = re.compile(r'\[([^\]]+)\]\(([^)]+)\)|<(https?://[^>]+)>')

# Regex to find Markdown headings (potential anchors)
HEADING_REGEX = re.compile(r'^[ \t]*(#+)\s*(.*)')

def find_markdown_files(root_dir):
    """Finds all Markdown files in the given root directory."""
    md_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith(('.md', '.markdown')):
                md_files.append(os.path.join(dirpath, f))
    return md_files

def extract_links(filepath):
    """Extracts all links from a Markdown file."""
    links = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                for match in LINK_REGEX.finditer(line):
                    link_text = match.group(1) if match.group(1) else ''
                    url = match.group(2) if match.group(2) else match.group(3)
                    if url:
                        links.append({
                            'file': os.path.relpath(filepath),
                            'line': i + 1,
                            'link_text': link_text,
                            'url': url
                        })
    except IOError as e:
        print(f"Warning: Could not read file {filepath}: {e}", file=sys.stderr)
    return links

def check_external_link(url):
    """Checks if an external URL is reachable."""
    try:
        # Use HEAD request for efficiency, but fallback to GET if HEAD is not allowed
        response = requests.head(url, timeout=5, allow_redirects=True)
        if response.status_code >= 400 and response.status_code != 405: # 405 Method Not Allowed is a common HEAD issue
            # If HEAD failed with a client/server error (not just method not allowed), try GET
            response = requests.get(url, timeout=5, allow_redirects=True)
        elif response.status_code == 405: # If HEAD is 405, try GET
            response = requests.get(url, timeout=5, allow_redirects=True)

        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        return True, None
    except requests.exceptions.RequestException as e:
        return False, str(e)

def check_internal_link(base_filepath, target_url, all_md_files_absolute_paths):
    """Checks if an internal link (file or anchor) exists."""
    parsed_url = urlparse(target_url)
    target_path = parsed_url.path
    fragment = parsed_url.fragment

    # Resolve the target path relative to the base file's directory
    base_dir = os.path.dirname(base_filepath)
    resolved_path = os.path.normpath(os.path.join(base_dir, target_path))

    # Check if the file/directory exists
    if not os.path.exists(resolved_path):
        return False, f"Internal file not found: {resolved_path}"
    
    # If it's a directory, it's considered valid if it contains a common index file
    if os.path.isdir(resolved_path):
        if not any(os.path.exists(os.path.join(resolved_path, idx_file)) for idx_file in ['index.md', 'README.md']):
            return False, f"Internal link points to directory '{resolved_path}' without an index file (index.md or README.md)"

    # Check if the fragment (anchor) exists within the target file
    if fragment:
        try:
            with open(resolved_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Markdown heading IDs are typically lowercase, spaces replaced by hyphens
                expected_heading_id = fragment.lower().replace('_', '-').replace(' ', '-')
                
                # Check for explicit HTML anchors (id or name attributes)
                if f'id="{expected_heading_id}"' in content or f'name="{expected_heading_id}"' in content:
                    return True, None
                
                # Check for Markdown headings that would generate this ID
                for line in content.splitlines():
                    match = HEADING_REGEX.match(line)
                    if match:
                        heading_text = match.group(2).strip()
                        generated_id = heading_text.lower().replace(' ', '-')
                        if generated_id == expected_heading_id:
                            return True, None
                
                return False, f"Anchor '#{fragment}' not found in '{resolved_path}'"
        except IOError:
            return False, f"Could not read target file '{resolved_path}' for anchor check"

    return True, None

def main():
    parser = argparse.ArgumentParser(description="Scan Markdown files for broken links.")
    parser.add_argument('--path', default='.', help="Root directory to start scanning from.")
    args = parser.parse_args()

    root_dir = args.path
    broken_links = []
    all_md_files_absolute_paths = find_markdown_files(root_dir)

    for md_file in all_md_files_absolute_paths:
        links_in_file = extract_links(md_file)
        for link_info in links_in_file:
            url = link_info['url']
            parsed_url = urlparse(url)

            if parsed_url.scheme in ['http', 'https']:
                # External link
                is_valid, reason = check_external_link(url)
                if not is_valid:
                    link_info['reason'] = f"External link failed: {reason}"
                    broken_links.append(link_info)
            elif not parsed_url.scheme and not parsed_url.netloc:
                # Internal link (relative path or anchor)
                is_valid, reason = check_internal_link(md_file, url, all_md_files_absolute_paths)
                if not is_valid:
                    link_info['reason'] = reason
                    broken_links.append(link_info)
            # else: mailto, tel, etc. - ignore for now as they are not 'broken' in the same sense

    print(json.dumps(broken_links, indent=2))

    if broken_links:
        exit(1) # Indicate failure if broken links are found
    else:
        exit(0) # Indicate success

if __name__ == '__main__':
    import sys
    main()
