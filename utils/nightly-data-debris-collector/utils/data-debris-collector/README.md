# Data Debris Collector

## Overview
In the digital wasteland, files accumulate like forgotten relics. The Data Debris Collector is your trusty scavenger, designed to help you identify and manage old, unused files across your file system. It scans specified directories, flags files older than a given threshold as 'debris', and generates a report to assist in cleanup efforts.

Keep your digital bunkers tidy and efficient!

## Features
- Scans directories recursively for files.
- Identifies files older than a specified age.
- Generates reports in human-readable text or machine-parseable JSON format.

## Installation
This utility is self-contained and requires Python 3.6+.
No external dependencies are needed beyond standard library modules.

## Usage
Run the `collector.py` script from the `src/` directory.

```bash
python src/collector.py <path_to_scan> [--age-days <int>] [--report-format <text|json>]
```

### Arguments
- `<path_to_scan>`: The root directory to start scanning from. (Required)
- `--age-days <int>`: The minimum age in days for a file to be considered 'debris'. Files older than this will be reported. Defaults to 30 days. (Optional)
- `--report-format <text|json>`: The format of the output report. Can be `text` (default) or `json`. (Optional)

### Examples

**Scan current directory for files older than 60 days, outputting text:**
```bash
python src/collector.py . --age-days 60
```

**Scan a specific directory for files older than 7 days, outputting JSON:**
```bash
python src/collector.py /var/log --age-days 7 --report-format json
```

## Report Format

### Text Format (Default)
```
Data Debris Report for: /path/to/scan (Older than 30 days)
----------------------------------------------------------
Found 3 debris files:

- /path/to/scan/old_log.txt (Modified: 2023-09-01 10:00:00)
- /path/to/scan/archive/temp_data.zip (Modified: 2023-08-15 14:30:00)
- /path/to/scan/another_old_file.bak (Modified: 2023-07-20 08:00:00)

Consider reviewing these files for archiving or deletion.
```

### JSON Format
```json
{
  "scan_path": "/path/to/scan",
  "age_threshold_days": 30,
  "report_generated": "2023-10-27T12:34:56",
  "debris_files": [
    {
      "path": "/path/to/scan/old_log.txt",
      "modified_timestamp": 1693555200.0,
      "modified_datetime": "2023-09-01T10:00:00"
    },
    {
      "path": "/path/to/scan/archive/temp_data.zip",
      "modified_timestamp": 1692186600.0,
      "modified_datetime": "2023-08-15T14:30:00"
    }
  ]
}
```
