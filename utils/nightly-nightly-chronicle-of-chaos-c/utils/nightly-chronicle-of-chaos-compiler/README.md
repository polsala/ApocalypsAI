# Nightly Chronicle of Chaos Compiler

## Overview
In the ever-shifting landscape of the post-apocalypse, keeping track of daily events, discoveries, and dangers is paramount. The 'Nightly Chronicle of Chaos Compiler' is a simple, yet essential, command-line utility designed to help you maintain a personal logbook of your journey through the wasteland.

It allows you to quickly add timestamped entries to a daily log file and then compile all your daily logs into a single, comprehensive chronicle, sorted by date. Never lose track of that suspicious rustling in Sector 7, or the location of that surprisingly intact can of beans again!

## Features
- **Daily Logging**: Easily add new entries to a log file specific to the current date.
- **Chronicle Compilation**: Merge all your daily logs into one master `chronicle.md` file, ordered chronologically.
- **Log Viewing**: Quickly view the current day's log or the entire compiled chronicle.

## Installation
This utility is self-contained and written in Python 3.11. No external dependencies are required beyond the standard library.

1.  Navigate to the `utils/nightly-chronicle-of-chaos-compiler/` directory.
2.  You can run the script directly using `python src/chronicle_compiler.py`.

## Usage
All commands are executed via `python src/chronicle_compiler.py <command> [arguments]`.

### 1. Add an entry
Adds a new timestamped entry to the current day's log file (`logs/YYYY-MM-DD.log`). If the `logs` directory doesn't exist, it will be created.

```bash
python src/chronicle_compiler.py add "Found a rusty spanner near the old water tower. Might be useful."
```

### 2. Compile the chronicle
Reads all log files from the `logs/` directory and compiles them into `chronicle.md` in the utility's root directory. Existing `chronicle.md` will be overwritten.

```bash
python src/chronicle_compiler.py compile
```

### 3. View a log
Views the content of the current day's log or the entire compiled chronicle.

```bash
# View today's log
python src/chronicle_compiler.py view daily

# View the entire compiled chronicle
python src/chronicle_compiler.py view chronicle
```

## File Structure
```
nightly-chronicle-of-chaos-compiler/
├── README.md
├── src/
│   └── chronicle_compiler.py
└── tests/
    └── test_chronicle_compiler.py
└── logs/             # Created automatically when adding entries
    ├── YYYY-MM-DD.log
    └── ...
```
