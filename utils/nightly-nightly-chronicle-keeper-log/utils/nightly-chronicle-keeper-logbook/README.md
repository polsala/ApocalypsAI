# Chronicle-Keeper Logbook

## Description

The `Chronicle-Keeper Logbook` is a simple, yet essential, command-line utility designed for survivors of the apocalypse (or anyone needing a quick logging tool). It allows you to swiftly add timestamped entries to a daily log file, helping you document your journey, observations, and critical events without fuss.

Keep track of your scavenged goods, encountered anomalies, or simply your daily thoughts as you navigate the new world.

## Features

*   **Timestamped Entries**: Every log entry is automatically prefixed with a precise `[YYYY-MM-DD HH:MM:SS]` timestamp.
*   **Configurable Output**: Easily specify the path to your chronicle log file. Defaults to `logs/chronicle.log`.
*   **Automatic Directory Creation**: If the specified log file's directory doesn't exist, the utility will create it for you.
*   **Self-Contained**: Written in Python, requiring no external dependencies beyond the standard library.

## Usage

To add an entry to your chronicle, simply navigate to the `nightly-chronicle-keeper-logbook` directory and run the `logbook.py` script with your message:

```bash
python src/logbook.py "Found a stash of canned peaches near the old supermarket. Good haul!"
```

This will append an entry like this to `logs/chronicle.log` (creating the file and directory if they don't exist):

```
[2023-10-27 10:30:00] Found a stash of canned peaches near the old supermarket. Good haul!
```

### Custom Output File

You can specify a different output file using the `--output` or `-o` flag:

```bash
python src/logbook.py -o my_personal_journal.txt "Encountered a pack of wild dogs today. Managed to scare them off."
```

This will write the entry to `my_personal_journal.txt` in the current directory (or a specified path).

### Help

For more information on arguments:

```bash
python src/logbook.py --help
```

## Installation

No special installation is required. Ensure you have Python 3.6+ installed. The utility is self-contained within its `src/` directory.

## Development & Testing

To run the automated tests, navigate to the `utils/nightly-chronicle-keeper-logbook/` directory and execute:

```bash
python -m unittest tests/test_logbook.py
```

All tests are deterministic and use mocks to ensure they run offline without side effects.
