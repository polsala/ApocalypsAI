import argparse
import re
import requests
from typing import List, Tuple, Dict

# Regex to find URLs. This is a simplified version,
# a more robust one might be needed for production,
# but this covers common cases in text files.
URL_REGEX = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
)

def find_urls_in_file(filepath: str) -> List[str]:
    """
    Reads a file and extracts all unique URLs found within it.
    """
    urls = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            found_urls = URL_REGEX.findall(content)
            for url in found_urls:
                urls.add(url)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return []
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return []
    return sorted(list(urls))

def check_url(url: str, timeout: int = 5) -> Tuple[str, str]:
    """
    Checks the reachability of a single URL using an HTTP HEAD request.
    Returns a tuple of (url, status_message).
    """
    try:
        # Use HEAD request as it's lighter than GET and usually sufficient for status.
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        if 200 <= response.status_code < 400:
            return url, "OK"
        else:
            return url, f"BROKEN (Status: {response.status_code})"
    except requests.exceptions.ConnectionError:
        return url, "UNREACHABLE (Connection Error)"
    except requests.exceptions.Timeout:
        return url, "UNREACHABLE (Timeout)"
    except requests.exceptions.RequestException as e:
        return url, f"UNREACHABLE (Request Error: {e})"
    except Exception as e:
        return url, f"UNREACHABLE (Unexpected Error: {e})"

def detect_dead_links(filepath: str) -> Dict[str, List[str]]:
    """
    Orchestrates the process of finding and checking URLs in a file.
    Returns a dictionary categorizing links.
    """
    print(f"Scanning {filepath} for ancient echoes...")
    urls = find_urls_in_file(filepath)
    if not urls:
        print("No URLs found to check.")
        return {"ok": [], "broken": [], "unreachable": []}

    results = {"ok": [], "broken": [], "unreachable": []}
    total_urls = len(urls)
    for i, url in enumerate(urls):
        print(f"  Checking [{i+1}/{total_urls}]: {url}...", end='\r')
        _, status = check_url(url)
        if "OK" in status:
            results["ok"].append(url)
        elif "BROKEN" in status:
            results["broken"].append(f"{url} ({status.split('Status: ')[1].strip(')')})")
        else:
            results["unreachable"].append(f"{url} ({status.split('(')[1].strip(')')})")
    print("\nScan complete!")
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Unearth broken links within text files."
    )
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to the file to scan for URLs."
    )
    args = parser.parse_args()

    results = detect_dead_links(args.file)

    print("\n--- Ancient Echoes Report ---")
    if results["broken"]:
        print("\n💔 Broken Links Found:")
        for link in results["broken"]:
            print(f"  - {link}")
    else:
        print("\n✅ No Broken Links Found!")

    if results["unreachable"]:
        print("\n⚠️ Unreachable Links (Connection/Timeout/Other Errors):")
        for link in results["unreachable"]:
            print(f"  - {link}")

    if results["ok"]:
        print(f"\n✨ {len(results['ok'])} Healthy Links Found.")

    if results["broken"] or results["unreachable"]:
        exit(1) # Indicate failure if any broken/unreachable links
    else:
        exit(0) # Indicate success

if __name__ == "__main__":
    main()
