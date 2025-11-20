import os
import re
import requests
import sys
from urllib.parse import urlparse

def find_markdown_files(root_dir):
    """Recursively finds all markdown files (.md) in the given directory."""
    markdown_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.md'):
                markdown_files.append(os.path.join(dirpath, f))
    return markdown_files

def extract_urls_from_markdown(filepath):
    """Extracts external HTTP/HTTPS URLs from a markdown file."""
    urls = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Regex to find markdown links: [text](url)
            # And also bare URLs that might be present
            # This regex is simplified and might miss some edge cases, but covers common patterns.
            link_pattern = re.compile(r'\[.*?\]\((https?://[^\s)]+)\)|(https?://[^\s)]+)')
            for match in link_pattern.finditer(content):
                url = match.group(1) or match.group(2)
                if url:
                    parsed_url = urlparse(url)
                    # Only consider http/https schemes and ensure it's not a relative path
                    if parsed_url.scheme in ['http', 'https'] and parsed_url.netloc:
                        urls.add(url)
    except Exception as e:
        print(f"Error reading or parsing {filepath}: {e}")
    return list(urls)

def check_url(url, timeout=5):
    """Checks a single URL for reachability and returns its status code or an error."""
    try:
        # Use HEAD request for efficiency, fall back to GET if HEAD is not allowed
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        # If HEAD is forbidden (405) or not implemented (501), try GET
        if response.status_code in [405, 501]:
            response = requests.get(url, timeout=timeout, allow_redirects=True)
        return response.status_code
    except requests.exceptions.ConnectionError:
        return "Connection Error"
    except requests.exceptions.Timeout:
        return "Timeout"
    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}"
    except Exception as e:
        return f"Unexpected Error: {e}"

def main(root_dir="."):
    """Main function to orchestrate the link checking process."""
    print(f"🔍 Scavenging for broken links in markdown files under '{root_dir}'...")
    markdown_files = find_markdown_files(root_dir)
    if not markdown_files:
        print("✅ No markdown files found to scavenge.")
        return

    broken_links_found = False
    for md_file in markdown_files:
        print(f"\nProcessing: {md_file}")
        urls = extract_urls_from_markdown(md_file)
        if not urls:
            print("  No external links found.")
            continue

        file_has_broken_links = False
        for url in urls:
            status = check_url(url)
            if isinstance(status, int) and 200 <= status < 300:
                print(f"  [OK] {url} (Status: {status})")
            else:
                print(f"  [BROKEN] {url} (Status: {status})")
                broken_links_found = True
                file_has_broken_links = True
        if not file_has_broken_links:
            print("  All external links appear healthy.")

    if broken_links_found:
        print("\n🚨 Scavenging complete: Some broken links were found!")
        # In a CI/CD context, you might want to exit with a non-zero code here.
        # sys.exit(1)
    else:
        print("\n✅ Scavenging complete: All external links appear healthy!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scavenge markdown files for broken external links.")
    parser.add_argument("root_dir", nargs="?", default=".",
                        help="The root directory to start scavenging from (default: current directory).")
    args = parser.parse_args()
    main(args.root_dir)
