# Nightly Gloom-Gazer Gratitude Journal

## Overview
Even when the world is a smoldering ruin, there's always something to be grateful for. The `Nightly Gloom-Gazer Gratitude Journal` is a simple, self-contained command-line utility designed to help you record and review your daily moments of gratitude. It's a small beacon of positivity in the post-apocalyptic gloom.

## Features
*   **Add Entries**: Quickly log a new gratitude entry with an automatic timestamp.
*   **View All**: See all your past gratitude entries.
*   **Search**: Find specific entries using keywords.
*   **Self-Contained**: Stores all data in a simple text file (`gratitude_log.txt`) within its directory, making it easy to manage and backup.

## Usage
This utility requires Python 3.11+.

1.  **Navigate**: Change into the `utils/nightly-gloom-gazer-gratitude-journal/` directory.
2.  **Run**: Execute the `journal.py` script with the desired command.

### Add a new gratitude entry
```bash
python src/journal.py add "Found a perfectly intact can of beans today!"
```

### View all entries
```bash
python src/journal.py view
```

### Search for entries
```bash
python src/journal.py search beans
```

## Installation
No special installation steps or external dependencies are required beyond a standard Python 3.11+ environment. Just place the `nightly-gloom-gazer-gratitude-journal` folder in your `utils/` directory, and you're ready to start logging your gratitude.
