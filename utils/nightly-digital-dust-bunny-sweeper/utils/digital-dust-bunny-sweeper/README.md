# Digital Dust Bunny Sweeper

## 🧹 What is this?

The Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to help you declutter your digital workspace. It scans a specified directory for "digital dust bunnies" – old, unused, empty files, and empty directories – and generates a report, helping you identify what can be safely swept away. Keep your pre-apocalypse data pristine!

## ✨ Features

*   **Finds Empty Files**: Identifies files with zero bytes.
*   **Finds Empty Directories**: Locates directories containing no files or subdirectories.
*   **Finds Ancient Files**: Reports on files older than a configurable threshold (default: 365 days).
*   **Comprehensive Report**: Outputs a clear summary of all identified dust bunnies.

## 🚀 How to Use

1.  **Navigate**: Change into the `digital-dust-bunny-sweeper` directory.
2.  **Run**: Execute the `sweeper.py` script with the target directory and an optional age threshold.

    ```bash
    python src/sweeper.py --path /path/to/your/messy/folder --age-days 180
    ```

    *   `--path`: (Required) The directory to scan.
    *   `--age-days`: (Optional) Files older than this many days will be flagged. Default is 365.

## 🧪 Example Output

```
🧹 Digital Dust Bunny Sweeper Report 🧹

Scanning: /path/to/your/messy/folder
Files older than 365 days:

  - /path/to/your/messy/folder/old_report.txt (Modified: 2022-01-15 10:00:00)
  - /path/to/your/messy/folder/archive/ancient_log.log (Modified: 2021-11-01 08:30:00)

Empty Files:

  - /path/to/your/messy/folder/empty.txt
  - /path/to/your/messy/folder/temp/placeholder.log

Empty Directories:

  - /path/to/your/messy/folder/temp/
  - /path/to/your/messy/folder/unused_project/

Summary:
  - Total old files found: 2
  - Total empty files found: 2
  - Total empty directories found: 2

Consider sweeping these digital dust bunnies away!
```

## 🛠️ Development

The utility is written in Python 3.11 and uses only standard library modules.

### Running Tests

```bash
python -m unittest tests/test_sweeper.py
```
