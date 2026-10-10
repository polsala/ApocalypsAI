# Nightly Data Echo Locator

## Summary
A whimsical Bash utility to detect and report duplicate files, framed as 'temporal data echoes' across your filesystem. It helps you identify redundant data that might be causing "temporal distortions" in your storage.

## Usage
To invoke the Nightly Data Echo Locator, simply provide the path to the directory you wish to scan for echoes:

```bash
./src/echo_locator.sh <directory_path>
```

**Example:**
```bash
./src/echo_locator.sh /home/user/my_precious_data
```

The script will output groups of files that have identical content, indicating they are "temporal echoes" of each other. Each group will be preceded by a blank line for readability.

## How it Works
The `echo_locator.sh` script performs the following steps:
1.  **Scans for Files**: It uses `find` to locate all regular files within the specified directory and its subdirectories.
2.  **Generates Checksums**: For each file, it calculates an MD5 checksum. This checksum acts as a unique "temporal signature" for the file's content.
3.  **Identifies Echoes**: It then groups files by their MD5 checksums. If multiple files share the same checksum, they are considered "temporal data echoes" – exact duplicates.
4.  **Reports Findings**: The script prints out these groups, showing the checksum and the full path to each echoing file.

## Running Tests
To ensure the Nightly Data Echo Locator is functioning correctly and its temporal sensors are calibrated, you can run the provided test suite:

```bash
./tests/test_echo_locator.sh
```

The tests will create temporary files and directories, simulate various scenarios (no duplicates, multiple duplicates, empty directories, invalid paths), and verify the script's output. All test artifacts are cleaned up automatically.

## Example Output
```
Initiating Temporal Data Echo Scan in: /path/to/your/data
--------------------------------------------------
92955523a1059434857500196235123d  /path/to/your/data/fileA.txt
92955523a1059434857500196235123d  /path/to/your/data/fileB.txt
92955523a1059434857500196235123d  /path/to/your/data/subdir/fileD.txt

# (If there were other duplicate groups, they would appear here, separated by a blank line)
```
