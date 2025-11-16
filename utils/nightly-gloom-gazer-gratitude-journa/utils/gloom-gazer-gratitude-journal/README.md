# Gloom-Gazer's Gratitude Journal

## Overview
Even when the world is a smoldering ruin, there's always something to be grateful for! The Gloom-Gazer's Gratitude Journal is a simple command-line utility designed to help you log and review your daily moments of appreciation. Keep your spirits up, one grateful thought at a time.

## Features
*   **Add Entries**: Quickly log a new gratitude entry with an automatic timestamp.
*   **View All Entries**: See your entire history of grateful thoughts.
*   **View By Date**: Filter entries to see what you were grateful for on a specific day.

## Installation
This utility is self-contained and requires Python 3.11+. No external dependencies are needed beyond the standard library.

1.  Navigate to the `gloom-gazer-gratitude-journal` directory.
2.  Run the script directly.

## Usage

### Add a new gratitude entry
```bash
python src/journal.py add "I'm grateful for the last working flashlight."
```

### View all entries
```bash
python src/journal.py view
```

### View entries for a specific date
```bash
python src/journal.py view --date 2024-07-26
```

### Help
```bash
python src/journal.py --help
```

## Journal File Location
Entries are stored in `data/journal.txt` within the utility's directory.
