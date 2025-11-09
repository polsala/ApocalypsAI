# Digital Dust Bunny Sweeper

## 🧹 Overview

The Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to help you declutter your digital workspace. It scans a specified directory for "digital dust bunnies" – files and folders that might be taking up unnecessary space or are simply remnants of past operations. Think of it as a friendly robot vacuum for your file system!

It identifies:
*   **Empty Files**: Files with zero bytes, just sitting there.
*   **Empty Directories**: Folders that contain no files or subdirectories.
*   **Temporary & Backup Files**: Files with common temporary or backup extensions (e.g., `.tmp`, `.bak`, `~`, `.log`, `.old`, `.swp`).
*   **Ancient Files**: Regular files that haven't been modified in a long, long time (default: 90 days).

## ✨ How to Use

1.  **Navigate**: Change your directory to `utils/digital-dust-bunny-sweeper/`.
2.  **Run**: Execute the `sweeper.py` script with the path you wish to scan.

    ```bash
    python src/sweeper.py /path/to/your/directory
    ```

    You can also specify an optional age threshold in days for "Ancient Files":

    ```bash
    python src/sweeper.py /path/to/your/directory 180
    ```
    (This would mark files older than 180 days as ancient.)

## 📜 Example Report

```
--- Digital Dust Bunny Sweeper Report for '/home/user/my_project' ---

Greetings, brave maintainer! Your digital realm has been scanned for lurking dust bunnies.
Fear not, for we have uncovered their hiding spots!

🕳️ Empty Files (1): These files are just taking up space, dreaming of content.
  - /home/user/my_project/data/empty_config.json

🚪 Empty Directories (1): Echoing chambers of forgotten data.
  - /home/user/my_project/old_assets/

⏳ Temporary & Backup Files (2): These were just visiting, now they're overstaying their welcome.
  - /home/user/my_project/temp_build.tmp
  - /home/user/my_project/main.py.bak

👴 Ancient Files (1): Relics from a bygone era, perhaps it's time to archive them?
  - /home/user/my_project/docs/legacy_notes.md

🧹 Total Digital Dust Bunnies Found: 5
Consider giving them a good sweep!

--- End of Report ---
```

## ⚠️ Disclaimer

This utility only *reports* on potential dust bunnies; it does **not** delete or modify any files. It's up to you to review the report and decide what to clean up! Always back up important data before performing any cleanup operations.
