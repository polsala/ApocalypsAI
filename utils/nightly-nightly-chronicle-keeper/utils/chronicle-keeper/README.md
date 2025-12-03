# Nightly Chronicle Keeper

## Overview

The Nightly Chronicle Keeper is a simple, yet essential, utility for documenting your daily findings, thoughts, and progress in the ever-unfolding post-apocalyptic narrative. Whether you're tracking resource caches, noting down strange anomalies, or simply journaling your survival journey, this tool ensures your chronicles are timestamped and neatly organized in a markdown logbook.

It's designed to be a quick, command-line way to add entries to a persistent log file, making it easy to review your history and plan for the future.

## Features

*   **Timestamped Entries**: Every entry is automatically prefixed with the current date and time, ensuring a clear chronological record.
*   **Markdown Format**: Logs are stored in a simple Markdown format, making them easy to read, edit, and integrate with other tools.
*   **Append-Only**: New entries are always appended to the existing logbook, preserving your history.
*   **Custom Logbook Name**: Specify a different log file if you wish to maintain multiple chronicles (e.g., `survival.md`, `research.md`).

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed beyond the standard library.

1.  Navigate to the `utils/nightly-chronicle-keeper/` directory.
2.  The main script is `utils/chronicle-keeper/src/chronicle_keeper.py`.

## Usage

To add an entry to your default logbook (`logbook.md`):

```bash
python utils/chronicle-keeper/src/chronicle_keeper.py "Discovered a new source of clean water near the old bridge. Marked coordinates on the map."
```

To add an entry to a custom logbook file:

```bash
python utils/chronicle-keeper/src/chronicle_keeper.py --file research_notes.md "Observed unusual bioluminescence in the abandoned subway tunnels. Requires further investigation."
```

The logbook file will be created in the current directory (where you run the script from) if it doesn't already exist.

## Example `logbook.md` content

```markdown
## 2024-07-20 10:30:00

Found a shiny new wrench.

---

## 2024-07-21 11:00:00

Repaired the water purifier.

---

## 2024-07-22 09:15:00

Custom log entry.

---
```

## Development & Testing

To run the tests for this utility:

```bash
python -m unittest utils/chronicle-keeper/tests/test_chronicle_keeper.py
```

All tests are deterministic and offline, using Python's `unittest.mock` to simulate file system operations and control time.
