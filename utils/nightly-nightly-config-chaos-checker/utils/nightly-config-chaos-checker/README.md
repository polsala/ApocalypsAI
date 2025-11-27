# Nightly Config Chaos Checker

## Overview

The Nightly Config Chaos Checker is a whimsical-yet-useful utility designed to bring order to the often chaotic world of configuration files. It scans specified directories for common configuration file types (`.env`, `.ini`) and identifies potential 'chaos points' such as sensitive data exposure, empty critical values, and duplicate keys. By proactively flagging these issues, it helps prevent unexpected behavior, security vulnerabilities, and deployment headaches.

Think of it as your personal digital librarian, ensuring that every configuration scroll is properly cataloged and free from dangerous scribbles.

## Features

- **Sensitive Data Exposure Detection**: Identifies patterns indicative of hardcoded secrets (e.g., `API_KEY=`, `PASSWORD=`) in plain text.
- **Empty Critical Value Check**: Flags configuration keys that are often essential but have been left empty.
- **Duplicate Key Detection**: Warns about keys defined multiple times within the same configuration file, which can lead to unpredictable behavior.
- **Multi-format Support**: Currently supports `.env` and `.ini` file formats.

## Usage

```bash
python src/checker.py --path /path/to/your/project/configs
```

### Arguments

- `--path <directory>`: The root directory to start scanning for configuration files. (Required)

## Example Output

```
Scanning for config chaos in: /path/to/your/project/configs

--- Chaos Report ---

File: /path/to/your/project/configs/.env
  [CRITICAL] Sensitive data detected for 'API_KEY'. Consider using environment variables or a secret management system.
  [WARNING] Empty value for 'DATABASE_URL'. This might cause connection issues.

File: /path/to/your/project/configs/app.ini
  [WARNING] Duplicate key 'debug_mode' found. The last definition will likely be used, but this indicates a potential error.

No chaos detected in /path/to/another/dir/config.ini

--- Scan Complete ---
```

## Development

### Running Tests

```bash
python -m unittest tests/test_checker.py
```
