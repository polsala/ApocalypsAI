# Digital Dust Bunny Sweeper

## 🧹 Whimsical Cleanup for Your Digital Lair 🧹

The Digital Dust Bunny Sweeper is a charming little utility designed to help you reclaim disk space by tidying up those pesky, forgotten temporary files, old logs, and cache directories that accumulate over time. Think of it as a tiny, diligent robot vacuum for your file system, but with a touch of personality!

It's safe, interactive, and always asks for permission before sweeping away your digital detritus.

## ✨ Features

*   **Whimsical Output**: Enjoy delightful messages as your system gets cleaned.
*   **Safe Dry Run**: Preview what will be deleted without making any changes.
*   **Interactive Confirmation**: You're always in control; confirm deletions before they happen.
*   **Configurable Paths**: Specify which directories to scan.
*   **Common Patterns**: Targets typical temporary files (`.tmp`, `.log`), cache folders (`cache/`, `__pycache__`), and more.

## 🚀 How to Use

1.  **Navigate to the utility directory**:
    ```bash
    cd utils/digital-dust-bunny-sweeper/
    ```

2.  **Run the sweeper**:

    The utility accepts one or more paths to scan. If no paths are provided, it will default to scanning the current working directory.

    ```bash
    python3 src/dust_bunny_sweeper.py [path1] [path2] ...
    ```

    **Example: Scan your home directory and a project folder**
    ```bash
    python3 src/dust_bunny_sweeper.py ~/Documents/MyProject /var/log/old_logs
    ```

3.  **Dry Run (Highly Recommended First!)**:

    Always start with a dry run to see what the sweeper *would* do without actually deleting anything.

    ```bash
    python3 src/dust_bunny_sweeper.py --dry-run ~/Documents/MyProject
    ```

4.  **Confirm Deletion**: 

    When not in dry-run mode, the sweeper will list detected 'dust bunnies' and ask for your confirmation before proceeding with deletion.

## ⚙️ Configuration (Advanced)

The utility currently uses a hardcoded list of common patterns. Future versions might include a configuration file for custom patterns and exclusions. For now, feel free to modify `src/dust_bunny_sweeper.py` directly to adjust the `DUST_BUNNY_PATTERNS` list.

## 🧪 Running Tests

To ensure the sweeper is working as expected and to verify its safety mechanisms, you can run the provided tests:

```bash
python3 -m unittest tests/test_dust_bunny_sweeper.py
```
