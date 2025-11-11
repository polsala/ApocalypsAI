import os
import re
import argparse
from typing import List, Tuple

def find_markdown_files(root_dir: str) -> List[str]:
    """
    Recursively finds all Markdown files (.md) in the given directory.
    """
    markdown_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.md'):
                markdown_files.append(os.path.join(dirpath, f))
    return markdown_files

def parse_markdown_for_links(content: str) -> List[str]:
    """
    Parses Markdown content to find internal relative links.
    Ignores external links (http/https) and anchor links (#).
    """
    # Regex to find Markdown links: [text](path)
    # Group 1: link path
    link_pattern = re.compile(r'\[.*?\]\((.*?)\)')
    links = []
    for match in link_pattern.finditer(content):
        link_path = match.group(1)
        # Ignore external links
        if link_path.startswith('http://') or link_path.startswith('https://'):
            continue
        # Ignore anchor links within the same file
        if link_path.startswith('#'):
            continue
        links.append(link_path)
    return links

def check_links(root_dir: str, markdown_files: List[str]) -> List[Tuple[str, str, str]]:
    """
    Checks if internal relative links in Markdown files point to existing files.
    Returns a list of (file_path, broken_link_text, resolved_broken_path).
    """
    broken_links_report = []
    for file_path in markdown_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            links_in_file = parse_markdown_for_links(content)
            
            for link_path in links_in_file:
                # Resolve the link path relative to the current Markdown file's directory
                file_dir = os.path.dirname(file_path)
                resolved_path = os.path.normpath(os.path.join(file_dir, link_path))

                # Check if the resolved path exists and is a file
                # For simplicity, we assume all linked .md files should exist as files.
                # We don't check for directories or other file types explicitly,
                # but os.path.exists will handle non-existent paths.
                if not os.path.exists(resolved_path):
                    # Find the original link text for better reporting
                    original_link_match = re.search(r'\[(.*?)\]\(' + re.escape(link_path) + r'\)', content)
                    link_text = original_link_match.group(1) if original_link_match else link_path
                    broken_links_report.append((file_path, link_text, resolved_path))
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            continue
    return broken_links_report

def main():
    parser = argparse.ArgumentParser(
        description="Digital Dustbunny Duster: Detects broken internal Markdown links."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for Markdown files."
    )
    args = parser.parse_args()

    root_dir = args.path
    if not os.path.isdir(root_dir):
        print(f"Error: Directory '{root_dir}' not found.")
        exit(1)

    print(f"Scanning directory: {root_dir}")
    markdown_files = find_markdown_files(root_dir)
    
    if not markdown_files:
        print("No Markdown files found to scan.")
        exit(0)

    broken_links = check_links(root_dir, markdown_files)

    if broken_links:
        print("---")
        for original_file, link_text, resolved_broken_path in broken_links:
            print(f"File: {original_file}")
            print(f"  Broken link: [{link_text}]({resolved_broken_path}) -> {resolved_broken_path} (Does not exist)")
        print("---")
        print(f"Scan complete. Found {len(broken_links)} broken links in {len(set(f for f, _, _ in broken_links))} files.")
        exit(1) # Exit with 1 to indicate issues found
    else:
        print("---")
        print("Scan complete. No digital dustbunnies (broken links) found! Your documentation is pristine.")
        print("---")
        exit(0)

if __name__ == "__main__":
    main()
