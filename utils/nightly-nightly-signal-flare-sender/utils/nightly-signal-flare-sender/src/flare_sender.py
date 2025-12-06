import requests
import argparse
import sys

def check_url(url: str, session: requests.Session) -> str:
    """Checks a single URL and returns its status."""
    try:
        response = session.get(url, timeout=5, allow_redirects=True)
        if 200 <= response.status_code < 300:
            return f"[{response.status_code} OK]"
        elif response.status_code == 404:
            return f"[{response.status_code} Not Found]"
        else:
            return f"[{response.status_code} {response.reason}]"
    except requests.exceptions.ConnectionError:
        return "[Connection Error]"
    except requests.exceptions.Timeout:
        return "[Timeout Error]"
    except requests.exceptions.RequestException as e:
        return f"[Request Error: {e}]"

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Signal Flare Sender: Check the status of URLs from a file."
    )
    parser.add_argument(
        "--urls", 
        type=str, 
        required=True, 
        help="Path to a file containing URLs, one per line."
    )
    args = parser.parse_args()

    try:
        with open(args.urls, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: URL file not found at '{args.urls}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading URL file: {e}", file=sys.stderr)
        sys.exit(1)

    if not urls:
        print("No URLs found in the provided file.")
        sys.exit(0)

    print(f"Initiating signal flare scan for {len(urls)} URLs...")
    with requests.Session() as session:
        for url in urls:
            status = check_url(url, session)
            print(f"Checking URL: {url} ... {status}")

    print("Signal flare scan complete.")

if __name__ == "__main__":
    main()
