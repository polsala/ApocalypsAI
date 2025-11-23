# Nightly Cosmic Dust Collector

## 🌌 Overview

The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help you keep your digital workspace tidy. It scans specified directories for files that meet certain criteria for 'cosmic dust' – typically small, old, or empty files that might be forgotten artifacts, temporary leftovers, or just general clutter. Once identified, these files can either be listed for your review or automatically moved to a designated 'cosmic dustbin' directory.

Think of it as a tiny, automated digital broom, sweeping away the detritus of your daily coding adventures.

## ✨ Features

*   **Flexible Scanning**: Define criteria for what constitutes 'dust' (maximum size, minimum age, emptiness).
*   **Two Modes**: `list` to simply report findings, or `move` to relocate files to a dedicated `cosmic_dustbin`.
*   **Self-Contained**: A single Python script with no external dependencies beyond the standard library.

## 🚀 Usage

To run the Cosmic Dust Collector, navigate to its directory and execute the `dust_collector.py` script with the target directory and desired options.

```bash
python3 src/dust_collector.py <target_directory> [options]
```

### Arguments

*   `<target_directory>`: The root directory to scan for cosmic dust. This is a required positional argument.

### Options

*   `--max-size-kb <int>`: Maximum file size in kilobytes (KB) to consider a file 'dust'. Files larger than this will be ignored. Default: `1` (1KB).
*   `--min-age-days <int>`: Minimum age in days for a file to be considered 'dust'. Files younger than this will be ignored. Default: `30` (30 days).
*   `--action <list|move>`: The action to perform. 
    *   `list`: (Default) Prints the paths of identified dust files.
    *   `move`: Moves identified dust files to a `cosmic_dustbin` subdirectory within the target directory.
*   `--dustbin-dir <name>`: The name of the subdirectory to create and move files into if `--action` is `move`. Default: `cosmic_dustbin`.

### Examples

1.  **List all files under `my_project/` that are empty or older than 60 days and smaller than 5KB:**
    ```bash
    python3 src/dust_collector.py my_project/ --max-size-kb 5 --min-age-days 60 --action list
    ```

2.  **Move all files under `downloads/` that are older than 90 days and smaller than 10KB to a custom dustbin named `old_junk/`:**
    ```bash
    python3 src/dust_collector.py downloads/ --max-size-kb 10 --min-age-days 90 --action move --dustbin-dir old_junk
    ```

3.  **Find only empty files in the current directory:**
    ```bash
    python3 src/dust_collector.py . --max-size-kb 999999 --min-age-days 0 --action list
    ```
    *(Note: Setting `max-size-kb` very high and `min-age-days` to 0 effectively makes only 'empty' the primary criterion, though small files will still be caught if they are also empty.)*

## 🧪 Testing

To run the tests for the Cosmic Dust Collector, use the Python `unittest` module:

```bash
python3 -m unittest tests/test_dust_collector.py
```
