# Digital Dust Bunny Sweeper

## 🧹 What is this?

In the digital catacombs of your file system, tiny, forgotten files accumulate, much like dust bunnies under a forgotten server rack. The "Digital Dust Bunny Sweeper" is a whimsical yet practical utility designed to help you identify and declutter these digital remnants. It scans a specified directory for files that are both older than a given age and larger than a certain size, presenting them as candidates for deletion. Think of it as a friendly robot vacuum for your hard drive, but it only points out the fluff, never actually sucks it up without your explicit command.

## ✨ Features

*   **Age-based Filtering**: Identify files older than a specified number of days.
*   **Size-based Filtering**: Pinpoint files larger than a certain byte threshold.
*   **Dry Run**: Always operates in a dry-run mode, suggesting files without ever deleting them.
*   **Recursive Scan**: Traverses subdirectories to find hidden dust bunnies.
*   **Clear Output**: Presents a list of "dust bunnies" with their path, age, and size.

## 🚀 How to Use

1.  **Navigate**: Change into the `src` directory:
    ```bash
    cd utils/digital-dust-bunny-sweeper/src
    ```
2.  **Run**: Execute the Python script with the target directory and optional filters.

    ```bash
    python dust_bunny_sweeper.py --path /path/to/scan --older-than-days 30 --larger-than-bytes 1048576
    ```

    *   `--path <directory>`: **Required**. The directory to scan for digital dust bunnies.
    *   `--older-than-days <int>`: **Optional**. Only show files older than this many days. Default: `365` (1 year).
    *   `--larger-than-bytes <int>`: **Optional**. Only show files larger than this many bytes. Default: `1048576` (1 MB).

### Example

To find all files in your `~/Downloads` directory that are older than 90 days and larger than 50MB:

```bash
python dust_bunny_sweeper.py --path ~/Downloads --older-than-days 90 --larger-than-bytes 52428800
```

## 🧪 Development & Testing

To run the tests, navigate to the `tests` directory and execute:

```bash
cd utils/digital-dust-bunny-sweeper/tests
python -m unittest test_dust_bunny_sweeper.py
```
