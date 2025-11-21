# Nightly Asset Auditor

The ApocalypsAI Nightly Asset Auditor is a whimsical-yet-useful utility designed to help you quickly assess the "survival readiness" of your digital assets. It scans a specified directory, categorizes files by their extension, calculates their total size, and assigns a "survival score" to give you an immediate sense of what's important and what might just be digital rubble.

## Features

*   **File Categorization**: Groups files by their extension.
*   **Size Calculation**: Reports total size per category and overall.
*   **Survival Scoring**: Assigns a whimsical "survival score" based on file type, helping you prioritize.
*   **CLI Interface**: Easy to run from your terminal.

## How to Use

1.  Navigate to the `nightly-asset-auditor` directory.
2.  Run the `auditor.py` script with the target directory as an argument.

```bash
python src/auditor.py /path/to/your/project
```

### Example Output

```
ApocalypsAI Asset Audit Report for: /path/to/your/project

--- Overall Summary ---
Total Files Scanned: 15
Total Size: 1.2 MB
Overall Survival Score: 42 points

--- File Type Breakdown ---
.py (Python Source)
  Files: 5
  Size: 500 KB
  Survival Score: 15 (Essential)

.md (Markdown Document)
  Files: 3
  Size: 150 KB
  Survival Score: 15 (Critical)

.json (JSON Data)
  Files: 2
  Size: 50 KB
  Survival Score: 10 (Critical)

.log (Log File)
  Files: 3
  Size: 400 KB
  Survival Score: 3 (Useful)

.tmp (Temporary File)
  Files: 2
  Size: 100 KB
  Survival Score: 0 (Junk)

--- Survival Score Legend ---
*   **Critical (5 points/file)**: Documentation, Configuration, Core Data
*   **Essential (3 points/file)**: Source Code, Key Scripts
*   **Useful (1 point/file)**: Logs, Auxiliary Data, Web Assets
*   **Junk (0 points/file)**: Temporary, Backups, Archives, System Files
*   **Unknown (0 points/file)**: Uncategorized files
```
