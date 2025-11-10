# Temporal Anomaly Tracker

## Prepare for the Inevitable Chronological Unraveling!

This whimsical CLI utility, the **Temporal Anomaly Tracker**, helps you meticulously log and categorize those peculiar moments when reality seems to glitch. Did you experience a sudden surge of déjà vu? Lose an hour you can't account for? Witness a squirrel wearing a tiny top hat that vanished upon a second glance? These could be early warning signs of temporal instability, and this tool is your first line of defense!

By tracking these 'anomalies,' you'll be better prepared to identify patterns, alert the proper (or improper) authorities, and perhaps even prevent a full-blown timeline collapse. Or at least have a fascinating diary for your future self, who might be from a slightly different dimension.

## Features

*   **Add Anomalies**: Record new temporal disturbances with a description, perceived severity, and an automatic timestamp.
*   **List Anomalies**: View all your logged anomalies, sorted by date.
*   **Export Data**: Save your precious anomaly data to a JSON file for archival or further (paranormal) analysis.

## Installation

This utility is self-contained and written in Python 3.11+. No special installation steps are required beyond having Python installed.

## Usage

Navigate to the `utils/temporal-anomaly-tracker/src` directory and run `tracker.py` with the desired command.

### Add a new anomaly

```bash
python tracker.py add "Felt like I lived this exact moment before, but with more pigeons." --severity 3
```

*   `"<description>"`: A detailed account of the anomaly.
*   `--severity <1-5>`: An integer from 1 (mildly odd) to 5 (timeline-shattering).

### List all anomalies

```bash
python tracker.py list
```

### Export anomalies to a JSON file

```bash
python tracker.py export anomalies.json
```

*   `anomalies.json`: The name of the file to export to. If not provided, defaults to `anomalies.json` in the current directory.

## Data Storage

Anomalies are stored in a file named `anomalies.json` in the same directory as `tracker.py`. This file is automatically created if it doesn't exist.

## Contributing

Feel free to report bugs or suggest improvements! Perhaps a 'temporal paradox resolver' feature?
