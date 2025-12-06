# Data Decontamination Duster

## Purge the Digital Fallout from Your System!

The ApocalypsAI Data Decontamination Duster is a whimsical-yet-useful utility designed to help you identify and remove "irradiated" data – temporary files, old logs, and cache directories – from your system. Keep your digital wasteland pristine and reclaim valuable storage space!

### Philosophy

In a world of digital decay, even your file system can accumulate hazardous waste. This duster helps you perform regular "decontamination sweeps" to ensure your machine runs efficiently, free from the digital fallout of past operations.

### Features

*   **Irradiated Data Detection**: Scans specified paths for files and directories that might be considered digital waste.
*   **Size Reporting**: Provides a summary of the total size of detected "irradiated" data.
*   **Dry Run Mode**: Safely preview what would be decontaminated without making any changes.
*   **Actual Decontamination**: With the `--cleanse` flag, permanently remove the identified data.

### Installation

This utility is self-contained and written in Python 3.11+. No special installation steps are required beyond having Python installed.

1.  Navigate to the `utils/data-decontamination-duster/` directory.
2.  Run the `duster.py` script directly.

### Usage

The `duster.py` script is a command-line tool.

```bash
python src/duster.py <path1> [path2 ...] [--cleanse]
```

*   `<path1> [path2 ...]`: One or more paths (files or directories) to scan for "irradiated" data.
*   `--cleanse`: (Optional) Perform actual decontamination (delete files/directories). If omitted, the tool will run in dry-run mode, reporting what *would* be removed without making changes.

#### Examples

**1. Scan for irradiated data (dry run):**

This command will scan `/tmp/my_app_cache` and `/var/log/old_logs` and report any detected "fallout" without deleting anything.

```bash
python src/duster.py /tmp/my_app_cache /var/log/old_logs
```

**2. Perform actual decontamination:**

This command will scan the specified paths and, if "irradiated" data is found, it will proceed to delete it. **Use with caution!**

```bash
python src/duster.py /tmp/my_app_cache /var/log/old_logs --cleanse
```

**3. Decontaminate a specific old file:**

```bash
python src/duster.py /home/user/downloads/temp_report.zip --cleanse
```

### Development & Testing

To run the tests, navigate to the `utils/data-decontamination-duster/` directory and execute:

```bash
python -m unittest tests/test_duster.py
```

All tests are deterministic and use mocks to simulate file system operations, ensuring no actual files are touched during testing.
