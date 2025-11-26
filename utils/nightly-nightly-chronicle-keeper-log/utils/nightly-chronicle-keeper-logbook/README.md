# Nightly Chronicle Keeper Logbook

A simple, yet essential, command-line utility for the discerning survivor. The Chronicle Keeper allows you to quickly log timestamped entries into a plain text file, serving as your personal record of discoveries, events, or musings in the ever-unfolding saga of the apocalypse.

Whether you're tracking radiation spikes, noting the location of a particularly robust can of beans, or simply documenting your daily existential dread, the Chronicle Keeper ensures your observations are preserved for posterity (or at least until the next EMP).

## Usage

### Add a new entry

```bash
python src/chronicle_keeper.py --message "Found a pristine copy of 'The Art of War' near the old library ruins."
```

Or, specify a custom log file:

```bash
python src/chronicle_keeper.py -m "Encountered a pack of particularly grumpy squirrels." -f my_personal_log.txt
```

### View the log

```bash
python src/chronicle_keeper.py --view
```

Or, view a specific log file:

```bash
python src/chronicle_keeper.py -v -f my_personal_log.txt
```

## Installation

This utility is self-contained and requires Python 3.6+ (compatible with 3.11). No external dependencies are needed.

1.  Navigate to the `utils/nightly-chronicle-keeper-logbook` directory.
2.  Run the `chronicle_keeper.py` script directly.

## Development & Testing

To run tests:

```bash
python -m unittest tests/test_chronicle_keeper.py
```
