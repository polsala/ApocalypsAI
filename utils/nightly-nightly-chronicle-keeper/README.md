# Nightly Chronicle Keeper

A whimsical-yet-useful command-line utility for the ApocalypsAI community to log timestamped entries into a Markdown file. Whether you're tracking daily progress, documenting observations, or simply noting down "apocalyptic" events, the Chronicle Keeper ensures your records are organized and easily reviewable.

## Features

*   **Timestamped Entries**: Each log entry is automatically prefixed with a precise date and time.
*   **Markdown Format**: Logs are stored in a human-readable Markdown format, making them easy to view and integrate with other tools.
*   **Customizable Log File**: Specify the log file path, or use the default `chronicle.md`.
*   **Simple CLI**: Quick and easy to use from your terminal.

## Installation

This utility is self-contained. You can run it directly using Python 3.11+.

1.  Navigate to the `utils/nightly-chronicle-keeper` directory.
2.  Ensure you have Python 3.11 or newer installed.

## Usage

To add an entry to your chronicle:

```bash
python src/chronicle_keeper.py "Your log message here."
```

This will append an entry to `chronicle.md` in the current directory, like so:

```markdown
## YYYY-MM-DD HH:MM:SS
- Your log message here.
```

### Custom Log File

You can specify a different log file using the `--file` argument:

```bash
python src/chronicle_keeper.py "Found a rare artifact." --file my_personal_journal.md
```

Or even a file in a subdirectory:

```bash
python src/chronicle_keeper.py "Patrol route clear." --file logs/daily_reports.md
```

The utility will automatically create the specified file and any necessary parent directories if they don't exist.

## Development & Testing

To run the tests for this utility:

1.  Navigate to the `utils/nightly-chronicle-keeper` directory.
2.  Run the tests using `unittest`:

    ```bash
    python -m unittest tests/test_chronicle_keeper.py
    ```

The tests are designed to be deterministic and do not interact with the filesystem, using mocks for file operations and time.
