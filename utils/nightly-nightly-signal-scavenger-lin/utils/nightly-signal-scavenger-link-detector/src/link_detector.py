import requests
import sys
import argparse
from typing import List, Dict, Tuple

def _check_single_link(url: str, timeout: float = 5.0) -> Tuple[str, int, str]:
    """
    Checks a single URL for reachability.
    Returns (url, status_code, error_message).
    """
    try:
        # Use stream=True and then r.raise_for_status() to handle large responses efficiently
        # and ensure status code is checked before reading content.
        # However, for just checking reachability, a simple get is fine.
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        return url, response.status_code, "OK" if response.status_code < 400 else "Client/Server Error"
    except requests.exceptions.Timeout:
        return url, 0, "Timeout"
    except requests.exceptions.ConnectionError:
        return url, 0, "Connection Error"
    except requests.exceptions.RequestException as e:
        return url, 0, f"Request Error: {e}"

def check_links(urls: List[str], timeout: float = 5.0) -> List[Dict]:
    """
    Checks a list of URLs and returns a list of dictionaries with their status.
    """
    results = []
    for url in urls:
        url = url.strip()
        if not url:
            continue
        _, status_code, message = _check_single_link(url, timeout)
        results.append({
            "url": url,
            "status_code": status_code,
            "message": message
        })
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Signal Scavenger's Dead Link Detector: Scans URLs for reachability."
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        type=str,
        help="Path to a file containing URLs (one per line). If not provided, reads from stdin."
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Timeout in seconds for each URL request (default: 5.0)."
    )
    args = parser.parse_args()

    urls_to_check = []
    if args.input_file:
        try:
            with open(args.input_file, 'r') as f:
                urls_to_check = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
            sys.exit(1)
    else:
        print("Reading URLs from stdin. Press Ctrl+D (or Ctrl+Z on Windows) when done.")
        urls_to_check = [line.strip() for line in sys.stdin if line.strip()]

    if not urls_to_check:
        print("No URLs provided to check.", file=sys.stderr)
        sys.exit(0)

    print(f"Checking {len(urls_to_check)} URLs with a timeout of {args.timeout} seconds...")
    results = check_links(urls_to_check, args.timeout)

    print("\n--- Link Check Results ---")
    dead_links_found = False
    for result in results:
        status = "✅ REACHABLE" if result["status_code"] >= 200 and result["status_code"] < 400 else "❌ UNREACHABLE"
        if status == "❌ UNREACHABLE":
            dead_links_found = True
        print(f"{status} | {result['status_code'] if result['status_code'] != 0 else 'N/A'} | {result['url']} ({result['message']})")

    if dead_links_found:
        sys.exit(1) # Indicate failure if dead links are found
    else:
        sys.exit(0) # Indicate success if all links are good

if __name__ == "__main__":
    main()
