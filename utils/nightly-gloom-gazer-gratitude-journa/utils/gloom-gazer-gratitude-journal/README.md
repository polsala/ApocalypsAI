# Gloom-Gazer's Gratitude Journal

A simple command-line utility to log daily gratitude entries and receive a morale-boosting "silver lining" prompt. Because even in the darkest times, there's always something to appreciate.

## Features

*   **Add Entries**: Quickly log what you're grateful for with a timestamp.
*   **View Journal**: See all your past gratitude entries.
*   **Silver Lining Prompts**: Get a random prompt to help you find something positive.

## Usage

Navigate to the `src` directory and run the `journal.py` script with the desired command.

### Add a new gratitude entry

```bash
python src/journal.py add "Today I'm grateful for a working flashlight."
```

### View all entries

```bash
python src/journal.py view
```

### Get a silver lining prompt

```bash
python src/journal.py prompt
```

## Data Storage

Entries are stored in a plain text file named `journal.txt` within the `src` directory, alongside the `journal.py` script. This makes it easy to back up or inspect your journal directly.

## Installation

No special installation is required. Simply ensure you have Python 3.x installed. The utility is self-contained within its directory.

## Contributing

Feel free to suggest new prompts, features, or improvements!
