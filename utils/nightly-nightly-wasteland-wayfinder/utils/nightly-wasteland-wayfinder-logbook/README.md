# Nightly Wasteland Wayfinder Logbook

## Overview

The Nightly Wasteland Wayfinder Logbook is a simple command-line utility designed to help survivors document their daily journeys, discoveries, and encounters in the post-apocalyptic world. It appends timestamped entries to a markdown-formatted log file, creating a chronological record of your adventures.

Keep track of where you've been, what you've found, and who (or what) you've met, ensuring no crucial detail is lost to the sands of time (or radiation).

## Features

*   **Timestamped Entries**: Every log entry is automatically prepended with the current date and time.
*   **Markdown Format**: Logs are saved in a simple Markdown format, making them easy to read and integrate with other tools.
*   **Append-Only**: New entries are always added to the end of the log file, preserving history.
*   **View Log**: Easily display the entire logbook content directly in your terminal.

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed beyond the standard library.

1.  Navigate to the `utils/nightly-wasteland-wayfinder-logbook` directory.
2.  Run the script directly.

## Usage

```bash
python src/logbook.py --help
```

### Adding an Entry

To add a new entry to your logbook:

```bash
python src/logbook.py add "Discovered an abandoned bunker. Looks promising, but the door is jammed."
```

By default, the logbook is saved as `wasteland_log.md` in the current directory. You can specify a different log file:

```bash
python src/logbook.py add "Found a pristine can of pre-war beans!" --file my_expedition.md
```

### Viewing the Logbook

To view the entire contents of your logbook:

```bash
python src/logbook.py view
```

Or with a specific file:

```bash
python src/logbook.py view --file my_expedition.md
```

## Examples

```bash
# Add a new entry about a scavenging run
python src/logbook.py add "Scavenged Sector 7. Found some scrap metal and a half-eaten bag of chips. No signs of hostiles."

# Add another entry about a strange encounter
python src/logbook.py add "Heard strange whispers near the old radio tower. Decided to avoid for now."

# View the logbook
python src/logbook.py view
```

This will output something like:

```
# Wasteland Logbook

## 2023-10-27 14:35:01
Scavenged Sector 7. Found some scrap metal and a half-eaten bag of chips. No signs of hostiles.

## 2023-10-27 14:40:15
Heard strange whispers near the old radio tower. Decided to avoid for now.
```
