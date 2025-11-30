# Nightly Resource Scavenger Log

## Overview

The `nightly-resource-scavenger-log` is a simple, whimsical-yet-useful command-line utility designed to help you track your daily 'scavenged resources' – be it completed tasks, new ideas, organized files, or any other valuable contributions. Inspired by the ApocalypsAI's spirit of diligent resource gathering, this tool logs your daily efforts into a human-readable Markdown file, providing a personal record of your progress.

## Features

*   **Add Entries**: Quickly log new 'scavenged resources' with a category and description.
*   **List Entries**: View all your logged entries, or filter them by date.
*   **Markdown Format**: Logs are stored in a simple, append-only Markdown file, making them easy to read and integrate with other tools.

## Installation

1.  Navigate to the `utils/nightly-resource-scavenger-log` directory.
2.  The utility is a standalone Python script. No special installation steps are required beyond having Python 3.11+ installed.

## Usage

Run the script directly from its `src` directory:

```bash
python src/scavenger_log.py <command> [arguments]
```

### Commands:

#### `add <category> <description>`

Adds a new entry to your scavenger log.

*   `<category>`: A short, descriptive tag for your resource (e.g., `code`, `docs`, `idea`, `bugfix`, `misc`).
*   `<description>`: A detailed description of the resource scavenged.

**Example:**

```bash
python src/scavenger_log.py add code "Refactored the agent_integrator to be more efficient."
python src/scavenger_log.py add idea "Brainstormed a new utility for tracking cosmic dust."
```

#### `list [--date YYYY-MM-DD]`

Lists all entries in your scavenger log. Optionally filter by a specific date.

*   `--date YYYY-MM-DD`: (Optional) Filters entries to show only those from the specified date.

**Examples:**

```bash
python src/scavenger_log.py list
python src/scavenger_log.py list --date 2023-10-27
```

## Log File Location

By default, the log file (`scavenger_log.md`) is created in the directory where the script is run. You can modify the `LOG_FILE` variable in `src/scavenger_log.py` to specify a different path, e.g., `os.path.expanduser('~/.apocalypsai/scavenger_log.md')` for a system-wide log.

## Development & Testing

To run the tests for this utility:

```bash
python -m unittest tests/test_scavenger_log.py
```

## License

This utility is released under the MIT License. See the main repository's `LICENSE` file for details.
