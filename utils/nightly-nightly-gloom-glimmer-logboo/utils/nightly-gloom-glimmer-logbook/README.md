# Nightly Gloom-Glimmer Logbook

## Purpose

In the desolate quiet of the post-apocalypse, it's easy to lose track of time, events, and most importantly, hope. The **Gloom-Glimmer Logbook** is a simple command-line utility designed to help survivors record their daily experiences, challenges ("gloom"), and any small moments of joy or progress ("glimmers"). It's a digital journal to preserve sanity and track the slow march of time.

## Features

*   **Daily Logging**: Easily add new entries with a date, your main observations, and a specific "glimmer" of hope or success.
*   **View History**: Review all your past entries to reflect on your journey.
*   **Self-Contained**: Stores all data in a local JSON file, no internet required.

## Installation

This utility is written in Python 3.11 and requires no external dependencies beyond the standard library.

1.  Navigate to the `utils/nightly-gloom-glimmer-logbook/` directory.
2.  You can run it directly using `python src/logbook.py`.

## Usage

The logbook operates via command-line arguments.

### Add a new entry

To add a new log entry, use the `add` command:

```bash
python src/logbook.py add "Today I found a working flashlight, but the generator is still broken." "The flashlight has new batteries! A small victory."
```

*   The first argument is your main log entry (the "gloom" or general observation).
*   The second argument is your "glimmer" – a positive observation, a small win, or a moment of hope.

### View all entries

To view all recorded entries, use the `view` command:

```bash
python src/logbook.py view
```

This will print all entries from your logbook, ordered by date.

## Example Output (view command)

```
--- Log Entry: 2024-07-20 ---
Gloom: Today I found a working flashlight, but the generator is still broken.
Glimmer: The flashlight has new batteries! A small victory.
-----------------------------
--- Log Entry: 2024-07-21 ---
Gloom: Spent the day fortifying the shelter. Found some rusty tools.
Glimmer: Managed to fix the loose hinge on the main door. It's safer now.
-----------------------------
```

## Data Storage

Entries are stored in `logbook.json` within the same directory as `src/logbook.py`. This file is automatically created if it doesn't exist.
