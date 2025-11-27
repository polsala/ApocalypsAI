# Nightly Morale Monitor

## Overview

The Nightly Morale Monitor is a whimsical utility designed to gauge the collective spirits of your post-apocalyptic community. Simply log daily events in a text file, and this tool will process them to calculate a 'morale score' and provide a lighthearted report on the community's overall well-being.

It's perfect for when you need a quick, albeit slightly sarcastic, pulse check on whether your fellow survivors are thriving, surviving, or just barely tolerating each other.

## How it Works

1.  **Log Events**: Create a file (default `daily_events.txt`) where each line describes a significant event that happened in your community. These events can be positive (e.g., "found a working toaster", "shared a can of mystery meat") or negative (e.g., "ran out of irradiated coffee beans", "lost my favorite spork").
2.  **Calculate Morale**: The utility scans these events for keywords (e.g., "found", "lost", "fixed", "argued") and assigns a predefined morale impact score to each. These scores are summed up to get a total morale score.
3.  **Generate Report**: Based on the total morale score, a whimsical report is generated, offering a status update and a bit of post-apocalyptic wisdom.

## Usage

1.  **Create `daily_events.txt`** (or any `.txt` file) in the same directory as `morale_monitor.py`.
    Each line should be a single event:
    ```
    found a working toaster
    shared a can of mystery meat
    argued about who gets the last battery
    fixed the rusty water purifier
    ran out of irradiated coffee beans
    saw a particularly fluffy dust bunny
    ```
2.  **Run the script**:
    ```bash
    python src/morale_monitor.py
    ```
    Optionally, specify a different events file:
    ```bash
    python src/morale_monitor.py --events my_custom_events.txt
    ```

## Example Output

```
--- Nightly Morale Report ---

Morale: Optimistic Glow. Things are looking up! A few more wins and we'll be practically skipping through the rubble.

Total Morale Score: 6

-----------------------------
```

## Development

This utility is written in Python 3.11 and is self-contained. No external dependencies are required beyond the standard library.

To run tests:

```bash
python -m unittest tests/test_morale_monitor.py
```
