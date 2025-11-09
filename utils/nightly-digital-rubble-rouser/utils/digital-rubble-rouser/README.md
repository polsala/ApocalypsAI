# Digital Rubble Rouser

## 🧹 Clear Out the Digital Debris!

In the post-apocalyptic digital landscape, storage space is a precious commodity. The **Digital Rubble Rouser** is your trusty companion for sifting through the forgotten corners of your file system, identifying old or excessively large files that are hogging valuable space. It doesn't delete anything; it just points out the 'rubble' so you can decide what to salvage or scrap.

### ✨ Features

*   **Age-based Scanning**: Find files older than a specified number of days.
*   **Size-based Scanning**: Pinpoint files larger than a given megabyte threshold.
*   **Recursive Search**: Dive deep into subdirectories or stick to the surface.
*   **Safe Operation**: Only lists files; never modifies or deletes them.

### 🚀 Usage

Run the utility from your terminal, providing a directory path and at least one criterion (`--age` or `--size`).

```bash
python src/rubble_rouser.py <path_to_directory> [--age <days>] [--size <MB>] [--recursive]
```

**Arguments:**

*   `<path_to_directory>`: The starting directory to scan.
*   `--age <days>`: (Optional) List files older than this many days.
*   `--size <MB>`: (Optional) List files larger than this many megabytes (MB).
*   `--recursive`: (Optional) Scan subdirectories recursively. If omitted, only the top-level directory is scanned.

**Examples:**

1.  **Find all files in `~/Downloads` older than 365 days:**
    ```bash
    python src/rubble_rouser.py ~/Downloads --age 365
    ```

2.  **Find all files in `~/Documents` larger than 500MB (non-recursive):**
    ```bash
    python src/rubble_rouser.py ~/Documents --size 500
    ```

3.  **Recursively find files in `/var/log` older than 90 days AND larger than 10MB:**
    ```bash
    python src/rubble_rouser.py /var/log --age 90 --size 10 --recursive
    ```

### 📦 Output

The utility will print a list of identified 'rubble' files, including their full path, size in MB, and last modification date. If no rubble is found, it will let you know your digital space is pristine!

```
Scanning '/home/user/my_data' for digital rubble...

--- Identified Digital Rubble ---
  Path: /home/user/my_data/old_backup.zip
    Size: 1234.56 MB
    Last Modified: 2022-01-15 10:30:00
------------------------------
  Path: /home/user/my_data/temp/large_log.txt
    Size: 50.12 MB
    Last Modified: 2023-03-20 14:05:10
------------------------------

Found 2 pieces of digital rubble.
Consider reviewing these files for potential cleanup.
```
