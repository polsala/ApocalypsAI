# Shelter Sentry Log

A command-line utility for logging and reviewing sentry duty shifts and observations in a shared shelter. In the uncertain times of the ApocalypsAI, vigilance is paramount. This tool helps your community maintain a clear, auditable record of who was on watch, what they observed, and when, ensuring no anomaly goes unnoticed.

## Features

*   **Log Observations**: Quickly record a new sentry shift with the observer's name and their findings.
*   **Review History**: View all past sentry logs, ordered by timestamp.
*   **Filter by Sentry**: Easily check the observations made by a specific individual.
*   **Persistent Storage**: All logs are saved to a local JSON file, ensuring data survives reboots and power fluctuations.

## Installation

This utility is written in Python 3.11+ and uses only standard library modules. No external dependencies are required.

1.  Navigate to the `utils/shelter-sentry-log/` directory.
2.  You can run it directly using `python src/sentry_log.py`.

## Usage

The `sentry_log.py` script supports several commands:

*   `python src/sentry_log.py add <sentry_name> <observation_text>`: Adds a new log entry.
    *   `<sentry_name>`: The name of the individual on sentry duty (e.g., "Scout Alpha").
    *   `<observation_text>`: A description of what was observed (e.g., "Strange lights on the horizon", "All clear").
*   `python src/sentry_log.py view [--sentry <sentry_name>]`: Views log entries.
    *   If `--sentry <sentry_name>` is provided, only logs from that sentry will be shown.
    *   If no `--sentry` is provided, all logs will be displayed.
*   `python src/sentry_log.py clear`: **DANGER!** Clears all log entries. Use with extreme caution.

### Examples

```bash
# Add an observation
python src/sentry_log.py add "Scout Alpha" "Strange lights on the horizon, moving fast."

# Add another observation
python src/sentry_log.py add "Watcher Beta" "Perimeter fence intact. No unusual activity."

# View all logs
python src/sentry_log.py view

# View logs by a specific sentry
python src/sentry_log.py view --sentry "Scout Alpha"

# Clear all logs (use with caution!)
python src/sentry_log.py clear
```

## Data Storage

Logs are stored in `sentry_log.json` within the `utils/shelter-sentry-log/` directory. This file is automatically created if it doesn't exist.
