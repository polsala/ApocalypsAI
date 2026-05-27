# Nightly Temporal Pocket Cleaner

A whimsical utility to help you manage digital clutter by moving old, forgotten files into a "temporal pocket" – a hidden directory – for later retrieval. Keep your digital space tidy and your mind clear, knowing your files aren't truly gone, just... elsewhere.

## Features

- **Clean**: Identifies and moves files older than a specified age into a `.temporal_pocket` subdirectory.
- **List**: Shows you what forgotten treasures reside within a temporal pocket.
- **Retrieve**: Brings files back from the temporal pocket to their original location.

## Usage

```bash
./src/temporal_pocket_cleaner.sh <command> <directory> [options]
```

### Commands:

#### `clean <directory> <age_in_days>`
Moves files older than `age_in_days` from `<directory>` into `<directory>/.temporal_pocket`.

**Example:**
```bash
./src/temporal_pocket_cleaner.sh clean /path/to/my/documents 30
```
This will move all files in `/path/to/my/documents` older than 30 days into `/path/to/my/documents/.temporal_pocket`.

#### `list <directory>`
Lists all files currently residing in `<directory>/.temporal_pocket`.

**Example:**
```bash
./src/temporal_pocket_cleaner.sh list /path/to/my/documents
```

#### `retrieve <directory> [filename_pattern]`
Moves files from `<directory>/.temporal_pocket` back to `<directory>`.
If `filename_pattern` is provided, only files matching the pattern will be retrieved. If no pattern is given, all files are retrieved.

**Example (retrieve a specific file):**
```bash
./src/temporal_pocket_cleaner.sh retrieve /path/to/my/documents "old_report.txt"
```

**Example (retrieve all files):**
```bash
./src/temporal_pocket_cleaner.sh retrieve /path/to/my/documents
```

## Installation

This is a standalone bash script. Simply download `src/temporal_pocket_cleaner.sh` and make it executable:

```bash
chmod +x src/temporal_pocket_cleaner.sh
```

## Development & Testing

To run the automated tests:

```bash
./tests/test_temporal_pocket_cleaner.sh
```
