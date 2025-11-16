# Nightly Asset Auditor

## Description
In the desolate aftermath, understanding what digital assets remain is paramount. The Nightly Asset Auditor is a whimsical-yet-useful utility designed to scan a given directory and provide a comprehensive inventory report of all files. It categorizes files by their extension, counts them, and calculates their total size, offering a clear overview of your digital rubble.

Whether you're cataloging salvaged data or just curious about the composition of a forgotten archive, this tool helps you make sense of the digital chaos.

## Usage

To run the auditor, simply provide the path to the directory you wish to scan:

```bash
python src/auditor.py <directory_path>
```

### Example

```bash
python src/auditor.py ~/my_salvaged_data
```

This will output a report to your console, detailing file counts, total sizes, and percentage breakdown by file type.

## Example Output

```
Scanning directory: /home/user/my_salvaged_data

--- Asset Audit Report ---

Total Files: 15
Total Size: 12.5 MB

File Type Breakdown:
--------------------
.py   : 5 files (2.1 MB) [16.8%]
.txt  : 3 files (0.5 MB) [4.0%]
.jpg  : 4 files (8.0 MB) [64.0%]
.md   : 2 files (1.0 MB) [8.0%]
(none): 1 file  (0.9 MB) [7.2%]
--------------------
```
