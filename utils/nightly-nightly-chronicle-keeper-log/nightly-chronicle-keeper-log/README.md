# Nightly Chronicle Keeper's Log

A simple, command-line utility for the ApocalypsAI community to keep a personal, timestamped log of daily events, observations, or thoughts. In the chaotic post-apocalyptic world, every piece of information is valuable. Use this tool to record your chronicles, track resources, or simply document the strange occurrences of the wasteland.

## Features

*   **Timestamped Entries**: Every log entry is automatically prefixed with the current date and time.
*   **Simple Appending**: Easily add new observations to your personal chronicle file.
*   **View Recent Entries**: Quickly review the last few entries to catch up on your saga.
*   **Custom Log File**: Option to specify a different log file if you're keeping multiple chronicles.

## Usage

This utility is written in Python 3.11 and can be run directly from the command line.

### Add a new entry

To add a new entry to your chronicle:

```bash
python src/chronicle_log.py --add "Discovered a new species of glowing fungi near Sector 7."
```

Or, using the shorthand:

```bash
python src/chronicle_log.py -a "The automated defense turrets are still operational, surprisingly."
```

By default, entries are saved to `chronicle.log` in the current directory.

### View recent entries

To view the last 5 entries (default):

```bash
python src/chronicle_log.py --view
```

To view a specific number of entries (e.g., the last 10):

```bash
python src/chronicle_log.py --view 10
```

Or, using the shorthand:

```bash
python src/chronicle_log.py -v 3
```

### Using a custom log file

You can specify a different log file for both adding and viewing entries using the `--log-file` argument:

```bash
python src/chronicle_log.py -a "Found a stash of pre-war comic books." --log-file "loot_log.txt"
python src/chronicle_log.py -v 5 --log-file "loot_log.txt"
```

## Development & Testing

The utility is self-contained and requires Python 3.11.

To run the tests:

```bash
python -m unittest tests/test_chronicle_log.py
```

All tests are deterministic and use `unittest.mock` to simulate file system operations and time, ensuring consistent results without actual file I/O.
