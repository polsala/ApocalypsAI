# Quantum Entanglement Link Checker

## Purpose

In the ever-shifting cosmic tapestry of the internet, links can decay, leading to documentation that points to the void. The `quantum-entanglement-link-checker` ensures that your project's external references remain 'entangled' with their targets, verifying their reachability and reporting any cosmic disconnects.

This utility scans specified directories for Markdown files (`.md`, `.markdown`) and extracts all external URLs. It then attempts to connect to each URL to confirm its validity, providing a report of broken or unreachable links.

## Usage

```bash
python src/link_checker.py <path_to_scan> [--timeout <seconds>] [--ignore-domain <domain>] [--ignore-pattern <regex>]
```

- `<path_to_scan>`: The directory or file to scan for Markdown files.
- `--timeout <seconds>`: Optional. Maximum time in seconds to wait for a link check (default: 5).
- `--ignore-domain <domain>`: Optional. A domain to ignore during link checking (e.g., `example.com`). Can be specified multiple times.
- `--ignore-pattern <regex>`: Optional. A regex pattern for URLs to ignore (e.g., `^https://localhost`). Can be specified multiple times.

## Example

To check all Markdown files in the current directory and its subdirectories, with a 10-second timeout, ignoring `example.com` and any `localhost` links:

```bash
python src/link_checker.py . --timeout 10 --ignore-domain example.com --ignore-pattern "^https?://localhost"
```

## Output

The utility will print a summary of all checked links, categorizing them as `[OK]`, `[REDIRECT]`, `[BROKEN]`, or `[ERROR]` (for network issues).

```
Scanning path: .

[OK] https://www.github.com/polsala/ApocalypsAI
[REDIRECT] https://old.example.com/ (-> https://new.example.com/)
[BROKEN] https://nonexistent.link/404 (Status: 404 Not Found)
[ERROR] https://unreachable.site/ (Connection Error: Max retries exceeded)

--- Summary ---
Total links scanned: 4
Total links checked: 4
OK: 1
Redirects: 1
Broken: 1
Errors: 1
Ignored: 0
```

An exit code of `0` indicates all checked links are valid (OK or Redirect). An exit code of `1` indicates one or more broken or error links were found.
