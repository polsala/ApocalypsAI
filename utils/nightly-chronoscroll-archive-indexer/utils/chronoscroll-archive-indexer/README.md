# Chronoscroll Archive Indexer

## Unearthing the Past, One Byte at a Time

In the chaotic aftermath, data fragments are scattered like digital dust. The Chronoscroll Archive Indexer is your trusty companion for cataloging these precious remnants. It scans a specified directory, meticulously recording file names, sizes, and their last known modification dates, then compiles them into a neat, human-readable index. Whether you're building a new civilization from scratch or just trying to find that one cat video from before the Great Glitch, the Chronoscroll has your back.

## Usage

The indexer can output its findings in either Markdown or JSON format.

### Prerequisites

*   Python 3.11+

### Running the Indexer

```bash
python src/indexer.py --path <directory_to_scan> [--output-format <markdown|json>] [--output-file <filename>]
```

*   `--path`: The directory to scan. (Required)
*   `--output-format`: The desired output format. Can be `markdown` (default) or `json`.
*   `--output-file`: Optional. If provided, the output will be written to this file. Otherwise, it prints to stdout.

### Examples

1.  **Index current directory and print Markdown to console:**
    ```bash
    python src/indexer.py --path .
    ```

2.  **Index a specific directory and save JSON to a file:**
    ```bash
    python src/indexer.py --path /path/to/your/archives --output-format json --output-file archive_index.json
    ```

3.  **Index a directory and save Markdown to a file:**
    ```bash
    python src/indexer.py --path /path/to/data --output-file data_summary.md
    ```

## Output Format Examples

### Markdown

```markdown
# Chronoscroll Archive Index - /path/to/your/archives

**Scan Date:** 2023-10-27 10:30:00

## Files Found: 3

- **document.txt**
  - Size: 1024 bytes
  - Last Modified: 2023-01-15 08:00:00
- **image.jpg**
  - Size: 51200 bytes
  - Last Modified: 2023-03-20 14:15:30
- **video.mp4**
  - Size: 1024000 bytes
  - Last Modified: 2023-09-01 18:45:10
```

### JSON

```json
{
  "scan_date": "2023-10-27T10:30:00",
  "scanned_path": "/path/to/your/archives",
  "files_count": 3,
  "files": [
    {
      "name": "document.txt",
      "size_bytes": 1024,
      "last_modified": "2023-01-15T08:00:00"
    },
    {
      "name": "image.jpg",
      "size_bytes": 51200,
      "last_modified": "2023-03-20T14:15:30"
    },
    {
      "name": "video.mp4",
      "size_bytes": 1024000,
      "last_modified": "2023-09-01T18:45:10"
    }
  ]
}
```
