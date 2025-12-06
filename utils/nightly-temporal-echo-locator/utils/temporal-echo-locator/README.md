# Temporal Echo Locator

## 🌌 Purpose

The Temporal Echo Locator is a whimsical-yet-useful utility designed to help maintain code quality and prevent technical debt from accumulating. It scans your repository's files for common 'echoes' of forgotten tasks, temporary solutions, or areas needing attention. Think of it as a digital archaeologist, unearthing the whispers of past intentions.

It specifically looks for keywords like `TODO`, `FIXME`, `HACK`, and `BUG` (case-insensitive) within specified file types, providing a clear, actionable report of where these echoes reside.

## 🚀 Usage

To run the Temporal Echo Locator, navigate to the `utils/temporal-echo-locator` directory and execute the `echo_locator.py` script. It accepts optional arguments to customize the scan.

```bash
python src/echo_locator.py [directory] [--keywords K1 K2 ...] [--extensions .ext1 .ext2 ...]
```

### Arguments:

*   `directory` (optional): The root directory to scan. Defaults to the current directory (`.`).
*   `--keywords` (optional): A space-separated list of keywords to search for. Defaults to `TODO FIXME HACK BUG`.
*   `--extensions` (optional): A space-separated list of file extensions to include in the scan. Defaults to common code and text file extensions (e.g., `.py`, `.js`, `.md`, `.txt`).

### Example:

Scan the entire repository for `TODO` and `DEPRECATED` comments in Python and Markdown files:

```bash
python src/echo_locator.py ../.. --keywords TODO DEPRECATED --extensions .py .md
```

## 📊 Output

The utility outputs a JSON array, where each object represents an 'echo' found. Each echo includes:

*   `file_path`: The path to the file where the echo was found.
*   `line_number`: The line number within the file.
*   `line_content`: The full content of the line where the echo was detected (trimmed).
*   `keyword`: The specific keyword that was matched.

### Example JSON Output:

```json
[
  {
    "file_path": "./src/main.py",
    "line_number": 15,
    "line_content": "# TODO: Implement error handling for API calls",
    "keyword": "TODO"
  },
  {
    "file_path": "./docs/CONTRIBUTING.md",
    "line_number": 42,
    "line_content": "*   FIXME: Update this section with new guidelines",
    "keyword": "FIXME"
  }
]
```

## 🛠️ Development

The Temporal Echo Locator is written in Python 3.11 and uses only standard library modules, making it highly portable and self-contained.

### Running Tests

To ensure the locator is functioning correctly and its echoes are truly temporal, run the provided unit tests:

```bash
python -m unittest tests/test_echo_locator.py
```
