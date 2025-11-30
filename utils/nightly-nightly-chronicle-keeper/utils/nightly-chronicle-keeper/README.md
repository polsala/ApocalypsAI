# Nightly Chronicle Keeper

A simple command-line utility to help you keep a daily log of your thoughts, tasks, or observations. In the post-apocalyptic world, keeping track of your daily chronicles is crucial for survival and sanity. This tool ensures your entries are timestamped and organized into daily log files.

## Features

*   **Daily Logs**: Automatically creates or appends to a log file for the current day (`YYYY-MM-DD_chronicle.log`).
*   **Timestamped Entries**: Each entry is prefixed with the exact time it was recorded.
*   **Simple CLI**: Easy to use from your terminal.

## Installation

This utility is self-contained and requires Python 3.8+ (tested with 3.11).

1.  Navigate to the `utils/nightly-chronicle-keeper/` directory.
2.  You can run it directly using `python src/chronicle_keeper.py`.

## Usage

To add an entry to your daily chronicle:

```bash
python src/chronicle_keeper.py "Your chronicle entry goes here."
```

The log files will be created in a `logs/` subdirectory within the directory where you run the script.

### Examples

```bash
# Record a daily observation
python src/chronicle_keeper.py "Found a new stash of canned beans near the old library. Marked coordinates on map."

# Log a task completed
python src/chronicle_keeper.py "Repaired the water purifier. Output flow rate is stable."

# Jot down a thought
python src/chronicle_keeper.py "The silence tonight is unnerving. Wonder if the scavengers are out."
```

## Development

The source code is in `src/chronicle_keeper.py` and tests are in `tests/test_chronicle_keeper.py`.
