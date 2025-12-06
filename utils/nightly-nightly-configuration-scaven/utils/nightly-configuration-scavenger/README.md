# Nightly Configuration Scavenger

In the post-apocalyptic digital wasteland, configuration files often become fragmented, corrupted, or scattered across forgotten directories. The Nightly Configuration Scavenger is here to help! This utility diligently scours specified paths for common configuration formats (INI, YAML, JSON), parses their contents, and presents them in a structured report.

It's like a digital archaeologist, sifting through the rubble to reconstruct the lost blueprints of your systems.

## Features

*   **Multi-format Parsing**: Supports INI, YAML, and JSON configuration files.
*   **Directory Scanning**: Recursively scans specified directories for config files.
*   **Error Reporting**: Identifies and reports files that cannot be parsed.
*   **Structured Output**: Provides a clear, organized view of all discovered configurations.

## Usage

```bash
python src/scavenger.py --path /path/to/configs --extensions ini yaml json
```

### Arguments

*   `--path <directory>`: The root directory to start scavenging for configuration files.
*   `--extensions <ext1> <ext2> ...`: A space-separated list of file extensions to look for (e.g., `ini yaml json`).
*   `--output <file_path>`: (Optional) Path to save the JSON output. If not provided, prints to stdout.

## Example Output

```json
{
  "/path/to/configs/app.ini": {
    "section1": {
      "key1": "value1"
    }
  },
  "/path/to/configs/data/settings.yaml": {
    "database": {
      "host": "localhost",
      "port": 5432
    }
  },
  "/path/to/configs/invalid.json": {
    "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)"
  }
}
```

## Installation

This utility is self-contained and requires Python 3.11+.
It uses `configparser` (stdlib), `json` (stdlib), and `PyYAML`.
To install `PyYAML`:

```bash
pip install PyYAML
```

## Development

To run tests:

```bash
python -m pytest tests/test_scavenger.py
```
