# Nightly Byte-Sized Snack Dispenser

## 🍽️ Overview

The Nightly Byte-Sized Snack Dispenser is a handy utility for when you're faced with a colossal file (think log files, massive CSVs, or ancient data dumps) and just need a quick taste, not the whole feast. It allows you to extract a "snack-sized" sample of lines based on various criteria, making quick inspections a breeze without overwhelming your system or your brain.

No more waiting for huge files to load just to peek at the beginning, end, or a few random entries!

## ✨ Features

*   **First N Lines**: Grab the initial lines of a file.
*   **Last N Lines**: Fetch the concluding lines of a file.
*   **Random N Lines**: Pick a random selection of lines from anywhere in the file.
*   **Pattern Match (Grep-like)**: Extract all lines that contain a specific string or regex pattern.
*   **Memory Efficient**: Designed to handle very large files by processing them line-by-line.
*   **Output Flexibility**: Print to standard output or save to a new file.

## 🚀 Usage

```bash
python src/dispenser.py <file_path> --method <first|last|random|grep> [options]
```

### Examples:

1.  **Get the first 10 lines:**
    ```bash
    python src/dispenser.py my_big_log.log --method first --count 10
    ```

2.  **Get the last 5 lines and save to a new file:**
    ```bash
    python src/dispenser.py data.csv --method last --count 5 --output last_5_data.csv
    ```

3.  **Get 3 random lines:**
    ```bash
    python src/dispenser.py access.log --method random --count 3
    ```

4.  **Find all lines containing "ERROR" and print to console:**
    ```bash
    python src/dispenser.py app.log --method grep --pattern "ERROR"
    ```

5.  **Find all lines matching a regex pattern and save to a file:**
    ```bash
    python src/dispenser.py server.log --method grep --pattern "\[WARN\] user-\d+" --output warnings.log
    ```

### Arguments:

*   `<file_path>`: Path to the input file.
*   `--method <first|last|random|grep>`: The sampling method to use.
*   `--count <int>`: (Required for `first`, `last`, `random` methods) The number of lines to extract.
*   `--pattern <string>`: (Required for `grep` method) The string or regex pattern to search for.
*   `--output <file_path>`: (Optional) Path to save the extracted lines. If not provided, output goes to stdout.

## 🛠️ Development

This utility is written in Python 3.11 and is self-contained. No external dependencies are required beyond the standard library.

### Running Tests:

```bash
python -m unittest tests/test_dispenser.py
```
