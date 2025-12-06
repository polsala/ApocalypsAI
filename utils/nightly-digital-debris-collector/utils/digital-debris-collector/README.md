# Digital Debris Collector

## 🧹 Clean Your Digital Bunker!

In the post-apocalyptic digital landscape, even your files can become forgotten relics, gathering virtual dust and consuming precious storage. The `digital-debris-collector` is your trusty broom, designed to sweep through your directories and identify files that are either ancient, untouched, or simply empty.

Keep your digital bunker lean and efficient, ready for whatever the future throws at it!

## ✨ Features

*   **Old File Detection**: Identifies files not accessed or modified within a specified number of days.
*   **Empty File Detection**: Pinpoints files that take up space but contain no data.
*   **Recursive Scan**: Traverses subdirectories to ensure no digital dust bunny is missed.
*   **Configurable Threshold**: You decide what 'old' means for your files.

## 🚀 Usage

This utility is a Python 3.11 script. To run it, navigate to its directory and execute it with `python`.

```bash
python src/debris_collector.py <directory_to_scan> [--days-threshold <days>]
```

### Arguments:

*   `<directory_to_scan>`: The path to the directory you want to scan for debris. This is a required argument.
*   `--days-threshold <days>`: (Optional) The number of days. Files not accessed or modified within this period will be flagged as 'old'. Defaults to `90` days.

### Examples:

Scan your current directory for files older than 90 days:

```bash
python src/debris_collector.py .
```

Scan your 'documents' folder for files older than 365 days:

```bash
python src/debris_collector.py /home/user/documents --days-threshold 365
```

## 💡 Output

The script will print a report to the console, listing all identified 'old' and 'empty' files, along with their relevant timestamps (access and modification times for old files).

```
Scanning '/home/user/data' for digital debris (threshold: 90 days)...

--- Digital Debris Report ---

Found 2 'old' files (not accessed/modified in 90 days):
  - /home/user/data/old_report.txt (Accessed: 2023-01-15T10:00:00; Modified: 2023-01-10T11:30:00)
  - /home/user/data/archive/forgotten_log.log (Accessed: 2022-12-01T08:00:00; Modified: 2022-11-25T14:00:00)

Found 1 'empty' files:
  - /home/user/data/temp/empty_file.tmp

Consider reviewing these files for potential cleanup.
```

If no debris is found, you'll get a celebratory message!

```
✨ Your digital bunker is sparkling clean! No debris found. ✨
```

## 🧪 Testing

To run the tests for this utility, use `unittest` from the root of the `digital-debris-collector` directory:

```bash
python -m unittest tests/test_debris_collector.py
```
