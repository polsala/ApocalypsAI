# Nightly README Revivalist

The `nightly-readme-revivalist` is a whimsical-yet-useful utility designed to help maintain the quality and completeness of your project's `README.md` files. In the post-apocalyptic landscape of code, a well-maintained README is a beacon of hope, guiding survivors (developers) through the rubble. This tool scans your README for common issues, ensuring it's always ready to inform and inspire.

## Features

*   **Section Scrutiny**: Checks for the presence of essential sections like "Installation", "Usage", "Contributing", and "License" (case-insensitive, header-style).
*   **Placeholder Purge**: Identifies common placeholder texts (e.g., "TODO", "FIXME", "YOUR_PROJECT_NAME", "PROJECT_DESCRIPTION") that indicate incomplete documentation.
*   **Link Linter**: Basic syntax check for Markdown links, catching empty URLs or URLs with spaces.

## Usage

To run the Revivalist, navigate to your project's root directory (where your `README.md` resides) and execute the `revivalist.py` script.

```bash
python utils/nightly-readme-revivalist/src/revivalist.py
```

The script will print a report to the console detailing any issues found.

### Example Output (if issues are found)

```
--- Missing Sections ---
- Missing or improperly formatted section: 'Installation'
- Missing or improperly formatted section: 'Usage'

--- Placeholders ---
- Found placeholder text: 'TODO'
- Found placeholder text: 'YOUR_PROJECT_NAME'

--- Link Syntax Issues ---
- Found a link with an empty URL: `[]()` or `![]()`

README revival report complete. Consider addressing the issues above.
```

### Example Output (if no issues are found)

```
README looks great! No revival needed.
```

## Development

The `revivalist.py` script is written in Python 3.11 and is self-contained. It uses standard library modules only.

### Running Tests

To run the automated tests, navigate to the `utils/nightly-readme-revivalist` directory and execute:

```bash
python -m unittest tests/test_revivalist.py
```

The tests use `unittest.mock` to simulate file system operations, ensuring they are deterministic and do not require actual file manipulation.
