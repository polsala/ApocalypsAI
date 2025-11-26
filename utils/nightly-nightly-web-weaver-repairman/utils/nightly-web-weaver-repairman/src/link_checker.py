import os
import re
import requests
from typing import List, Tuple, Dict

# Define a timeout for requests to prevent hanging
REQUEST_TIMEOUT = 5

def find_markdown_files(root_dir: str) -> List[str]:
    """
    Recursively finds all Markdown files (.md) in the given root directory.
    """
    markdown_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.md'):
                markdown_files.append(os.path.join(dirpath, f))
    return markdown_files

def extract_external_links(file_path: str) -> List[str]:
    """
    Extracts external HTTP/HTTPS links from a Markdown file.
    """
    links = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Regex to find Markdown links: [text](url)
            # It's a bit simplified, but covers most common cases.
            # We specifically look for http(s):// to filter external links.
            matches = re.findall(r'\[.*?\]\((https?://[^\s)]+)\)', content)
            for url in matches:
                # Basic validation to ensure it's a full URL and not just a fragment
                if url.startswith('http://') or url.startswith('https://'):
                    links.append(url)
    except Exception as e:
        print(f"Error reading or parsing {file_path}: {e}")
    return links

def check_link_status(url: str) -> Tuple[bool, str]:
    """
    Checks the status of a given URL using an HTTP HEAD request.
    Returns (is_broken, status_message).
    """
    try:
        response = requests.head(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        if 200 <= response.status_code < 400:
            return False, f"{response.status_code} OK"
        else:
            return True, f"{response.status_code} {response.reason}"
    except requests.exceptions.ConnectionError:
        return True, "Connection Error"
    except requests.exceptions.Timeout:
        return True, "Timeout Error"
    except requests.exceptions.RequestException as e:
        return True, f"Request Error: {e}"

def main():
    print("Scanning for broken links...")
    # Assume the script is run from the repository root or a sub-directory
    # We need to find the repository root to scan all .md files
    current_dir = os.getcwd()
    repo_root = current_dir # For simplicity, assume current_dir is repo_root for now.
                            # In a real scenario, one might traverse up to find .git/

    markdown_files = find_markdown_files(repo_root)
    print(f"Found {len(markdown_files)} .md files.")

    broken_links: Dict[str, List[Tuple[str, str]]] = {} # {file_path: [(url, status_message)]}

    for md_file in markdown_files:
        links_in_file = extract_external_links(md_file)
        for link in links_in_file:
            print(f"Checking link: {link} (from {os.path.basename(md_file)})")
            is_broken, status_message = check_link_status(link)
            if is_broken:
                if md_file not in broken_links:
                    broken_links[md_file] = []
                broken_links[md_file].append((link, status_message))

    if broken_links:
        print("\n--- Broken Links Found ---")
        for file_path, links_data in broken_links.items():
            for url, status_msg in links_data:
                print(f"- {os.path.relpath(file_path, repo_root)}: {url} ({status_msg})")
    else:
        print("\nNo broken links found. All web weavers are in good repair!")

if __name__ == "__main__":
    main()
