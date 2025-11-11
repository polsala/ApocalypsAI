# Cataclysmic Cache Cleaner

## Overview

The `cataclysmic-cache-cleaner` is a vital utility for any digital survivor. It helps you reclaim precious disk space by identifying and purging old, forgotten files and caches that accumulate over time. Think of it as decluttering your digital bunker before the big one hits, ensuring you have maximum capacity for critical data and emergency plans.

## Features

*   **Targeted Cleaning**: Specify directories to scan.
*   **Age-Based Purge**: Only targets files older than a configurable number of days.
*   **Dry Run Mode**: See what would be deleted without actually removing anything.
*   **Interactive Confirmation**: Prompts before deletion (unless `--force` is used).

## Installation

This utility is self-contained. Simply navigate to its directory and run the Python script.

## Usage

```bash
python src/cleaner.py --path <directory> [--days <int>] [--dry-run] [--force]
```

### Arguments

*   `--path <directory>`: **Required**. The directory to scan for old files. Can be specified multiple times.
*   `--days <int>`: Optional. Files older than this many days will be targeted. Defaults to `30`.
*   `--dry-run`: Optional. Perform a scan and report what *would* be deleted, but don't actually delete anything.
*   `--force`: Optional. Skip interactive confirmation prompts and delete files immediately (use with caution!).

### Examples

Scan your downloads folder for files older than 60 days (dry run):

```bash
python src/cleaner.py --path ~/Downloads --days 60 --dry-run
```

Clean up temporary files in `/tmp` older than 7 days, with confirmation:

```bash
python src/cleaner.py --path /tmp --days 7
```

Force-clean multiple cache directories:

```bash
python src/cleaner.py --path ~/.cache --path /var/cache --force
```
