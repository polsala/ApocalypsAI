# Nightly Rubble Report Generator

The digital apocalypse leaves behind a trail of forgotten files and bloated directories. The Nightly Rubble Report Generator is your trusty scout, sifting through the digital debris to provide a concise, actionable report on your system's disk usage. Identify the largest culprits and the oldest relics, so you can decide what to salvage and what to purge before the next wave hits!

## Features

*   **Disk Usage Summary**: Get an overview of the total size of scanned directories.
*   **Top Largest Files**: Pinpoint the biggest files hogging your precious storage.
*   **Top Oldest Files**: Discover files that haven't been touched in ages, potentially ripe for archiving or deletion.
*   **Configurable Scans**: Specify which directories to scan, thresholds for "large" files, and "old" files.
*   **Markdown Output**: Generates a clean, human-readable Markdown report.

## Usage

```bash
python src/report_generator.py --path /path/to/scan1 --path /path/to/scan2 --min-size 10 --min-age 365 --output report.md
```

### Arguments

*   `--path <directory>`: One or more directories to scan. Required.
*   `--min-size <MB>`: Minimum size in MB for a file to be considered "large". Default: 50 MB.
*   `--min-age <days>`: Minimum age in days for a file to be considered "old". Default: 180 days.
*   `--top-n <count>`: Number of top largest/oldest files to list. Default: 10.
*   `--output <filename>`: Output filename for the Markdown report. If not provided, prints to stdout.

## Example Report

```markdown
# Rubble Report for /home/user/projects and /var/log

**Generated On:** 2023-10-27 10:30:00

## Scan Summary

*   **Total Scanned Size:** 15.7 GB
*   **Total Files Scanned:** 12,345
*   **Total Directories Scanned:** 1,234

## Top 5 Largest Files (>= 50 MB)

1.  `1.2 GB` - `/home/user/projects/my_big_project/data/archive.zip`
2.  `800 MB` - `/var/log/nginx/access.log.1`
3.  `650 MB` - `/home/user/projects/another_project/build/output.iso`
4.  `120 MB` - `/home/user/downloads/large_video.mp4`
5.  `90 MB` - `/var/log/syslog.1`

## Top 5 Oldest Files (>= 180 days)

1.  `2 years, 3 months ago` - `/home/user/old_docs/legacy_report.pdf`
2.  `1 year, 10 months ago` - `/home/user/projects/archive/old_code.tar.gz`
3.  `1 year, 9 months ago` - `/var/log/old_audit.log`
4.  `200 days ago` - `/home/user/config/backup.conf`
5.  `190 days ago` - `/home/user/.cache/old_thumbnail.jpg`

---
*End of Report*
```
