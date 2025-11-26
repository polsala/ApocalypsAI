# Nightly Chronicle Keeper

A simple, command-line utility for logging daily events, observations, and resource counts in a post-apocalyptic world. Keep track of your survival journey with timestamped entries and optional tags for easy categorization.

## Features

*   **Timestamped Entries**: Every log entry is automatically stamped with the current date and time.
*   **Tagging System**: Categorize your entries with hashtags (e.g., `#resource`, `#discovery`, `#danger`).
*   **Easy Viewing**: Quickly review all your chronicles or filter them by specific tags.
*   **Self-contained**: No external dependencies, just a single Python script.

## Installation

This utility is self-contained. Simply navigate to the `utils/nightly-chronicle-keeper/src/` directory.

## Usage

The `chronicle_keeper.py` script provides `add` and `view` commands.

### Adding an Entry

To add a new entry to your chronicle:

```bash
python src/chronicle_keeper.py add "Found a pristine can of ApocalypsAI brand beans." #food #resource
```

You can include multiple tags, separated by spaces. Tags should start with `#`.

### Viewing Entries

To view all entries in your chronicle:

```bash
python src/chronicle_keeper.py view
```

To view entries filtered by a specific tag:

```bash
python src/chronicle_keeper.py view #food
```

## Example Chronicle

```
[2023-10-27 10:00:00] #weather #observation Sky unusually clear, no radiation clouds visible.
[2023-10-27 10:30:15] #resource #food Found a pristine can of ApocalypsAI brand beans.
[2023-10-27 11:45:30] #danger Heard strange growling from the old factory. Avoid.
```
