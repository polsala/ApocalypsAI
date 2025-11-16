# Nightly Asset Auditor

## Overview
The ApocalypsAI Nightly Asset Auditor is a whimsical-yet-useful utility designed to help you assess the digital resilience of your directories. It scans a specified directory, categorizes files by type, calculates their total size, and assigns a 'survival score' based on the perceived importance of each file type in a post-apocalyptic scenario. Think of it as a digital inventory manager for the end times.

## Features
- Scans a target directory recursively.
- Categorizes files by their extension.
- Calculates total file count and size.
- Assigns a 'survival score' to each file type (e.g., `.md` for crucial documentation, `.py` for essential tools).
- Generates a summary report with an overall 'Apocalypse Readiness Score'.

## Usage
To run the auditor, simply execute the `auditor.py` script with the path to the directory you wish to audit.

```bash
python3 src/auditor.py /path/to/your/directory
```

### Example Output
```
ApocalypsAI Digital Asset Audit Report for: /path/to/your/directory
------------------------------------------------------------------

Total Files Found: 15
Total Size: 2.5 MB
Overall Apocalypse Readiness Score: 125

File Type Breakdown:
--------------------
.md  : 3 files, 150.0 KB, Score: 30  (Survival Priority: High)
.py  : 5 files, 500.0 KB, Score: 40  (Survival Priority: Medium)
.json: 2 files, 1.0 MB, Score: 12  (Survival Priority: Medium)
.txt : 4 files, 800.0 KB, Score: 20  (Survival Priority: Low)
.log : 1 files, 50.0 KB, Score: 1   (Survival Priority: Very Low)
```

## Development
This utility is written in Python 3.11+ and uses standard library modules only. Tests are located in `tests/test_auditor.py`.
