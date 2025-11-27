# Nightly Broken Link Beacon

## 🔦 Overview

The Nightly Broken Link Beacon is a vigilant utility designed to scan your repository's Markdown files (like `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, etc.) for external HTTP/HTTPS links. It then attempts to reach these links to verify their accessibility. If a link is broken or unreachable, the Beacon will report it, helping you maintain up-to-date and reliable documentation.

No more dead ends in your docs! This tool ensures your project's external references are always pointing to valid destinations, keeping your community informed and your project's credibility intact.

## 🚀 How to Use

1.  **Navigate to the utility directory:**
    ```bash
    cd utils/nightly-broken-link-beacon
    ```
2.  **Run the script:**
    ```bash
    python3 src/link_checker.py <path_to_repository_root>
    ```
    Replace `<path_to_repository_root>` with the absolute or relative path to the directory you want to scan. For example, to scan the current directory:
    ```bash
    python3 src/link_checker.py .
    ```

## 💡 Example Output

```
Scanning directory: .
Found 2 Markdown files.

Checking links in README.md:
  ✅ https://github.com/polsala/ApocalypsAI (Status: 200)
  ❌ https://example.com/broken-link (Status: 404 - Not Found)
  ⚠️ https://another-site.org/unreachable (Error: Connection refused)

Checking links in docs/CONTRIBUTING.md:
  ✅ https://docs.github.com/en/get-started/quickstart/contributing-to-projects (Status: 200)

Scan complete. Found 2 broken/unreachable links.
```

## 🛠️ Development

This utility is written in Python 3.11 and uses the `requests` library for HTTP requests. Tests are located in the `tests/` directory and can be run using `pytest`.

```bash
pytest tests/
```
