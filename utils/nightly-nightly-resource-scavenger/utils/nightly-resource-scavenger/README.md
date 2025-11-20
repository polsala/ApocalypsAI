# Nightly Resource Scavenger

The digital wasteland is full of forgotten paths and crumbling connections. The Nightly Resource Scavenger is here to help you mend the broken web of your repository's documentation. It tirelessly combs through your markdown files, identifying external links that lead to nowhere and internal paths that have vanished into the ether. Keep your knowledge base pristine, even after the apocalypse!

## Features

*   **External Link Validation**: Checks if URLs are reachable.
*   **Internal Path Verification**: Ensures local file paths referenced in markdown exist.
*   **Configurable Scan**: Specify directories and file extensions to scan.
*   **Detailed Reporting**: Outputs a list of all broken links found.

## Usage

Run the scavenger from your repository root:

```bash
python3 -m utils.nightly-resource-scavenger.src.scavenger --path . --extensions md,txt
```

### Arguments

*   `--path <directory>`: The root directory to start scanning from (default: current directory).
*   `--extensions <ext1,ext2,...>`: Comma-separated list of file extensions to scan (default: `md,markdown`).

## Example Output

```
Scanning directory: .
Checking file: README.md
  Broken External Link: https://nonexistent-site.com/page (HTTP Error: 404)
  Broken Internal Link: ./docs/missing-file.md (File Not Found)
Checking file: agents/AGENTS.md
  Broken External Link: https://another-dead-link.org (HTTP Error: 500)

Scan complete. Found 3 broken links.
```
