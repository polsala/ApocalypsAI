# README Link Auditor

## 📜 The Digital Archaeologist for Your Docs

The `readme-link-auditor` is a whimsical-yet-essential utility that acts as a digital archaeologist, diligently unearthing ancient (broken) links in your `README.md` files. It scans for external URLs, checks their reachability, and reports any that have succumbed to the sands of time (HTTP 4xx/5xx errors or connection failures).

This tool helps maintain the integrity of your project's documentation, preventing users from clicking into the void and ensuring your `README.md` remains a reliable guide, not a historical graveyard of broken promises.

## ✨ Features

*   **Link Extraction**: Identifies both `[text](url)` and raw `<url>` formats in Markdown.
*   **Reachability Check**: Performs HTTP GET requests to verify if external links are still active.
*   **Detailed Reporting**: Provides a clear summary of valid, broken, and unreachable links.
*   **Self-Contained**: A single Python script with minimal dependencies.

## 🚀 Usage

1.  **Navigate** to the `utils/readme-link-auditor/` directory.
2.  **Run** the script, providing the path to your `README.md` file:

    ```bash
    python src/link_auditor.py --file ../../README.md
    ```

    (Adjust `../../README.md` to the actual path of the README you want to audit.)

### Example Output

```
🔍 Auditing README.md for broken links...

✅ Valid Links:
  - https://github.com/polsala/ApocalypsAI (Status: 200 OK)
  - https://example.com/working (Status: 200 OK)

❌ Broken Links:
  - https://example.com/404 (Status: 404 Not Found)
  - https://example.com/server-error (Status: 500 Internal Server Error)

⚠️ Unreachable Links:
  - https://nonexistent-domain.xyz (Error: Connection failed)

Summary: 2 valid, 2 broken, 1 unreachable.
```

## 🛠️ Development

The tool is written in Python 3.11 and uses the `requests` library for HTTP checks.
Tests are located in `tests/test_link_auditor.py` and use `unittest.mock` for deterministic, offline execution.
