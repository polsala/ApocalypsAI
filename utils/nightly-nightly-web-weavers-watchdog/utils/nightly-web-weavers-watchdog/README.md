# Nightly Web Weaver's Watchdog

## 🕸️ Untangle Your Web of Links! 🕸️

Welcome, brave maintainer, to the vigilant gaze of the Web Weaver's Watchdog! In the vast, ever-shifting digital landscape, links can fray, snap, and lead to dead ends, leaving your precious documentation in a tangled mess. Fear not! Our Watchdog is here to sniff out those broken threads and ensure your repository's web of knowledge remains strong and true.

This utility scans all Markdown files (`.md`) within a specified directory, extracts external URLs, and then diligently checks each one for accessibility. If a link is found to be broken (e.g., 404 Not Found, connection error, timeout), the Watchdog will bark a clear report, helping you mend the web before anyone gets lost.

## How to Unleash the Watchdog

1.  **Navigate**: Change into the `utils/nightly-web-weavers-watchdog/` directory.
2.  **Run**: Execute the `link_checker.py` script with the path to the directory you want to scan.

    ```bash
    python3 src/link_checker.py --path ../..
    ```

    (The example above scans the entire `polsala/ApocalypsAI` repository from the utility's perspective.)

### Arguments:

*   `--path <directory>`: The root directory to start scanning for Markdown files. Defaults to the current directory if not provided.

## What the Watchdog Reports

The Watchdog will output a list of any broken links it finds, along with the HTTP status code or error message, and the file(s) where the link was discovered. This way, you'll know exactly which threads need re-weaving.

```
🕸️ Web Weaver's Watchdog Report 🕸️

Scanning directory: /path/to/your/repo

Found 3 Markdown files.
Checking 5 unique external links...

🚨 BROKEN LINKS DETECTED! 🚨

[404 Not Found] https://example.com/non-existent-page
  - Found in: README.md

[Connection Error] https://broken-domain.xyz
  - Found in: docs/guide.md

[Timeout] https://slow-server.com/resource
  - Found in: CONTRIBUTING.md

All other links are holding strong! Keep up the good work!
```

Let the Web Weaver's Watchdog keep your documentation pristine and your users happily navigating your well-maintained digital tapestry!
