# Nightly Survival Kit Checker

## Overview

The `nightly-survival-kit-checker` is a whimsical-yet-useful utility designed to help maintain the health and readiness of your repository. It scans a specified directory for a set of 'essential' files (e.g., `README.md`, `LICENSE`, `.gitignore`, `pyproject.toml`, `requirements.txt`) and reports on their presence or absence. Think of it as your personal apocalypse prepper, ensuring your project has all the basics covered before the digital dust settles.

## Features

*   **Essential File Scan**: Checks for critical files that every well-maintained repository should have.
*   **Readiness Score**: Provides a simple percentage score indicating how 'ready' your directory is.
*   **Missing File Report**: Clearly lists any essential files that are absent.

## Usage

```bash
python src/checker.py --path /path/to/your/repository
```

### Arguments

*   `--path <directory>`: The absolute or relative path to the directory you want to check. (Required)

## Example Output

```json
{
  "directory": "/path/to/your/repository",
  "essential_files_checked": [
    "README.md",
    "LICENSE",
    ".gitignore",
    "pyproject.toml",
    "requirements.txt"
  ],
  "files_found": [
    "README.md",
    "LICENSE"
  ],
  "files_missing": [
    ".gitignore",
    "pyproject.toml",
    "requirements.txt"
  ],
  "survival_readiness_score": 40.0,
  "status": "WARNING",
  "message": "Some essential files are missing. Improve your survival readiness!"
}
```

## Development

This utility is written in Python 3.11 and is self-contained. It uses standard library modules only.

## Testing

To run the tests, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_checker.py
```
