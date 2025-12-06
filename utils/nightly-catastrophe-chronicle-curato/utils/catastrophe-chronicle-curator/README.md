# Catastrophe Chronicle Curator

"Documenting the End Times, One Disaster at a Time."

This utility provides a simple command-line interface to log, list, and search for 'catastrophic events'. Whether it's a global Wi-Fi outage, a zombie sighting, or just a particularly bad Tuesday, keep track of it all in your personal chronicle.

## Features

*   **Add Events**: Log a new event with a timestamp and description.
*   **List Events**: View all recorded events in chronological order.
*   **Search Events**: Find specific events using keywords.
*   **Local Storage**: All events are stored in a `catastrophes.json` file in the utility's directory.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

1.  Navigate to the `utils/catastrophe-chronicle-curator/` directory.
2.  You can run the script directly.

## Usage

All commands are executed via the `src/chronicle.py` script.

### Add an event

```bash
python src/chronicle.py add "Global Wi-Fi went down for 3 minutes. Panic ensued."
```

### List all events

```bash
python src/chronicle.py list
```

### Search for events by keyword

```bash
python src/chronicle.py search "Wi-Fi"
```

```bash
python src/chronicle.py search "zombie"
```

## Example Workflow

```bash
# Add a few events
python src/chronicle.py add "Mysterious glowing orb appeared over the city."
python src/chronicle.py add "Ration supplies are running low. Need to scavenge."
python src/chronicle.py add "Heard strange whispers from the old abandoned factory."

# List them all
python src/chronicle.py list

# Search for something specific
python src/chronicle.py search "whispers"
```

## Development & Testing

To run the automated tests for this utility:

```bash
python -m unittest tests/test_chronicle.py
```
