# Nightly Gloom-and-Doom Data Duster

## 🧹 Reclaim Your Digital Wasteland 🧹

In the grim darkness of the far future, every byte counts! The `Nightly Gloom-and-Doom Data Duster` is your trusty companion for sifting through the digital rubble and identifying files that are ripe for deletion. Whether it's ancient logs, forgotten backups, or insidious duplicates, this utility helps you reclaim precious storage space.

### Features

*   **Age-based Pruning**: Find files older than a specified number of days.
*   **Size-based Scavenging**: Locate files exceeding a certain size threshold.
*   **Duplicate Detection**: Uncover identical files eating up redundant space using content hashing.
*   **Comprehensive Reporting**: Get a clear summary of potential candidates for deletion.

### Installation

This utility is self-contained. Simply navigate to its directory:

```bash
cd utils/nightly-gloom-and-doom-data-duster
```

### Usage

Run the `data_duster.py` script with your desired options:

```bash
python src/data_duster.py --path /path/to/your/digital/hoard
```

#### Options:

*   `--path <directory>` (required): The directory to scan.
*   `--age <days>` (optional): Report files older than this many days. Default: 365 (1 year).
*   `--size <MB>` (optional): Report files larger than this many megabytes. Default: 100 MB.
*   `--duplicates` (optional): Enable duplicate file detection based on content hash. This can be CPU intensive for large files.
*   `--output <file>` (optional): Save the report to a specified file instead of printing to console.

#### Examples:

Scan your `documents` folder for files older than 2 years (730 days) or larger than 50MB:

```bash
python src/data_duster.py --path ~/documents --age 730 --size 50
```

Scan your `backups` folder for any duplicate files:

```bash
python src/data_duster.py --path /mnt/backups --duplicates
```

Scan your entire home directory for all criteria and save the report:

```bash
python src/data_duster.py --path ~ --age 365 --size 200 --duplicates --output duster_report.txt
```

### Development & Testing

To run tests, ensure you are in the `nightly-gloom-and-doom-data-duster` directory and execute:

```bash
python -m unittest tests/test_data_duster.py
```
