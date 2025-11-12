# Cosmic Dust Bunny Collector

## Purpose

The `cosmic-dust-bunny-collector` is a whimsical-yet-useful utility designed to help you declutter your digital workspace. It scans a specified directory for small, old, and potentially forgotten files – what we affectionately call 'cosmic dust bunnies'. These are often temporary files, old logs, forgotten build artifacts, or tiny remnants of past projects that accumulate over time, consuming precious disk space and mental bandwidth.

This utility identifies these digital dust bunnies and lists them, providing you with a clear overview of what could be safely archived or deleted, helping you maintain a tidy and efficient repository or project directory.

## Usage

Run the script from your terminal, providing the path to the directory you wish to scan. You can also specify the age threshold and maximum file size.

```bash
python src/dust_collector.py --path /path/to/your/project --age 60 --max-size 524288
```

### Arguments:

*   `--path <directory>` (required): The root directory to start scanning from.
*   `--age <days>` (optional): Files older than this many days will be considered 'old'. Default: `30` days.
*   `--max-size <bytes>` (optional): Files larger than this size (in bytes) will be ignored. Default: `1048576` bytes (1 MB).

## Example Output

```
Scanning /path/to/your/project for cosmic dust bunnies...

Found 3 cosmic dust bunnies:

- Path: /path/to/your/project/temp/old_log.txt
  Size: 1234 bytes
  Last Modified: 2023-01-15 10:30:00 (300 days ago)

- Path: /path/to/your/project/build/cache/temp_file.tmp
  Size: 567 bytes
  Last Modified: 2023-02-20 14:00:00 (250 days ago)

- Path: /path/to/your/project/docs/drafts/old_idea.md
  Size: 890 bytes
  Last Modified: 2023-03-01 09:00:00 (240 days ago)

Cleanup suggestions:
Consider archiving or deleting these files to free up space and declutter your project.
```
