# Nightly Scavenger's Scrapbook Generator

## Overview
In the desolate wastes, every scrap of information is vital. The `nightly-scavengers-scrapbook-generator` is a simple Python utility designed to help you compile your scattered text notes, logs, and observations into a single, chronologically ordered 'scrapbook' journal. Keep your survival story organized and easily reviewable.

## Features
- Scans a specified directory for `.txt` files.
- Sorts entries by filename (lexicographically, assuming a chronological naming convention, e.g., `YYYYMMDD_HHMMSS_note.txt`).
- Concatenates file contents into a single output file, adding clear headers for each entry.

## Usage

```bash
python src/scrapbook_generator.py --input-dir <path/to/your/notes> --output-file <path/to/your/journal.txt>
```

### Arguments:
- `--input-dir`: The directory containing your `.txt` notes.
- `--output-file`: The path to the output `.txt` file where the scrapbook will be generated.

## Example

Given an `input_notes/` directory with:
- `20770101_evening_observation.txt`: "Strange lights on the horizon. Might be raiders, might be a mirage."
- `20770101_morning_log.txt`: "Woke up. Still alive. Found a rusty can of beans."

Running:
```bash
python src/scrapbook_generator.py --input-dir input_notes/ --output-file my_journal.txt
```

Will produce `my_journal.txt`:

```
--- Entry from 20770101_evening_observation.txt ---
Strange lights on the horizon. Might be raiders, might be a mirage.


--- Entry from 20770101_morning_log.txt ---
Woke up. Still alive. Found a rusty can of beans.


```
*(Note: Entries are sorted lexicographically by filename. For strict chronological order, ensure filenames reflect this, e.g., `YYYYMMDD_HHMMSS_description.txt`.)*
