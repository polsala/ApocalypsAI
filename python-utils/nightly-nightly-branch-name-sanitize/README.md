# Nightly Branch Name Sanitizer

A utility to sanitize Git branch names to ensure they are safe for CI/CD pipelines and file systems.

## Features

- Removes or replaces unsafe characters
- Ensures branch names are valid for Git and common CI/CD systems
- Provides a dry-run mode for testing
- Supports custom sanitization rules

## Usage

```bash
python src/sanitizer.py --branch "feature/unsafe#branch@name" --output sanitized_branch.txt
```

## Installation

No installation required. Just run the script with Python 3.11+.

## License

MIT
