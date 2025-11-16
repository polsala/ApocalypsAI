# Nightly Chronicle Keeper Logbook

## Purpose
In the chaotic aftermath, reliable record-keeping is paramount. The Chronicle Keeper Logbook is a simple, command-line utility designed to help survivors quickly log timestamped entries about their daily activities, observations, and critical events. Whether it's tracking resource caches, noting mutant sightings, or simply documenting the passage of time, this tool ensures your chronicles are preserved.

## Usage

### Prerequisites
* Python 3.6+

### Installation
This utility is self-contained. Simply navigate to its directory.

### Adding an Entry
To add a new entry to your logbook:

```bash
python src/logbook.py add "Discovered a cache of canned beans near the old library. Marked coordinates: [34.0522, -118.2437]."
```

The entry will be appended to `chronicle.log` in the current working directory, prefixed with the current date and time.

### Viewing Entries
To view all entries in your logbook:

```bash
python src/logbook.py view
```

This will print the entire contents of `chronicle.log` to your console.

## Log File Location
The `chronicle.log` file will be created in the directory from which `logbook.py` is executed. It's recommended to run the utility from a consistent location or manage the log file's path as needed.

## Development

### Running Tests
To ensure the logbook is functioning correctly, run the tests:

```bash
python -m unittest tests/test_logbook.py
```
