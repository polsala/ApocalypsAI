# Nightly Asset Auditor

## Overview

The Nightly Asset Auditor is your essential companion for navigating the digital chaos. This utility scans a specified directory, meticulously categorizing files by their extension, tallying their collective size, and assigning a 'survival score' based on their perceived importance in a post-apocalyptic world. Think of it as a digital inventory for the end times, helping you discern the critical data from the digital dust.

## Features

*   **Directory Scan**: Recursively traverses a target directory.
*   **File Categorization**: Groups files by their extension.
*   **Size Aggregation**: Calculates the total size for each file type.
*   **Survival Scoring**: Assigns a whimsical-yet-insightful 'survival score' to each file type, indicating its potential utility or importance.
*   **Report Generation**: Outputs a structured report summarizing the audit findings.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

## Usage

To run the auditor, simply execute the `auditor.py` script with the target directory as an argument:

```bash
python3 src/auditor.py /path/to/your/repository
```

### Example Output (Markdown format):

```markdown
# Digital Asset Audit Report: /path/to/your/repository

## Audit Date: 2023-10-27 10:00:00

| File Type | Count | Total Size | Survival Score | Notes |
| :-------- | :---- | :--------- | :------------- | :---- |
| .py       | 15    | 150 KB     | 5 (Critical)   | Core logic, agent brains. |
| .md       | 5     | 25 KB      | 5 (Critical)   | Documentation, survival guides. |
| .yml      | 8     | 12 KB      | 5 (Critical)   | Configuration, workflow blueprints. |
| .txt      | 10    | 50 KB      | 3 (Useful)     | Data logs, notes. |
| .log      | 20    | 2 MB       | 1 (Disposable) | Ephemeral records. |
| .tmp      | 3     | 10 KB      | 1 (Disposable) | Temporary files, easily lost. |
| (Unknown) | 2     | 5 KB       | 0 (Irrelevant) | Uncategorized detritus. |

## Summary

Total Files Scanned: 63
Total Size Scanned: 2.25 MB

*Prioritize files with higher survival scores for backup and preservation.*
```

## Survival Score Legend

*   **5 (Critical)**: Essential code, documentation, critical configurations.
*   **3 (Useful)**: General data, logs, non-critical text.
*   **1 (Disposable)**: Temporary files, backups, archives that can be regenerated.
*   **0 (Irrelevant)**: Unknown types, system files, or files deemed utterly useless in the grand scheme of things.

## Development

Feel free to extend the `SURVIVAL_SCORES` dictionary in `src/auditor.py` to customize file type importance to your specific needs.
