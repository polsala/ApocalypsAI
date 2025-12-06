# Nightly Data Dust Defragmenter

## 🧹 Purpose

In the chaotic aftermath, digital detritus accumulates like radioactive fallout. The `Nightly Data Dust Defragmenter` is a whimsical yet essential utility designed to help you identify and manage redundant files – what we affectionately call "data dust" – scattered across your storage drives. By scanning specified directories, it uncovers duplicate files based on their content, allowing you to reclaim precious storage space and bring order to your digital wasteland.

## 🚀 How to Use

1.  **Navigate**: Change into the utility's directory:
    ```bash
    cd utils/nightly-data-dust-defragmenter/src
    ```
2.  **Run**: Execute the `defragmenter.py` script, providing the path to the directory you wish to scan.
    ```bash
    python3 defragmenter.py --path /path/to/your/scavenged/data
    ```
    Replace `/path/to/your/scavenged/data` with the actual directory.

## ⚙️ Options

*   `--path <directory>`: **Required**. The root directory to scan for duplicate files.
*   `--verbose`: Optional. Print more detailed information during the scan.

## 🧪 Example Output

```
Scanning /path/to/your/scavenged/data for data dust...
Found 2 groups of duplicate files:

--- Group 1 (Hash: 87d9a...) ---
  - /path/to/your/scavenged/data/logs/day_1_report.txt
  - /path/to/your/scavenged/data/backups/old_report.txt
  - /path/to/your/scavenged/data/archive/report_copy.txt

--- Group 2 (Hash: f3e1b...) ---
  - /path/to/your/scavenged/data/images/sunset_ruins.jpg
  - /path/to/your/scavenged/data/photos/sunset_ruins_copy.jpg

Scan complete. May your storage be ever clean!
```
