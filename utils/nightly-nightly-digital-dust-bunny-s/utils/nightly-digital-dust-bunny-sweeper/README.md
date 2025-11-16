# Nightly Digital Dust Bunny Sweeper

## 🧹 What is this?

The `Nightly Digital Dust Bunny Sweeper` is a whimsical-yet-useful utility designed to help you keep your project directories tidy. It scans a specified path for common "digital dust bunnies" – those small, often forgotten, and sometimes numerous files and folders that accumulate over time, cluttering your workspace.

## ✨ Features

Currently, the sweeper identifies and reports:

*   **Empty Directories**: Folders that contain no files or subdirectories.
*   **`__pycache__` Directories**: Python's temporary bytecode compilation folders.

## 🚀 How to Use

1.  **Navigate** to the `utils/nightly-digital-dust-bunny-sweeper/` directory.
2.  **Run** the `sweeper.py` script with the path you want to scan:

    ```bash
    python3 src/sweeper.py /path/to/your/project
    ```

    Replace `/path/to/your/project` with the actual directory you wish to clean.

### Example Output:

```
Scanning '/my/project' for digital dust bunnies...

--- Digital Dust Bunnies Report ---

Empty Directories Found:
- /my/project/data/temp_logs
- /my/project/old_assets/unused_images

__pycache__ Directories Found:
- /my/project/src/__pycache__
- /my/project/tests/__pycache__

--- End Report ---
```

## 🔮 Future Plans

*   **Interactive Cleaning**: Add an option (`--clean` flag) to automatically delete identified dust bunnies after user confirmation.
*   **More Dust Bunny Types**: Expand detection to include:
    *   Orphaned symbolic links.
    *   Common OS junk files (e.g., `.DS_Store`, `Thumbs.db`).
    *   Old log files or temporary files with specific extensions.
*   **Configuration**: Allow users to specify custom patterns for files/directories to ignore or include.
