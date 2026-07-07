# Nightly Digital Dust Bunny Sweeper

## Unearthing Forgotten Files with a Whimsical Touch

This utility helps you discover those long-forgotten files, affectionately dubbed "digital dust bunnies," that accumulate in your file system over time. It scans a specified directory (and its subdirectories) for files that haven't been modified in a given number of days and presents them in a charming report.

Keep your digital space tidy and free from the clutter of the past!

## Features

*   **Recursive Scanning**: Delves into subdirectories to find hidden gems (or dust bunnies).
*   **Age-Based Filtering**: Specify how old a file must be to be considered a "dust bunny."
*   **Whimsical Reporting**: Presents findings with a touch of charm.
*   **Safe**: Only reports files; never deletes or modifies anything.

## Installation

1.  Ensure you have Node.js installed (v14 or higher recommended).
2.  Clone this repository or download the `nightly-digital-dust-bunny` folder.
3.  Navigate into the `nightly-digital-dust-bunny` directory.
4.  Install dependencies for testing:
    ```bash
    npm install
    ```

## Usage

Run the script from your terminal:

```bash
node src/index.js <directory_path> [days_old]
```

*   `<directory_path>`: The path to the directory you want to scan. This is a required argument.
*   `[days_old]`: (Optional) The minimum age in days for a file to be considered a "dust bunny." Files modified more than this many days ago will be reported. Defaults to `90` days if not specified.

### Examples

Scan your current directory for files older than 90 days:
```bash
node src/index.js .
```

Scan your `~/Documents` directory for files older than 180 days:
```bash
node src/index.js ~/Documents 180
```

Scan a specific project folder for files older than 30 days:
```bash
node src/index.js /path/to/my/project 30
```

## Output

The utility will print a list of identified "digital dust bunnies," including their path, last modified date, and size.

```
🧹 Sweeping for digital dust bunnies in /path/to/scan...

Found 3 digital dust bunnies:

✨ /path/to/scan/old_report.pdf (Modified: 2023-01-15, Size: 1.2 MB) - 400 days old!
✨ /path/to/scan/archive/forgotten_script.js (Modified: 2022-11-01, Size: 50 KB) - 500 days old!
✨ /path/to/scan/temp/log_2023.txt (Modified: 2023-03-20, Size: 2.5 MB) - 350 days old!

Total dust bunnies found: 3. Time to consider a digital spring cleaning! 🧺
```

## Development & Testing

To run the tests, navigate to the utility's root directory and execute:

```bash
npm test
```
