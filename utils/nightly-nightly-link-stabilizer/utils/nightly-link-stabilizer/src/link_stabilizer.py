import os
import re
import argparse
import requests
from typing import List, Dict, Tuple

# Regex to find Markdown links: [text](url_or_path)
LINK_REGEX = re.compile(r'\[.*?\]\((.*?)\)')

def find_markdown_files(directory: str) -> List[str]:
    """Recursively finds all Markdown files (.md) in the given directory."""
    md_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def extract_links(filepath: str) -> Tuple[List[str], List[str]]:
    """Extracts external URLs and internal file paths from a Markdown file."""
    external_links = []
    internal_links = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            for match in LINK_REGEX.finditer(content):
                link_target = match.group(1)
                if link_target.startswith(('http://', 'https://')):
                    external_links.append(link_target)
                elif link_target and not link_target.startswith('#'): # Ignore anchor links
                    internal_links.append(link_target)
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
    return external_links, internal_links

def check_external_link(url: str) -> Tuple[bool, str]:
    """Checks if an external URL is reachable and returns a success status."""
    try:
        # Using a short timeout to avoid hanging on unresponsive servers
        response = requests.head(url, timeout=5, allow_redirects=True)
        if 200 <= response.status_code < 400:
            return True, f"Status: {response.status_code}"
        else:
            return False, f"Status: {response.status_code} {response.reason}"
    except requests.exceptions.ConnectionError:
        return False, "Connection Error"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except requests.exceptions.RequestException as e:
        return False, f"Request Error: {e}"

def check_internal_link(base_dir: str, current_file_path: str, relative_path: str) -> Tuple[bool, str]:
    """Checks if an internal file path exists relative to the current file."""
    # Resolve the absolute path of the target file
    if os.path.isabs(relative_path):
        # If the path is absolute, check it directly relative to the base_dir if it's within
        # For simplicity, we'll assume absolute paths are relative to the system root
        # or the base_dir if they start with a '/' but are not fully qualified URLs.
        # A more robust solution might need to define what absolute paths mean in context.
        # For now, if it's an absolute path, we'll check if it exists as is.
        target_path = relative_path
    else:
        # For relative paths, resolve them based on the current file's directory
        current_dir = os.path.dirname(current_file_path)
        target_path = os.path.normpath(os.path.join(current_dir, relative_path))

    # Ensure the target path is within the scanned base_dir to avoid checking arbitrary system paths
    # This check is important for security and scope.
    if not os.path.commonpath([os.path.abspath(base_dir), os.path.abspath(target_path)]) == os.path.abspath(base_dir):
        return False, f"Path '{relative_path}' points outside the scanned directory '{base_dir}'"

    if os.path.exists(target_path):
        return True, "File exists"
    else:
        return False, "File not found"

def main():
    parser = argparse.ArgumentParser(
        description="Scans Markdown files for broken external and internal links."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        required=True, 
        help='The root directory to start scanning for Markdown files.'
    )
    args = parser.parse_args()

    scan_directory = os.path.abspath(args.path)
    if not os.path.isdir(scan_directory):
        print(f"Error: Directory not found: {scan_directory}")
        exit(1)

    print(f"Scanning directory: {scan_directory}\n")

    all_broken_links: Dict[str, List[str]] = {}
    md_files = find_markdown_files(scan_directory)

    if not md_files:
        print("No Markdown files found in the specified directory.")
        exit(0)

    for md_file in md_files:
        print(f"---\n  Checking links in: {os.path.relpath(md_file, scan_directory)} ---")
        file_broken_links = []

        external_links, internal_links = extract_links(md_file)

        for link in external_links:
            is_valid, reason = check_external_link(link)
            if is_valid:
                print(f"  ✅ External: {link}")
            else:
                print(f"  ❌ External: {link} ({reason})")
                file_broken_links.append(f"Broken External: {link} ({reason})")

        for link in internal_links:
            is_valid, reason = check_internal_link(scan_directory, md_file, link)
            if is_valid:
                print(f"  ✅ Internal: {link}")
            else:
                print(f"  ❌ Internal: {link} ({reason})")
                file_broken_links.append(f"Broken Internal: {link} ({reason})")
        
        if file_broken_links:
            all_broken_links[os.path.relpath(md_file, scan_directory)] = file_broken_links

    print("\n--- Scan Complete ---")
    if all_broken_links:
        print(f"Found {sum(len(v) for v in all_broken_links.values())} broken links across {len(all_broken_links)} files:\n")
        for file, broken_links in all_broken_links.items():
            print(f"File: {file}")
            for link_info in broken_links:
                print(f"  - {link_info}")
            print()
        exit(1) # Exit with error code if broken links are found
    else:
        print("No broken links found. All links are perfectly entangled! ✨")
        exit(0)

if __name__ == '__main__':
    main()
