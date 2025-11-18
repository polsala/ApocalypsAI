# Nightly Morale Monitor

In the ever-challenging world of ApocalypsAI, maintaining optimal operational efficiency isn't just about code; it's about core well-being. The **Nightly Morale Monitor** is a simple, self-contained utility designed to help agents and human survivors track their daily mood and reflect on their emotional state.

Even amidst the rubble and rogue AI, a little self-care goes a long way. Log your morale, review your trends, and ensure your internal processors (or organic brains) are running smoothly.

## Features

*   **Log Daily Morale**: Record your mood on a scale of 1 (dreadful) to 5 (exhilarated), with an optional note.
*   **View History**: See all your past morale entries.
*   **Get Summary**: Obtain an average morale score and distribution of moods over time.
*   **Self-Contained**: Stores data locally in a JSON file, no external dependencies (beyond Python standard library).

## Installation

This utility is self-contained. Simply ensure you have Python 3.8+ installed.

## Usage

All commands are run via the `morale_monitor.py` script.

### 1. Add a Morale Entry

Record your current mood. The `--mood` argument is required (1-5), and `--note` is optional.

```bash
python src/morale_monitor.py add --mood 4 --note "Successfully integrated a new utility! Feeling productive."
python src/morale_monitor.py add --mood 2 --note "Another server farm went offline. Sigh."
```

### 2. View All Entries

See a chronological list of all your logged morale entries.

```bash
python src/morale_monitor.py view
```

### 3. Get Morale Summary

Receive an overview of your morale, including the average score and the count of each mood level.

```bash
python src/morale_monitor.py summary
```

## Data Storage

Morale entries are stored in a JSON file named `morale_data.json` in the same directory as `morale_monitor.py`. This file is automatically created if it doesn't exist.

## Contributing

While this utility is primarily for personal use, suggestions for improvements are always welcome. Just remember the ApocalypsAI philosophy: "Anarchy with discipline."
