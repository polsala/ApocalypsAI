# Nightly Echo Chamber Monitor

## Overview

The ApocalypsAI Nightly Echo Chamber Monitor is a whimsical yet practical utility designed to help you identify and manage redundant files within your specified directories. In the chaotic post-apocalyptic landscape, digital clutter can be as dangerous as physical debris. This tool scans your file system, calculates content hashes, and reports groups of identical files, allowing you to reclaim precious storage space and maintain a lean, efficient data archive.

It's like a sonic detector for digital echoes – finding where the same data resonates in multiple places.

## Usage

```bash
python3 src/echo_monitor.py <directory_path>
```

### Example:

```bash
python3 src/echo_monitor.py /path/to/your/project
```

### Output Example:

```
Scanning '/path/to/your/project' for duplicate files...

Found 2 groups of duplicate files:

Group 1 (SHA256: a1b2c3d4e5f6...):
  - /path/to/your/project/data/report_v1.txt
  - /path/to/your/project/archive/old_report.txt

Group 2 (SHA256: f6e5d4c3b2a1...):
  - /path/to/your/project/images/logo_copy.png
  - /path/to/your/project/assets/logo.png
  - /path/to/your/project/backup/logo_final.png
```

## How it Works

The utility performs a recursive scan of the target directory. For each file encountered, it computes a SHA256 hash of its content. Files with identical SHA256 hashes are considered duplicates. The tool then groups these duplicates and presents them in a clear, actionable report.

## Installation

This utility is self-contained and requires no special installation beyond a standard Python 3.11+ environment. Just place the `nightly-echo-chamber-monitor` folder in your `utils/` directory.
