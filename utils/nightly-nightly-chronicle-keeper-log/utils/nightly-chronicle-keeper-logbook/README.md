# Nightly Chronicle Keeper Logbook

A command-line utility for the discerning survivor, the ApocalypsAI Chronicle Keeper Logbook helps you record your daily observations, thoughts, and crucial findings in a post-apocalyptic world. Or, you know, just keep a dev journal.

It's designed to be simple, fast, and self-contained, ensuring your chronicles are safe even when the world isn't.

## Features

*   **Timestamped Entries**: Every entry is automatically stamped with the time it was recorded.
*   **Daily Logs**: Entries are organized into daily log files (e.g., `logs/YYYY-MM-DD.log`).
*   **Easy Viewing**: Quickly view today's entries, entries from a specific date, or the last N entries.
*   **Self-Contained**: Written in Python, with minimal dependencies, making it easy to run anywhere.

## Installation

This utility is self-contained. Simply navigate to the `utils/nightly-chronicle-keeper-logbook/` directory.

## Usage

The `chronicle.py` script is your gateway to documenting the future (or past).

### Add an Entry

To add a new entry to today's log:

```bash
python src/chronicle.py add "Discovered a new species of glowing fungi near the old power plant."
```

Example output:
```
Entry added to logs/2023-10-27.log
```

### View Entries

To view all entries for today:

```bash
python src/chronicle.py view
```

Example output:
```
--- Log for 2023-10-27 ---
[08:15:00] Repaired the perimeter fence.
[14:30:00] Discovered a new species of glowing fungi near the old power plant.
-----------------------------------
```

To view entries for a specific date (YYYY-MM-DD):

```bash
python src/chronicle.py view --date 2023-10-26
```

To view only the last N entries from today (or a specified date):

```bash
python src/chronicle.py view --last 3
python src/chronicle.py view --date 2023-10-25 --last 5
```

If no entries are found for the specified date, it will inform you:
```
No log entries found for 2023-10-26.
```

## Development & Testing

The utility is written in Python 3.11.

To run tests:

```bash
python -m unittest tests/test_chronicle.py
```

All tests are deterministic and use `unittest.mock` to prevent actual file system interactions or reliance on the current date/time.
