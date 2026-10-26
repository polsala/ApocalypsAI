# Nightly Digital Hoard Organizer

## Summary

In the desolate digital wasteland, every byte counts. The `nightly-digital-hoard` utility helps you manage your precious data reserves by scanning your specified 'bunker' directory for excessively large or ancient files that might be consuming valuable storage rations. Keep your digital hoard lean and efficient!

## Whimsical Context

Even in the post-apocalypse, digital clutter can be a silent killer of efficiency. This tool acts as your personal data scavenger, identifying forgotten relics and oversized cargo containers that are just taking up space. It's time to declutter your digital bunker and ensure your most vital information is readily accessible when the next data storm hits.

## Installation

1.  **Clone the repository (if not already part of ApocalypsAI):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-digital-hoard
    ```
2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```
    (Note: This utility uses only built-in Node.js modules, so `npm install` might not be strictly necessary, but it's good practice for future expansions.)

## Usage

Run the utility from the command line, specifying the path to your digital bunker (directory) and optional thresholds for file size and age.

```bash
node src/index.js <path_to_bunker> [--max-size <MB>] [--max-age <days>]
```

*   `<path_to_bunker>`: The absolute or relative path to the directory you want to scan.
*   `--max-size <MB>`: (Optional) Files larger than this size (in Megabytes) will be flagged as 'Bulky Cargo Containers'. Default is 100 MB.
*   `--max-age <days>`: (Optional) Files last modified more than this many days ago will be flagged as 'Ancient Data Scrolls'. Default is 365 days.

### Examples

Scan your current directory for files over 50MB or older than 180 days:
```bash
node src/index.js . --max-size 50 --max-age 180
```

Scan your '~/Documents/Archive' directory with default thresholds:
```bash
node src/index.js ~/Documents/Archive
```

## Output

The utility will print a categorized report to the console, listing files that exceed your specified thresholds.

```
Scanning your digital bunker at: /path/to/your/bunker
Thresholds: Max Size = 100 MB, Max Age = 365 days

--- Digital Hoard Analysis ---

### Bulky Cargo Containers (Files > 100 MB):
  - /path/to/your/bunker/large_video.mp4 (250.5 MB)
  - /path/to/your/bunker/backup/old_archive.zip (120.1 MB)

### Ancient Data Scrolls (Files > 365 days old):
  - /path/to/your/bunker/old_report.pdf (Last modified: 2022-01-15)
  - /path/to/your/bunker/notes/forgotten_plan.txt (Last modified: 2021-11-01)

--- Hoard Summary ---
Found 2 Bulky Cargo Containers.
Found 2 Ancient Data Scrolls.

Recommendation: Review these items. Consider archiving, compressing, or purging them to free up valuable storage rations for the future!
```

## Development

### Running Tests

```bash
node tests/test_index.js
```
