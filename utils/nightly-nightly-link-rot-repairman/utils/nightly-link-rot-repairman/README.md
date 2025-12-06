# Nightly Link Rot Repairman

## Description

The `Nightly Link Rot Repairman` is a whimsical-yet-useful utility designed to combat the insidious decay of digital documentation: link rot. It diligently scans specified directories for Markdown files, extracts all external URLs, and then attempts to verify their accessibility. Any links that return an error (e.g., 404 Not Found, connection timeout) are reported, allowing you to mend the broken pathways in your documentation.

This tool helps maintain the integrity and reliability of your project's documentation, ensuring that readers can always follow the intended references.

## Usage

To run the Link Rot Repairman, navigate to its directory and execute the `link_checker.py` script with the `--dir` argument pointing to the directory you wish to scan.

```bash
python src/link_checker.py --dir /path/to/your/docs
```

### Arguments

*   `--dir <path>`: The root directory to start scanning for Markdown files. (Required)
*   `--timeout <seconds>`: Timeout for HTTP requests in seconds. Default is 5 seconds.

## Example Output

```
Scanning directory: /path/to/your/docs

Found 2 markdown files.

Checking links...

[✅] https://example.com/valid-link
[❌] https://broken.example.com/404 (Status: 404 Not Found)
    -> Found in: /path/to/your/docs/README.md
[❌] https://nonexistent.example.org (Error: Connection Error)
    -> Found in: /path/to/your/docs/docs/guide.md

Scan complete.
Found 2 broken links:
  - https://broken.example.com/404 (Status: 404 Not Found)
    -> Found in: /path/to/your/docs/README.md
  - https://nonexistent.example.org (Status: Connection Error)
    -> Found in: /path/to/your/docs/docs/guide.md
```
