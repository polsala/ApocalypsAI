import os
import re
import argparse
import requests
from urllib.parse import urlparse
import fnmatch

# Regex to find markdown links: [text](url)
LINK_REGEX = re.compile(r'\[.*?\]\((.*?)\)')

def find_markdown_files(root_dir, ignore_patterns):
    """Finds all markdown files in the given root directory, respecting ignore patterns."""
    markdown_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter out ignored directories in place
        dirnames[:] = [d for d in dirnames if not any(fnmatch.fnmatch(os.path.join(dirpath, d), p) for p in ignore_patterns)]

        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if filename.endswith(('.md', '.markdown')) and not any(fnmatch.fnmatch(full_path, p) for p in ignore_patterns):
                markdown_files.append(full_path)
    return markdown_files

def extract_links(markdown_content):
    """Extracts all URLs from markdown content."""
    return LINK_REGEX.findall(markdown_content)

def is_external_link(url):
    """Checks if a URL is an external HTTP/HTTPS link."""
    parsed_url = urlparse(url)
    return parsed_url.scheme in ['http', 'https']

def check_local_link(scan_root_dir, current_file_path, link_path):
    """Checks if a local file path exists relative to the current_file_path,
    and ensures it stays within the scan_root_dir."""
    # Resolve relative paths
    resolved_path = os.path.normpath(os.path.join(os.path.dirname(current_file_path), link_path))

    # Ensure the resolved path is within the scan_root_dir
    if not resolved_path.startswith(scan_root_dir):
        return False, "Link path attempts to escape scan root"

    if os.path.exists(resolved_path):
        return True, "OK"
    return False, "File not found"

def check_external_link(url, timeout=5):
    """Checks if an external URL is reachable."""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return True, "OK"
    except requests.exceptions.HTTPError as e:
        return False, f"HTTP Error: {e.response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection Error"
    except requests.exceptions.Timeout:
        return False, "Timeout Error"
    except requests.exceptions.RequestException as e:
        return False, f"Request Error: {e}"

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Temporal Rift Repair Kit: Scans markdown files for broken links."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="The root directory to scan for markdown files."
    )
    parser.add_argument(
        "--ignore-patterns",
        nargs='*',
        default=[],
        help="Space-separated list of glob patterns for files/directories to ignore (e.g., 'node_modules/*', '*.bak')."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Timeout for external link checks in seconds (default: 5)."
    )
    args = parser.parse_args()

    root_dir = os.path.abspath(args.path)
    if not os.path.isdir(root_dir):
        print(f"Error: Directory '{root_dir}' not found.")
        exit(1)

    print(f"Scanning directory: {root_dir}\n")

    markdown_files = find_markdown_files(root_dir, args.ignore_patterns)
    broken_links_count = 0

    for md_file in markdown_files:
        print(f"--- Checking file: {md_file} ---")
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"  [ERROR] Could not read file: {md_file} - {e}")
            continue

        links = extract_links(content)
        for link in links:
            if is_external_link(link):
                status, reason = check_external_link(link, args.timeout)
                status_str = "[OK]" if status else "[BROKEN]"
                print(f"  {status_str} External link: {link} ({reason})")
                if not status:
                    broken_links_count += 1
            else:
                # Treat as internal link
                status, reason = check_local_link(root_dir, md_file, link)
                status_str = "[OK]" if status else "[BROKEN]"
                print(f"  {status_str} Internal link: {link} ({reason})")
                if not status:
                    broken_links_count += 1
        print() # Newline for readability between files

    print(f"Scan complete. Found {broken_links_count} broken links in {len(markdown_files)} files.")
    if broken_links_count > 0:
        exit(1) # Indicate failure if broken links are found
    else:
        exit(0) # Indicate success

if __name__ == "__main__":
    main()
