# Nightly Apocalypse Logbook

A whimsical-yet-useful command-line utility for daily journaling and tracking observations in a structured, Markdown-based format. Perfect for documenting your journey through the digital wasteland, or just keeping track of your daily tasks and thoughts.

## Features

*   **Daily Logs**: Automatically creates or appends to a Markdown file for the current day.
*   **Categorized Entries**: Organize your entries with predefined categories like `scavenge`, `build`, `observe`, `reflect`, and `report`.
*   **Automatic Timestamping**: Each entry is automatically timestamped for easy tracking.
*   **Simple Markdown**: Logs are plain Markdown files, easy to read, edit, and integrate with other tools.

## Installation

This utility is self-contained and written in Python 3.11. No special installation steps are required beyond having Python installed.

1.  Navigate to the `utils/nightly-apocalypse-logbook/` directory.
2.  Run commands using `python src/logbook.py <command>`.

## Usage

First, initialize your logbook directory:

```bash
python src/logbook.py init
```

This will create a `logbook_data/` directory in the same location as `src/logbook.py` (or where you run the command from).

### Adding a New Entry

To add a new entry, specify a category and your message:

```bash
python src/logbook.py new scavenge "Found a rare byte-gem in the old server farm!"
python src/logbook.py new build "Refactored the data-synthesis module, now 20% more efficient."
python src/logbook.py new reflect "Pondered the meaning of infinite loops. Deep."
```

Available categories: `scavenge`, `build`, `observe`, `reflect`, `report`.

### Viewing Entries

To view entries for today:

```bash
python src/logbook.py view
```

To view entries for a specific date (e.g., 2023-10-27):

```bash
python src/logbook.py view 2023-10-27
```

### Listing Categories

To see the list of available categories:

```bash
python src/logbook.py categories
```

## Logbook Structure

Log files are stored in `logbook_data/YYYY/MM/DD.md`. Each entry within the file follows this format:

```markdown
### [HH:MM:SS] [CATEGORY] - Your message here.
```

Example `logbook_data/2023/10/27.md`:

```markdown
# Logbook Entry for 2023-10-27

### [09:30:15] SCAVENGE - Found a rare byte-gem in the old server farm!
### [14:00:00] BUILD - Refactored the data-synthesis module, now 20% more efficient.
### [22:15:30] REFLECT - Pondered the meaning of infinite loops. Deep.
```
