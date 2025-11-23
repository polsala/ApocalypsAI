import os
import re
import argparse
import requests
from typing import List, Tuple, Dict

# Regex to find Markdown links: [text](url)
# It captures the URL part. It's a simplified regex and might not catch all edge cases,
# but it's robust enough for common Markdown link formats.
MARKDOWN_LINK_REGEX = re.compile(r'\[[^\]]+\]\((https?://[^\s)]+)\)')

def find_markdown_files(root_dir: str) -> List[str]:
    """Finds all markdown files (.md, .markdown) within a given directory."""
    markdown_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(('.md', '.markdown')):
                markdown_files.append(os.path.join(dirpath, filename))
    return markdown_files

def extract_urls_from_markdown(content: str) -> List[str]:
    """Extracts all URLs from markdown content using a regex."""
    return MARKDOWN_LINK_REGEX.findall(content)

def check_url_status(url: str, timeout: int = 5) -> Tuple[bool, str]:
    """Checks the HTTP status of a given URL.

    Returns a tuple: (is_ok, status_message)
    """
    try:
        # Use HEAD request for efficiency, as we only need the status code
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if response.status_code == 200:
            return True, "OK"
        else:
            return False, f"{response.status_code} {response.reason}"
    except requests.exceptions.ConnectionError:
        return False, "Connection Error"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except requests.exceptions.RequestException as e:
        return False, f"Request Error: {e}"
    except Exception as e:
        return False, f"Unexpected Error: {e}"

def main():
    parser = argparse.ArgumentParser(
        description="Scans markdown files for external URLs and reports broken links."
    )
    parser.add_argument(
        "--dir",
        type=str,
        required=True,
        help="The root directory to start scanning for Markdown files."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Timeout for HTTP requests in seconds. Default is 5 seconds."
    )

    args = parser.parse_args()
    target_dir = args.dir
    timeout = args.timeout

    if not os.path.isdir(target_dir):
        print(f"Error: Directory '{target_dir}' not found.")
        exit(1)

    print(f"Scanning directory: {target_dir}\n")

    markdown_files = find_markdown_files(target_dir)
    if not markdown_files:
        print("No markdown files found.")
        exit(0)

    print(f"Found {len(markdown_files)} markdown files.\n")
    print("Checking links...\n")

    broken_links: List[Dict[str, str]] = []
    # Use a set to store URLs that have already been checked to avoid redundant network requests
    checked_urls = set()

    for filepath in markdown_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            urls = extract_urls_from_markdown(content)

            for url in urls:
                if url in checked_urls:
                    continue # Skip if already checked
                checked_urls.add(url)

                is_ok, status_msg = check_url_status(url, timeout)
                if is_ok:
                    print(f"[✅] {url}")
                else:
                    print(f"[❌] {url} (Status: {status_msg})")
                    broken_links.append({
                        "url": url,
                        "status": status_msg,
                        "file": filepath
                    })
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")

    print("\nScan complete.")
    if broken_links:
        print(f"Found {len(broken_links)} broken links:")
        for link_info in broken_links:
            print(f"  - {link_info['url']} (Status: {link_info['status']})")
            print(f"    -> Found in: {link_info['file']}")
        exit(1) # Exit with error code if broken links are found
    else:
        print("No broken links found. All clear!")
        exit(0)

if __name__ == "__main__":
    main()
