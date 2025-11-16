# Nightly Temporal Tear Tracker

## Unearthing the Forgotten: A Digital Archeology Tool

In the ever-shifting sands of the ApocalypsAI repository, files can sometimes be lost to the temporal currents, forgotten and untouched for eons. The **Nightly Temporal Tear Tracker** is your digital archeologist, designed to unearth these relics by scanning specified directories for files that haven't been modified in a configurable period.

Identify stale code, forgotten assets, or files that might be candidates for archiving, deletion, or a much-needed review. Keep your digital wasteland tidy and efficient!

## Usage

Run the `tracker.py` script with the target directory and an optional threshold in days.

```bash
python3 src/tracker.py --path <directory_to_scan> [--threshold <days>]
```

- `--path`: The root directory to start scanning from. This is a required argument.
- `--threshold`: The number of days a file must be untouched to be considered 'stale'. Defaults to 90 days if not specified.

### Example:

To find files older than 180 days in your current directory:

```bash
python3 src/tracker.py --path . --threshold 180
```

To find files older than the default 90 days in a specific `archive` folder:

```bash
python3 src/tracker.py --path ./archive
```

## Output

The utility will print a list of identified 'stale' files, their last known modification date, and their age in days, helping you decide their fate in the post-apocalyptic digital landscape.
