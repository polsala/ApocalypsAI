# Nightly Chrono-Shift File Renamer

## 🌌 About

The digital realm is a chaotic place, and files often lose their temporal context. The **Nightly Chrono-Shift File Renamer** is here to bring order to the temporal disarray! This whimsical utility scans a specified directory and, like a diligent archivist, prepends the last modification date (in `YYYY-MM-DD` format) to each file's name. This helps you instantly understand when a file was last touched, making chronological organization a breeze.

No more guessing when that `document.txt` was last updated – now it's `2023-10-27_document.txt`!

## ✨ Features

*   **Date Prepending**: Automatically adds the last modification date to filenames.
*   **Dry Run Mode**: Preview changes before committing to them.
*   **Idempotent**: Skips files that already have a `YYYY-MM-DD_` prefix, preventing duplicate renaming.
*   **Directory Skipping**: Intelligently ignores subdirectories, focusing only on files.

## 🚀 Usage

### Prerequisites

*   Python 3.6+

### Running the Renamer

1.  Navigate to the `src` directory:
    ```bash
    cd utils/nightly-chrono-shift-file-renamer/src
    ```
2.  Run the script, providing the target directory:

    ```bash
    python renamer.py --directory /path/to/your/files
    ```

    To see what changes would be made without actually renaming anything (highly recommended first!):

    ```bash
    python renamer.py --directory /path/to/your/files --dry-run
    ```

### Command Line Arguments

*   `--directory <path>` (required): The path to the directory containing files to be renamed.
*   `--dry-run`: If present, the utility will only print what it *would* do, without making any actual changes.

## 🧪 Testing

To run the tests, navigate to the `tests` directory and execute:

```bash
cd utils/nightly-chrono-shift-file-renamer/tests
python -m unittest test_renamer.py
```
