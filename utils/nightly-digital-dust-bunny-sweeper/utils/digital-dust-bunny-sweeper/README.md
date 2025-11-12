# Digital Dust Bunny Sweeper

## 🧹 What is this?

The Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to help you reclaim disk space and maintain a tidy filesystem. It scans a specified directory for 'digital dust bunnies' – files that are:

1.  **Empty**: Files with 0 bytes.
2.  **Old**: Files not modified for a configurable number of days (default: 365 days).
3.  **Duplicate**: Files with identical content (based on SHA256 hash).

The utility provides a detailed report of its findings, helping you identify and manually clean up these digital nuisances.

## ✨ Features

*   **Empty File Detection**: Quickly spots those forgotten, zero-byte files.
*   **Old File Identification**: Flags files that haven't been touched in a while, perfect for archiving or deletion.
*   **Duplicate Content Finder**: Uncovers identical files lurking in different locations, saving precious disk space.
*   **Dry Run by Default**: Always reports findings first, ensuring you review before any action is taken.
*   **Configurable Age Threshold**: Customize what 'old' means to you.

## 🚀 How to Use

1.  **Navigate to the utility's directory**:
    ```bash
    cd utils/digital-dust-bunny-sweeper/src
    ```

2.  **Run the sweeper with a target directory**:
    ```bash
    python sweeper.py /path/to/your/target/directory
    ```
    Replace `/path/to/your/target/directory` with the actual path you want to scan.

3.  **Customize the age threshold (optional)**:
    To define 'old' as files not modified in, say, 180 days:
    ```bash
    python sweeper.py /path/to/your/target/directory --age-threshold 180
    ```

4.  **Review the report**: The utility will print a detailed report to your console, listing all detected digital dust bunnies.

### Example Output

```
Scanning '/home/user/my_project' for digital dust bunnies...

--- Digital Dust Bunny Report ---
Scan conducted on: 2023-10-27 10:30:00
Age threshold for 'old' files: 365 days

### Empty Files (0 bytes) ###
- /home/user/my_project/logs/empty.log
Found 1 empty files.

### Duplicate Files (identical content) ###
  Hash: abcdef1234...
  - /home/user/my_project/data/report_v1.csv
  - /home/user/my_project/backup/report_v1_copy.csv
  Hash: fedcba9876...
  - /home/user/my_project/assets/image.png
  - /home/user/my_project/temp/image_copy.png
Found 2 redundant duplicate files.

### Old Files (modified before 2022-10-27) ###
- /home/user/my_project/old_docs/legacy_spec.pdf (Modified: 2021-05-15)
- /home/user/my_project/archive/old_script.py (Modified: 2020-11-01)
Found 2 old files.

Total potential digital dust bunnies to clean: 5

This was a DRY RUN. No files were deleted.
To actually delete files, run with '--action delete' (USE WITH CAUTION!).
```

## ⚠️ Important Notes

*   **Deletion is not implemented**: For safety, this version of the utility only *reports* findings. It does not automatically delete any files. You must review the report and perform deletions manually.
*   **Symlinks are skipped**: To prevent unintended scans or issues, symbolic links are ignored during the scan.
*   **Error Handling**: The utility attempts to gracefully handle unreadable files or directories, printing warnings instead of crashing.

Keep your digital space clean and efficient with the Digital Dust Bunny Sweeper!
