import argparse
import os
import re
import requests
from urllib.parse import urlparse

# Regex to find Markdown links: [text](url) or <url>
# This regex is simplified and might not catch all edge cases, but covers common patterns.
LINK_REGEX = re.compile(r'\[[^\]]+\]\((https?://[^)]+)\)|<(https?://[^>]+)>')

def extract_links_from_markdown(content: str) -> set[str]:
    """Extracts unique external HTTP/HTTPS links from Markdown content."""
    links = set()
    for match in LINK_REGEX.finditer(content):
        if match.group(1):  # [text](url) pattern
            links.add(match.group(1))
        elif match.group(2): # <url> pattern
            links.add(match.group(2))
    return links

def check_link(url: str, timeout: int = 5) -> tuple[str, str]:
    """Checks a single URL and returns its status and a message.
    Returns a tuple: (status_category, message)
    """
    try:
        # Use HEAD request to avoid downloading full content, but fall back to GET if HEAD is not allowed
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        if 200 <= response.status_code < 300: # OK
            return "OK", url
        elif 300 <= response.status_code < 400: # Redirect
            final_url = response.url # requests automatically follows redirects
            if final_url != url:
                return "REDIRECT", f"{url} (-> {final_url})"
            else:
                return "OK", url # Should not happen if it's a redirect, but for explicit handling
        else: # Should be caught by raise_for_status, but for explicit handling
            return "BROKEN", f"{url} (Status: {response.status_code} {response.reason})"
    except requests.exceptions.HTTPError as e:
        return "BROKEN", f"{url} (Status: {e.response.status_code} {e.response.reason})"
    except requests.exceptions.ConnectionError as e:
        return "ERROR", f"{url} (Connection Error: {e})"
    except requests.exceptions.Timeout as e:
        return "ERROR", f"{url} (Timeout Error: {e})"
    except requests.exceptions.RequestException as e:
        return "ERROR", f"{url} (Request Error: {e})"
    except Exception as e:
        return "ERROR", f"{url} (Unexpected Error: {e})"

def main():
    parser = argparse.ArgumentParser(
        description="Check external links in Markdown files."
    )
    parser.add_argument(
        "path_to_scan",
        type=str,
        help="The directory or file to scan for Markdown files."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Maximum time in seconds to wait for a link check (default: 5)."
    )
    parser.add_argument(
        "--ignore-domain",
        action="append",
        default=[],
        help="A domain to ignore during link checking (e.g., example.com). Can be specified multiple times."
    )
    parser.add_argument(
        "--ignore-pattern",
        action="append",
        default=[],
        help="A regex pattern for URLs to ignore (e.g., ^https://localhost). Can be specified multiple times."
    )

    args = parser.parse_args()

    all_links = set()
    markdown_extensions = ('.md', '.markdown')

    print(f"Scanning path: {args.path_to_scan}")

    if os.path.isfile(args.path_to_scan):
        if args.path_to_scan.lower().endswith(markdown_extensions):
            try:
                with open(args.path_to_scan, 'r', encoding='utf-8') as f:
                    content = f.read()
                    all_links.update(extract_links_from_markdown(content))
            except Exception as e:
                print(f"Error reading {args.path_to_scan}: {e}")
                exit(1)
        else:
            print(f"Error: '{args.path_to_scan}' is not a Markdown file.")
            exit(1)
    elif os.path.isdir(args.path_to_scan):
        for root, _, files in os.walk(args.path_to_scan):
            for file in files:
                if file.lower().endswith(markdown_extensions):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            all_links.update(extract_links_from_markdown(content))
                    except Exception as e:
                        print(f"Error reading {filepath}: {e}")
                        # Continue scanning other files even if one fails to read
    else:
        print(f"Error: '{args.path_to_scan}' is not a valid file or directory.")
        exit(1)

    results = []
    ignored_count = 0
    ignore_patterns = [re.compile(p) for p in args.ignore_pattern]

    for link in sorted(list(all_links)): # Sort for deterministic output
        parsed_url = urlparse(link)
        domain = parsed_url.netloc

        should_ignore = False
        if domain in args.ignore_domain:
            should_ignore = True
        else:
            for pattern in ignore_patterns:
                if pattern.match(link):
                    should_ignore = True
                    break

        if should_ignore:
            print(f"[IGNORED] {link}")
            ignored_count += 1
            continue

        status, message = check_link(link, args.timeout)
        results.append((status, message))
        print(f"[{status}] {message}")

    print("\n--- Summary ---")
    total_scanned = len(all_links)
    total_checked = total_scanned - ignored_count
    ok_count = sum(1 for s, _ in results if s == "OK")
    redirect_count = sum(1 for s, _ in results if s == "REDIRECT")
    broken_count = sum(1 for s, _ in results if s == "BROKEN")
    error_count = sum(1 for s, _ in results if s == "ERROR")

    print(f"Total links scanned: {total_scanned}")
    print(f"Total links checked: {total_checked}")
    print(f"OK: {ok_count}")
    print(f"Redirects: {redirect_count}")
    print(f"Broken: {broken_count}")
    print(f"Errors: {error_count}")
    print(f"Ignored: {ignored_count}")

    if broken_count > 0 or error_count > 0:
        exit(1) # Indicate failure if any broken or error links

if __name__ == "__main__":
    main()
