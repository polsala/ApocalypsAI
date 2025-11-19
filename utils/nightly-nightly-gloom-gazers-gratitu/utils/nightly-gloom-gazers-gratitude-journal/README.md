# Nightly Gloom-Gazer's Gratitude Journal

Even when the world is crumbling, there's always a glimmer of something to be grateful for. The "Gloom-Gazer's Gratitude Journal" is a simple command-line utility designed to help you log those small, precious moments of appreciation. Keep your spirits up, one grateful thought at a time.

## Features

*   **Quick Logging**: Easily add new gratitude entries with a timestamp.
*   **Daily Files**: Entries are automatically organized into daily log files for easy review.
*   **View Entries**: Read back your past moments of gratitude.

## Installation

This utility is self-contained and requires Python 3.8+ (or compatible).

1.  Navigate to the utility's directory:
    ```bash
    cd utils/nightly-gloom-gazers-gratitude-journal
    ```
2.  (Optional, but recommended) Create a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

## Usage

All commands are run via `python3 src/journal.py`.

### Add a new gratitude entry

```bash
python3 src/journal.py add "Found a perfectly intact can of peaches today!"
```
or
```bash
python3 src/journal.py add "The sunset was surprisingly beautiful through the smog."
```

### View entries for today

```bash
python3 src/journal.py view
```

### View entries for a specific date

Specify the date in `YYYY-MM-DD` format.

```bash
python3 src/journal.py view 2077-10-23
```

### View all entries (concatenated)

```bash
python3 src/journal.py view --all
```

## Project Structure

```
.
├── README.md
├── src/
│   └── journal.py
└── tests/
    └── test_journal.py
```
