# Nightly Chronicle Keeper Logbook

A humble command-line utility for the discerning survivor, designed to help you keep a timestamped log of your daily findings, observations, or existential musings in the face of the unknown. Never forget that peculiar glowing mushroom or the day the sky turned green again.

## Usage

```bash
python src/logbook.py add "Found a rusty can of beans near the old gas station."
python src/logbook.py view 5
python src/logbook.py view --log-file my_personal_chronicle.log
```

### Commands

*   `add <message>`: Appends a new timestamped entry to the logbook.
*   `view [N]`: Displays the last `N` entries from the logbook. If `N` is omitted, all entries are shown.
*   `--log-file <path>`: (Optional) Specifies the path to the log file. Defaults to `chronicle.log` in the current directory.

## Installation

This utility is self-contained and requires Python 3.6+ (for f-strings). No external dependencies are needed.

1.  Navigate to the `nightly-chronicle-keeper-logbook` directory.
2.  Run the `logbook.py` script directly.

## Examples

```bash
# Add an entry
python src/logbook.py add "Repaired the water purifier. Output is still a bit murky, but drinkable."

# Add another entry
python src/logbook.py add "Heard strange whispers from the old radio tower tonight. Probably just the wind."

# View the last 2 entries
python src/logbook.py view 2

# View all entries
python src/logbook.py view

# Use a custom log file
python src/logbook.py add "Discovered a hidden stash of pre-apocalypse comic books!" --log-file secret_stash.log
python src/logbook.py view --log-file secret_stash.log
```
