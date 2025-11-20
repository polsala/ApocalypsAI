# Nightly Resource Scavenger

## 🔍 Overview

The `nightly-resource-scavenger` is a whimsical-yet-useful utility designed to help maintain the health of your repository's documentation. In the post-apocalyptic digital landscape, links can decay rapidly. This tool acts as a diligent scavenger, sifting through your markdown files (`.md`) to find and report any external HTTP/HTTPS links that have gone stale or are no longer reachable.

It performs a lightweight check (HEAD request, falling back to GET if necessary) on each identified external URL and reports its HTTP status code. This allows you to quickly identify and fix broken references in your `README.md`, `AGENTS.md`, or any other documentation.

## ✨ Features

*   **Markdown Scanning**: Recursively finds all `.md` files within a specified directory.
*   **External Link Extraction**: Identifies `[text](url)` and bare `http(s)://` URLs.
*   **Reachability Check**: Uses HTTP HEAD/GET requests to determine if links are active.
*   **Status Reporting**: Clearly indicates `[OK]` (2xx status) or `[BROKEN]` (non-2xx status, connection errors, timeouts).

## 🚀 How to Run

1.  **Navigate to the utility's directory**:
    ```bash
    cd utils/nightly-resource-scavenger
    ```
2.  **Run the scavenger script**: (Python 3.11+ required)
    ```bash
    python3 src/scavenger.py [root_directory]
    ```
    *   `[root_directory]` (optional): The path to the directory you want to scan. If omitted, it defaults to the current directory (`.`).

### Example:

To scan the entire `polsala/ApocalypsAI` repository from its root:

```bash
python3 utils/nightly-resource-scavenger/src/scavenger.py .
```

## 📝 Example Output

```
🔍 Scavenging for broken links in markdown files under '.'...

Processing: README.md
  [OK] https://github.com/polsala/ApocalypsAI (Status: 200)
  [BROKEN] https://example.com/non-existent-page (Status: 404)
  [BROKEN] http://unreachable-domain.xyz (Status: Connection Error)
  [OK] https://docs.github.com/en/actions (Status: 200)

Processing: agents/AGENTS.md
  No external links found.

Processing: utils/nightly-apocalypse-countdown-timer/README.md
  [OK] https://pypi.org/project/rich/ (Status: 200)
  All external links appear healthy.

🚨 Scavenging complete: Some broken links were found!
```

## 🚧 Limitations

*   Currently focuses exclusively on **external HTTP/HTTPS links**. Internal relative links (e.g., `[file](./path/to/file.md)`) and anchor links (e.g., `[section](#section)`) are ignored.
*   The link extraction regex is robust for common markdown patterns but might miss highly unusual or malformed URLs.
*   Does not perform deep content analysis; only checks the HTTP status of the URL.
