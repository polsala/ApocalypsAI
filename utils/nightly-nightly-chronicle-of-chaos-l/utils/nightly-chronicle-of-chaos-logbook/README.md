# Nightly Chronicle of Chaos Logbook

## Overview

The `nightly-chronicle-of-chaos-logbook` is a minimalist command-line utility designed to help survivors of the apocalypse (or just busy individuals) keep a simple, timestamped log of their daily activities, observations, and thoughts. In a world of chaos, maintaining a record can be crucial for mental well-being, tracking resources, or simply remembering what happened yesterday.

It's a self-contained Python script that stores entries in a plain text file, making it robust and easy to manage even with limited resources.

## Features

*   **Add Entry**: Quickly append a new, timestamped entry to your personal chronicle.
*   **View Entries**: Display all past entries from your logbook.
*   **Simple Storage**: Uses a plain text file (`chronicle.log`) for maximum compatibility and ease of backup.

## Installation (No Installation Required!)

This utility is a single Python script. Simply place `logbook.py` in a directory of your choice.

## Usage

Navigate to the directory containing `logbook.py` in your terminal.

### Add a new entry

To add an entry, use the `add` command followed by your message:

```bash
python src/logbook.py add "Found a can of beans near the old supermarket. Morale: +1."
```

### View all entries

To view your entire chronicle, use the `view` command:

```bash
python src/logbook.py view
```

### Example Output (View)

```
[2024-07-20 14:30:00] Found a can of beans near the old supermarket. Morale: +1.
[2024-07-20 18:15:22] Repaired the leaky roof in the shelter. It's holding for now.
[2024-07-21 09:05:10] Heard strange noises from the east. Will investigate tomorrow.
```

## Development

The utility is written in Python 3.x. It uses standard library modules only, ensuring minimal dependencies.

### Running Tests

To run the automated tests, navigate to the `tests/` directory and execute:

```bash
python -m unittest test_logbook.py
```
