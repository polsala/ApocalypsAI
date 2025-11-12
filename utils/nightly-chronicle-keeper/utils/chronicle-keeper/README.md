# Chronicle Keeper: Your Personal Apocalyptic Journal

## Overview

The `chronicle-keeper` is a simple, self-contained command-line utility designed to help you log events and thoughts, automatically timestamping and categorizing them relative to a configurable 'Doom Date'. Whether you're documenting the slow decline of civilization or the glorious rebirth, this tool ensures your chronicles are properly filed.

## Features

*   **Add Entries**: Quickly log new events with an automatic timestamp.
*   **Doom Date Categorization**: Entries are automatically marked as `[PRE-APOCALYPSE]` or `[POST-APOCALYPSE]` based on your configured Doom Date.
*   **List Entries**: View all your chronicles, or filter them by category.
*   **Configure Doom Date**: Set or update the pivotal date that defines the shift from 'pre' to 'post'.

## Installation & Usage

This utility is written in Python 3.11 and requires no external dependencies beyond the standard library. Simply navigate to the `utils/chronicle-keeper/` directory.

### Files

*   `src/chronicle.py`: The main script.
*   `chronicle.log`: Stores all your journal entries.
*   `chronicle.config`: Stores your configured Doom Date.

### Commands

To run any command, execute `python src/chronicle.py <command> [arguments]` from the `utils/chronicle-keeper/` directory.

#### 1. `add <message>`: Add a new journal entry.

```bash
python src/chronicle.py add "Discovered a new species of glowing mushroom in the old supermarket."
python src/chronicle.py add "The sky turned a peculiar shade of green today. Probably fine."
```

#### 2. `list [category]`: List all entries, or filter by category.

*   `category` can be `pre` or `post`.

```bash
python src/chronicle.py list
python src/chronicle.py list pre
python src/chronicle.py list post
```

#### 3. `config [YYYY-MM-DD]`: Set or view the Doom Date.

*   If no date is provided, it will display the current Doom Date.
*   If a date is provided, it will set the new Doom Date.

```bash
python src/chronicle.py config 2025-12-31
python src/chronicle.py config
```

## Example Workflow

```bash
# Set the Doom Date
python src/chronicle.py config 2024-07-15

# Add a pre-apocalypse entry
python src/chronicle.py add "Still waiting for my Amazon package. Hope it arrives before the big one."

# (Imagine time passes, the Doom Date is now in the past)

# Add a post-apocalypse entry
python src/chronicle.py add "Found a working solar panel! Power for the radio is secured."

# List all entries
python src/chronicle.py list

# List only pre-apocalypse entries
python src/chronicle.py list pre
```

Your `chronicle.log` will then contain entries like:

```
[2024-07-10 10:00:00] [PRE-APOCALYPSE] Still waiting for my Amazon package. Hope it arrives before the big one.
[2024-07-16 14:30:00] [POST-APOCALYPSE] Found a working solar panel! Power for the radio is secured.
```
