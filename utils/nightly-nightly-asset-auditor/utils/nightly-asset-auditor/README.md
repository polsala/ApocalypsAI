# Nightly Asset Auditor

## Overview

The `Nightly Asset Auditor` is a whimsical-yet-useful utility designed to help you understand the 'survival potential' of your digital assets. It scans a specified directory, categorizes files by their extensions, calculates their total size, and assigns a 'survival score' based on a predefined heuristic. This helps you quickly identify what's critical, what's code, and what's just digital rubble.

Think of it as your personal post-apocalyptic inventory manager, ensuring you know which data to salvage first when the servers inevitably crumble.

## Features

*   **File Categorization**: Groups files by their extension.
*   **Size Aggregation**: Calculates total size for each file type and the entire directory.
*   **Survival Scoring**: Assigns a score (Critical, Important, Useful, Ephemeral, Unknown) to each file type, providing a quick assessment of its perceived value.
*   **Markdown Report**: Generates a human-readable Markdown report summarizing the audit.

## Usage

To run the auditor, simply provide the path to the directory you wish to audit:

```bash
python src/auditor.py <path_to_directory>
```

### Example

```bash
python src/auditor.py ../
```

This will print the audit report to standard output.

## Survival Score Heuristic

The survival score is determined by the file extension:

*   **Critical**: `.md`, `.txt`, `.json`, `.yaml`, `.yml`, `.csv` (Documentation, configuration, vital data)
*   **Important**: `.py`, `.sh`, `.js`, `.go`, `.rs`, `.java`, `.cpp`, `.h` (Source code, essential scripts)
*   **Useful**: `.log`, `.xml`, `.html`, `.css`, `.pdf`, `.zip`, `.tar.gz` (Logs, web assets, compiled docs, archives)
*   **Ephemeral**: `.tmp`, `.bak`, `.swp`, `.DS_Store` (Temporary files, backups, system junk)
*   **Unknown**: Any other extension (Requires manual review)

This heuristic can be easily modified within the `auditor.py` script to suit your specific 'survival' criteria.
