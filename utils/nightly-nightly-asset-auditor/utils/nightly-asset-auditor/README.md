# Nightly Asset Auditor

The Nightly Asset Auditor is a crucial utility for any pre- or post-apocalyptic archivist. It meticulously scans a specified directory, cataloging files by type, calculating their collective mass, and highlighting any "critical" documents that might contain vital survival information or ominous prophecies.

Ensure your digital hoard is accounted for before the next cataclysm strikes!

## Usage

```bash
python src/auditor.py <directory_path> [--extensions .py .md .txt] [--critical-keywords "secret base" "emergency cache"]
```

### Arguments

*   `<directory_path>`: The root directory to scan.
*   `--extensions`: (Optional) A space-separated list of file extensions to include in the audit (e.g., `.py .md .txt`). If not provided, all files will be considered.
*   `--critical-keywords`: (Optional) A space-separated list of keywords. Files containing any of these keywords will be flagged as "critical" in the report. Case-insensitive.

## Example

```bash
python src/auditor.py ./my_survival_data --extensions .txt .log --critical-keywords "coordinates" "safe zone"
```

This will scan the `my_survival_data` directory, focusing on `.txt` and `.log` files, and report any that mention "coordinates" or "safe zone".

## Output

The auditor prints a formatted report to standard output, detailing:
*   Total files scanned.
*   Files grouped by extension with counts and total sizes.
*   A list of "critical" files found, along with the keywords they contain.
