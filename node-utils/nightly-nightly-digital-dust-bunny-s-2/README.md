# Nightly Digital Dust Bunny Sweeper

## Summary

In the post-apocalyptic digital wasteland, files accumulate like dust, slowing down your systems and obscuring vital information. The `nightly-digital-dust-bunny-sweeper` is your trusty Node.js CLI companion, designed to scour specified directories for "digital dust bunnies" – files that haven't been modified in a long, long time. It helps you identify these forgotten relics so you can decide whether to sweep them into the void, quarantine them for later inspection, or simply acknowledge their continued existence.

## Installation

1.  **Ensure Node.js is installed**: This utility requires Node.js (v14 or higher).
    If you don't have it, download it from [nodejs.org](https://nodejs.org/).

2.  **Clone the repository (or download the utility)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-digital-dust-bunny-sweeper
    ```

3.  **No external dependencies**: This utility uses only built-in Node.js modules, so no `npm install` is required within its directory.

## Usage

Run the script directly using `node` and provide the target directory path and the threshold in days.

```bash
node src/index.js <directory_path> <threshold_days>
```

-   `<directory_path>`: The absolute or relative path to the directory you want to scan.
-   `<threshold_days>`: The number of days. Files not modified within this many days will be considered "digital dust bunnies".

### Examples

1.  **Scan your current project directory for files older than 90 days:**
    ```bash
    node src/index.2js . 90
    ```

2.  **Scan a specific user directory for files older than 180 days:**
    ```bash
    node src/index.js /home/survivor/documents 180
    ```

3.  **Scan a server log directory for files older than 30 days:**
    ```bash
    node src/index.js /var/log/old_logs 30
    ```

## How it Works

The utility recursively traverses the specified directory. For each file encountered, it retrieves its last modification timestamp (`mtime`). If this timestamp is older than the calculated threshold date (current date minus `threshold_days`), the file is flagged as a "digital dust bunny" and reported.

Error handling is included to gracefully skip directories or files that cannot be accessed due to permissions or other issues, ensuring the scan continues where possible.

## Output

If no dust bunnies are found:

```
Scanning "./my_project" for digital dust bunnies older than 90 days...

✨ All clear! No digital dust bunnies found. Your digital sanctuary is pristine.
```

If dust bunnies are found:

```
Scanning "./my_project" for digital dust bunnies older than 90 days...

🚨 Digital Dust Bunnies Detected! These files are gathering virtual dust:
- /path/to/my_project/old_report.pdf (Last modified: 2023-01-15)
- /path/to/my_project/archive/ancient_data.zip (Last modified: 2022-11-01)
- /path/to/my_project/logs/debug_old.log (Last modified: 2023-02-28)

Consider sweeping these relics into the void or quarantining them for later inspection.
```

## Future Enhancements

-   Options to automatically `sweep` (delete) or `quarantine` (move to an archive directory) detected files.
-   Support for an `.ddbsignore` file to exclude specific paths or file patterns.
-   More detailed reporting formats (e.g., JSON, CSV).
-   Interactive mode for reviewing and acting on each detected file.
