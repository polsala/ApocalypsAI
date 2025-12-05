# Nightly Digital Dust Bunny Destroyer

## 🧹 Sweep Away the Digital Grime!

In the chaotic aftermath of the digital apocalypse, even your file system can accumulate unsightly 'dust bunnies' – empty directories, forgotten temporary files, and broken links that serve no purpose. The **Nightly Digital Dust Bunny Destroyer** is here to bring order to the digital rubble, ensuring your precious storage space is optimized and your pathways are clear.

This utility scans a specified directory, identifying and eliminating common forms of digital clutter, making your system feel lighter and more efficient. Think of it as your personal digital janitor, working tirelessly to maintain a pristine environment.

## ✨ Features

*   **Empty Directory Exterminator**: Recursively finds and removes empty folders.
*   **Old Temp File Purger**: Deletes temporary files (based on common patterns and age) that have overstayed their welcome.
*   **Broken Symlink Buster**: Identifies and removes symbolic links that point to non-existent targets.

## 🚀 Usage

1.  **Navigate**: Change into the `src` directory:
    ```bash
    cd utils/nightly-digital-dust-bunny-destroyer/src
    ```
2.  **Run**: Execute the `destroyer.py` script with the target directory and optional parameters:
    ```bash
    python destroyer.py --path /path/to/your/messy/directory --age 30
    ```

### Parameters:

*   `--path <directory>`: **Required**. The root directory to scan and clean.
*   `--age <days>`: Optional. Number of days after which temporary files are considered 'old'. Defaults to 7 days.
*   `--dry-run`: Optional. If present, the utility will only report what it *would* do, without making any changes.

## 🛠️ Development

To run tests:

1.  **Navigate**: Change into the `tests` directory:
    ```bash
    cd utils/nightly-digital-dust-bunny-destroyer/tests
    ```
2.  **Run**: Execute `pytest` (or `python -m unittest`):
    ```bash
    python -m unittest test_destroyer.py
    ```
