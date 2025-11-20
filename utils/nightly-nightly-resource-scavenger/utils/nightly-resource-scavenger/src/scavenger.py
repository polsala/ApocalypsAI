import argparse
import os
import re
import requests
from typing import List, Tuple, Dict

# Regex to find markdown links: [text](url) or [text][ref]
# And also reference links: [ref]: url
LINK_REGEX = re.compile(r'\[.*?\]\((.*?)\)|\[.*?\]\[(.*?)\]|^\s*\[(.*?)\]:\s*(.*)$', re.MULTILINE)

def find_links_in_markdown(content: str) -> Tuple[List[str], Dict[str, str]]:
    """
    Extracts all potential URLs from markdown content.
    Returns a tuple: (list of direct URLs, dict of reference links {ref: url})
    """
    direct_urls = []
    reference_links = {}

    for match in LINK_REGEX.finditer(content):
        # Direct link: [text](url)
        if match.group(1):
            url = match.group(1).strip()
            if url and not url.startswith('#'): # Ignore internal anchor links
                direct_urls.append(url)
        # Reference link usage: [text][ref]
        elif match.group(2):
            ref = match.group(2).strip()
            if ref:
                # We'll resolve these later using the reference_links dict
                pass
        # Reference definition: [ref]: url
        elif match.group(3) and match.group(4):
            ref = match.group(3).strip()
            url = match.group(4).strip()
            if ref and url:
                reference_links[ref] = url

    # Resolve reference link usages
    resolved_urls = []
    for match in LINK_REGEX.finditer(content):
        if match.group(2): # [text][ref]
            ref = match.group(2).strip()
            if ref in reference_links:
                resolved_urls.append(reference_links[ref])
    
    return direct_urls + resolved_urls, reference_links

def check_url_reachable(url: str, timeout: int = 5) -> Tuple[bool, str]:
    """
    Checks if an external URL is reachable.
    Returns (True, "OK") or (False, "Error message").
    """
    if url.startswith(('http://', 'https://')):
        try:
            # Mock rationale: In a real scenario, this would make a network request.
            # For deterministic, offline tests, we mock requests.get to control its behavior.
            response = requests.get(url, timeout=timeout, allow_redirects=True)
            if response.status_code == 200:
                return True, "OK"
            else:
                return False, f"HTTP Error: {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "Connection Error"
        except requests.exceptions.Timeout:
            return False, "Timeout"
        except requests.exceptions.RequestException as e:
            return False, f"Request Error: {e}"
    return True, "Not an external URL (skipped)" # Treat non-http/https as valid for this check

def check_local_path_exists(base_dir: str, path: str) -> Tuple[bool, str]:
    """
    Checks if a local file path exists relative to the base directory.
    Returns (True, "OK") or (False, "Error message").
    """
    if path.startswith(('http://', 'https://', 'mailto:')):
        return True, "Not a local path (skipped)" # Handled by check_url_reachable or ignored
    
    # Remove query parameters or anchors for file path checking
    path_without_query = path.split('?')[0].split('#')[0]

    full_path = os.path.normpath(os.path.join(base_dir, path_without_query))

    # Mock rationale: In a real scenario, this would access the file system.
    # For deterministic, offline tests, we mock os.path.exists to control its behavior.
    if os.path.exists(full_path):
        return True, "OK"
    else:
        return False, "File Not Found"

def scan_directory_for_broken_links(
    directory: str,
    extensions: List[str]
) -> List[Dict[str, str]]:
    """
    Scans specified files in a directory for broken links.
    """
    broken_links = []
    print(f"Scanning directory: {directory}")

    for root, _, files in os.walk(directory):
        for file_name in files:
            if any(file_name.endswith(f".{ext}") for ext in extensions):
                file_path = os.path.join(root, file_name)
                print(f"Checking file: {file_path}")
                try:
                    # Mock rationale: In a real scenario, this would read from the file system.
                    # For deterministic, offline tests, we mock open() to control its content.
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    direct_urls, reference_links = find_links_in_markdown(content)
                    
                    # Combine direct and resolved reference URLs
                    all_urls = direct_urls
                    
                    # Check external URLs
                    for url in all_urls:
                        if url.startswith(('http://', 'https://')):
                            is_reachable, message = check_url_reachable(url)
                            if not is_reachable:
                                broken_links.append({
                                    "file": file_path,
                                    "type": "External",
                                    "link": url,
                                    "reason": message
                                })
                        elif not url.startswith('mailto:'): # Assume mailto links are fine
                            # Check local paths
                            is_exists, message = check_local_path_exists(root, url)
                            if not is_exists:
                                broken_links.append({
                                    "file": file_path,
                                    "type": "Internal",
                                    "link": url,
                                    "reason": message
                                })

                except Exception as e:
                    broken_links.append({
                        "file": file_path,
                        "type": "File Read Error",
                        "link": "N/A",
                        "reason": str(e)
                    })
    return broken_links

def main():
    parser = argparse.ArgumentParser(
        description="Scans markdown files for broken external and internal links."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--extensions",
        type=str,
        default="md,markdown",
        help="Comma-separated list of file extensions to scan (e.g., 'md,txt')."
    )
    args = parser.parse_args()

    extensions = [ext.strip() for ext in args.extensions.split(',')]
    
    broken_links = scan_directory_for_broken_links(args.path, extensions)

    if broken_links:
        print("\n--- Broken Links Found ---")
        for link_info in broken_links:
            print(f"File: {link_info['file']}")
            print(f"  Type: {link_info['type']}")
            print(f"  Link: {link_info['link']}")
            print(f"  Reason: {link_info['reason']}\n")
        print(f"Scan complete. Found {len(broken_links)} broken links.")
        exit(1) # Indicate failure if broken links are found
    else:
        print("\nScan complete. No broken links found. The digital wasteland is surprisingly intact!")
        exit(0)

if __name__ == "__main__":
    main()
