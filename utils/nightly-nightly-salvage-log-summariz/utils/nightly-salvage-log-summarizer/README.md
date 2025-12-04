# Nightly Salvage Log Summarizer

## Description

In the post-apocalyptic digital wasteland, log files are often the only remnants of past systems, holding vital clues to their demise or survival. The `Nightly Salvage Log Summarizer` is a crucial utility designed to help you make sense of this digital detritus. It scans specified directories for log files, sifting through them to count occurrences of predefined keywords (like 'ERROR', 'WARNING', 'INFO', or any custom terms you provide).

This tool generates a concise summary report, detailing keyword counts per file and providing overall totals. It's an indispensable aid for quickly assessing the health, activity, or critical events within a vast collection of salvaged logs, helping you prioritize your digital archaeology efforts.

## Usage

```bash
python src/summarizer.py <directory> [--keywords KEYWORD1 KEYWORD2 ...] [--file-pattern PATTERN]
```

### Arguments:

*   `<directory>`: The path to the directory containing the log files you wish to scan.
*   `--keywords KEYWORD1 KEYWORD2 ...`: (Optional) A space-separated list of keywords to search for. If not provided, defaults to `ERROR`, `WARNING`, `INFO`.
*   `--file-pattern PATTERN`: (Optional) A glob-style pattern (e.g., `*.log`, `server_*.txt`) to filter which files are scanned. Defaults to `*.log`.

### Example:

To scan the `~/salvaged_data/logs` directory for 'CRITICAL' and 'FAILURE' messages in files ending with `.txt`:

```bash
python src/summarizer.py ~/salvaged_data/logs --keywords CRITICAL FAILURE --file-pattern '*.txt'
```

To scan the current directory for default keywords in `.log` files:

```bash
python src/summarizer.py .
```

## Output Example

```
Salvage Log Summary Report for: /path/to/logs
File Pattern: *.log
Keywords: ERROR, WARNING, INFO

--------------------------------------------------
File: server_alpha.log
  ERROR: 3
  WARNING: 1
  INFO: 10

File: server_beta.log
  ERROR: 0
  WARNING: 5
  INFO: 22

File: app.log
  ERROR: 1
  WARNING: 0
  INFO: 5

--------------------------------------------------
Overall Totals:
  ERROR: 4
  WARNING: 6
  INFO: 37
--------------------------------------------------
```
