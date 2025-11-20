import os
import argparse
import requests
from markdown_it import MarkdownIt
from urllib.parse import urlparse

def scan_directory_for_markdown_files(directory):
    """Recursively scans a directory for Markdown files."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.md', '.markdown')):
                yield os.path.join(root, file)

def extract_links_from_markdown(markdown_content):
    """Extracts all HTTP/HTTPS links from Markdown content, including line numbers."""
    md = MarkdownIt()
    tokens = md.parse(markdown_content)
    links = []
    for token in tokens:
        if token.type == 'link_open':
            href = token.attrGet('href')
            if href and (href.startswith('http://') or href.startswith('https://')):
                # markdown-it tokens have `map` attribute which is [start_line, end_line]
                line_number = token.map[0] + 1 if token.map else None
                links.append({'url': href, 'line': line_number})
    return links

def check_link_status(url, timeout=5):
    """Checks the HTTP status of a URL using a HEAD request."""
    try:
        # Use HEAD request for efficiency, but fall back to GET if HEAD is not allowed
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return 'OK', response.status_code
    except requests.exceptions.HTTPError as e:
        return 'BROKEN', e.response.status_code
    except requests.exceptions.ConnectionError:
        return 'BROKEN', 'Connection Error'
    except requests.exceptions.Timeout:
        return 'BROKEN', 'Timeout'
    except requests.exceptions.RequestException as e:
        return 'BROKEN', f'Request Error: {e}'

def main():
    parser = argparse.ArgumentParser(description="Scan Markdown files for broken links.")
    parser.add_argument('--path', type=str, default='.',
                        help='The root directory to start scanning for Markdown files.')
    args = parser.parse_args()

    target_directory = args.path
    print(f"Scanning directory: {target_directory}")

    markdown_files = list(scan_directory_for_markdown_files(target_directory))
    print(f"Found {len(markdown_files)} Markdown files.\n")

    broken_links_found = 0
    for md_file_path in markdown_files:
        print(f"Checking links in file: {md_file_path}")
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            links = extract_links_from_markdown(content)

            if not links:
                print("  No external links found.")
                continue

            file_has_broken_links = False
            for link_info in links:
                url = link_info['url']
                line = link_info['line']
                status, detail = check_link_status(url)
                if status == 'BROKEN':
                    broken_links_found += 1
                    file_has_broken_links = True
                    print(f"  [Broken Link] {url} (Status: {detail}) - Line {line}")
            if not file_has_broken_links:
                print("  All links are healthy.")

        except Exception as e:
            print(f"  [Error] Could not process file {md_file_path}: {e}")
        print()

    if broken_links_found > 0:
        print(f"Scan complete. Found {broken_links_found} broken links.")
        exit(1) # Indicate failure if broken links are found
    else:
        print("Scan complete. All links are healthy.")
        exit(0) # Indicate success

if __name__ == '__main__':
    main()
