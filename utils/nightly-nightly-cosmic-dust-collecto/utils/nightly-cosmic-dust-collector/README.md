# Nightly Cosmic Dust Collector

## Overview

The 'Cosmic Dust Collector' is your vigilant guardian against the entropy of the digital wasteland. It silently monitors designated directories for changes in your precious files. When a file is modified, a snapshot of its *current* state is carefully archived into a 'cosmic dustbin' – a special directory where historical versions are preserved, timestamped, and ready for retrieval. Think of it as collecting the faint echoes of your data's past, ensuring no valuable byte is truly lost to the void.

## Features

*   **Automated Versioning**: Automatically archives files when changes are detected.
*   **Timestamped Snapshots**: Each archived version is clearly marked with its collection time.
*   **Simple Configuration**: Easy to set up source directories and a dustbin location.
*   **Lightweight**: Uses standard Python libraries, minimal overhead.

## Usage

```bash
python src/collector.py --source /path/to/your/precious/data --dustbin /path/to/your/cosmic/dustbin
```

### Arguments:

*   `--source <path>`: The directory to monitor for file changes.
*   `--dustbin <path>`: The directory where archived file versions will be stored. This directory will also contain a manifest file (`_dust_manifest.json`) to track file states.

## How it Works

1.  The utility scans the `--source` directory.
2.  For each file, it calculates a content hash and records its modification timestamp.
3.  It compares these with the last known state stored in `_dust_manifest.json` within the `--dustbin`.
4.  If a file is new or has changed (different hash or timestamp), its current version is copied into the `--dustbin` with a unique, timestamped filename (e.g., `my_document.txt.20231027143000.bak`).
5.  The `_dust_manifest.json` is updated with the new file state.

## Example

Let's say you have `my_notes.txt` in `/data/my_project`.

1.  **First run**: `my_notes.txt` is new. It's copied to `/archive/dustbin/my_notes.txt.20231027100000.bak`.
2.  **Second run (after modification)**: `my_notes.txt` has changed. The *new* version is copied to `/archive/dustbin/my_notes.txt.20231027110000.bak`.

Now, `/archive/dustbin` contains two versions of `my_notes.txt`, preserving its history.
