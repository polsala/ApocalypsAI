# Nightly Scavenged Intel Consolidator

## Overview
In the desolate landscape of the post-apocalypse, information is power – and often, it's scattered, fragmented, and duplicated across countless scraps of paper, data logs, and hastily scribbled notes. The `nightly-scavenged-intel-consolidator` is your digital sifter, designed to scour a specified directory for `.txt` files, extract vital 'intel' (tips, locations, warnings), de-duplicate them, and present a clean, consolidated report.

Think of it as your personal data scavenger, making sense of the chaos so you can focus on survival.

## Usage

```bash
python src/consolidator.py <path_to_intel_directory>
```

### Example

Given a directory `scraps/` with files:

`scraps/note_01.txt`:
```
Found some berries.
TIP: Red berries are usually poisonous. Stick to blue.
LOCATION: Old gas station, west of the river. Fuel might be present.
WARNING: Watch out for mutated squirrels near the old bridge.
```

`scraps/log_entry.txt`:
```
Another day, another struggle.
TIP: Always check for traps before entering abandoned buildings.
LOCATION: Old gas station, west of the river. Fuel might be present.
```

Running `python src/consolidator.py scraps/` would output:

```
--- Consolidated Scavenged Intel ---

[ TIPS ]
- Always check for traps before entering abandoned buildings.
- Red berries are usually poisonous. Stick to blue.

[ LOCATIONS ]
- Old gas station, west of the river. Fuel might be present.

[ WARNINGS ]
- Watch out for mutated squirrels near the old bridge.

------------------------------------
```

## Features
- Scans `.txt` files in a given directory.
- Extracts lines prefixed with `TIP:`, `LOCATION:`, and `WARNING:`.
- Automatically de-duplicates identical intel entries.
- Presents a categorized, easy-to-read report.

## Development

To run tests:

```bash
python -m unittest tests/test_consolidator.py
```
