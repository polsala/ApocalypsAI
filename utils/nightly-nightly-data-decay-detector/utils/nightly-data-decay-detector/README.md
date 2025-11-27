# Nightly Data Decay Detector

## Overview

The `nightly-data-decay-detector` is a whimsical-yet-useful utility designed to help you identify and manage digital 'rubble' – files that haven't been touched in a long time. In the ever-expanding digital landscape, it's easy for files to accumulate, consuming valuable storage and making organization a nightmare. This tool acts as your digital archaeologist, unearthing forgotten data before it truly decays into obscurity.

It scans a specified directory for files whose *most recent activity* (last modification or last access time) exceeds a defined 'decay threshold'. The output provides a clear list of these files, allowing you to decide whether to archive, delete, or simply acknowledge their existence.

## Usage

```bash
python src/decay_detector.py --path /path/to/scan --threshold-days 90
```

### Arguments:

*   `--path <directory>`: The root directory to start scanning from. (Required)
*   `--threshold-days <int>`: The number of days after which a file is considered 'decayed' if its most recent activity (modification or access) is older than this threshold. (Default: 90)

## Example Output

```json
[
  {
    "file": "/path/to/scan/old_project/legacy_code.py",
    "last_modified": "2023-01-15 10:30:00",
    "last_accessed": "2023-01-15 10:35:00",
    "age_days": 300
  },
  {
    "file": "/path/to/scan/archive/forgotten_report.pdf",
    "last_modified": "2022-11-01 14:00:00",
    "last_accessed": "2022-11-01 14:00:00",
    "age_days": 400
  }
]
```

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed beyond the standard library.

To run, simply navigate to the `utils/nightly-data-decay-detector/` directory and execute the script.

## Contributing

Feel free to suggest improvements or report issues! This tool is part of the ApocalypsAI project, aiming to bring order to the digital chaos.
