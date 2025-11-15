import argparse
import re
import requests
from typing import List, Tuple, Dict, Optional

# Regex to find Markdown links: [text](url) or <url>
# It's a bit simplified, but covers most common cases.
# Group 1: URL from [text](url)
# Group 2: URL from <url>
LINK_REGEX = re.compile(r'\[.*?\]\((https?://[^\s)]+)\)|<(https?://[^\s>]+)>')

def extract_links(markdown_content: str) -> List[str]:
    """
    Extracts unique URLs from markdown content.
    """
    found_links = set()
    for match in LINK_REGEX.finditer(markdown_content):
        if match.group(1):  # Link from [text](url)
            found_links.add(match.group(1))
        elif match.group(2): # Link from <url>
            found_links.add(match.group(2))
    return sorted(list(found_links))

def check_link(url: str) -> Tuple[int, Optional[str]]:
    """
    Checks the reachability and status of a single URL.
    Returns (status_code, error_message) or (200, None) for success.
    """
    try:
        # Use a short timeout to avoid hanging on unresponsive servers
        response = requests.get(url, timeout=5, allow_redirects=True)
        if 200 <= response.status_code < 400:
            return response.status_code, None
        else:
            return response.status_code, f"{response.status_code} {response.reason}"
    except requests.exceptions.ConnectionError:
        return 0, "Connection failed"
    except requests.exceptions.Timeout:
        return 0, "Timeout"
    except requests.exceptions.RequestException as e:
        return 0, f"Request error: {e}"

def audit_readme(file_path: str) -> Dict[str, List[Tuple[str, int, Optional[str]]]]:
    """
    Reads a README file, extracts links, and checks their status.
    Returns a dictionary categorizing links.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        return {}
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return {}

    links = extract_links(content)
    results = {
        "valid": [],
        "broken": [],
        "unreachable": []
    }

    print(f"🔍 Auditing '{file_path}' for broken links...")
    for url in links:
        status_code, error_msg = check_link(url)
        if error_msg is None:
            results["valid"].append((url, status_code, None))
        elif status_code == 0: # Connection/request error
            results["unreachable"].append((url, status_code, error_msg))
        else: # HTTP 4xx/5xx error
            results["broken"].append((url, status_code, error_msg))
        print(f"  - Checked {url}: {'OK' if error_msg is None else 'FAIL'} ({status_code if status_code != 0 else error_msg})")

    return results

def main():
    parser = argparse.ArgumentParser(
        description="Audits a README.md file for broken external links."
    )
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to the README.md file to audit."
    )
    args = parser.parse_args()

    results = audit_readme(args.file)

    print("\n" + "="*30)
    print("Link Audit Report")
    print("="*30)

    if results.get("valid"):
        print("\n✅ Valid Links:")
        for url, status, _ in results["valid"]:
            print(f"  - {url} (Status: {status} OK)")

    if results.get("broken"):
        print("\n❌ Broken Links:")
        for url, status, error in results["broken"]:
            print(f"  - {url} (Status: {error})")

    if results.get("unreachable"):
        print("\n⚠️ Unreachable Links:")
        for url, _, error in results["unreachable"]:
            print(f"  - {url} (Error: {error})")

    total_links = sum(len(v) for v in results.values())
    num_valid = len(results.get("valid", []))
    num_broken = len(results.get("broken", []))
    num_unreachable = len(results.get("unreachable", []))

    print(f"\nSummary: {num_valid} valid, {num_broken} broken, {num_unreachable} unreachable out of {total_links} links.")

    if num_broken > 0 or num_unreachable > 0:
        exit(1) # Indicate failure if any broken/unreachable links
    else:
        exit(0)

if __name__ == "__main__":
    main()
