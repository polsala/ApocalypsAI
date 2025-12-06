# Chronos-Chime Time Capsule Creator

## Overview
In the ever-shifting sands of the apocalypse, some digital memories are worth preserving. The Chronos-Chime Time Capsule Creator allows you to encapsulate a directory's contents into a timestamped ZIP archive, a digital echo sent forward in time.

Think of it as a digital message in a bottle, ready to be discovered by future survivors (or your future self).

## Features
- Archives a specified directory into a standard `.zip` file.
- Automatically names the capsule with a timestamp for easy chronological sorting.
- Simple, self-contained, and ready for your most cherished (or mundane) digital artifacts.

## Usage

```bash
python src/time_capsule.py --source /path/to/your/precious/data --output /path/to/capsule/storage
```

### Arguments:
- `--source`: The path to the directory you wish to archive.
- `--output`: The directory where the time capsule (ZIP file) will be saved.
- `--prefix` (optional): A custom prefix for the capsule filename (default: `chronos_chime`).

## Example

To archive your `my_old_photos` directory and save the capsule in `~/digital_vault`:

```bash
python src/time_capsule.py --source ~/my_old_photos --output ~/digital_vault --prefix "memories_of_yore"
```

This will create a file like `~/digital_vault/memories_of_yore_20231027_143000.zip` (timestamp will vary).

## Installation
This utility is self-contained and requires Python 3.8+ (tested with 3.11). No external dependencies are needed beyond standard library modules.

Simply navigate to the `utils/nightly-chronos-chime-time-capsule` directory and run the `src/time_capsule.py` script.
