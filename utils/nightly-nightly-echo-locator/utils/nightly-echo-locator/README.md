# Nightly Echo-Locator

## 📡 Unearthing Redundancy in the Ruins 📡

The Nightly Echo-Locator is a crucial utility for the discerning scavenger of the digital wasteland. In the chaos of the apocalypse, duplicate files can lurk in the darkest corners of your repository, consuming precious space and sowing confusion. This tool helps you identify and report files with identical content, allowing you to consolidate and streamline your digital hoard.

### Features

*   **Deep Scan**: Recursively traverses specified directories to find all files.
*   **Content-Based Hashing**: Uses SHA256 to accurately identify files with identical content, regardless of their name or location.
*   **Clear Reporting**: Presents a grouped list of duplicate files, making it easy to see which files are redundant.

### Usage

```bash
python src/echo_locator.py <directory_path>
```

**Example:**

```bash
python src/echo_locator.py .
```

This will scan the current directory and its subdirectories for duplicate files and print a report to the console.

### Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are strictly required beyond standard library modules.

### How it Works

1.  The script takes a root directory as an argument.
2.  It walks through all files in the specified directory and its subdirectories.
3.  For each file, it calculates a SHA256 hash of its content.
4.  It stores file paths, grouped by their content hash.
5.  Finally, it iterates through the groups and reports any hash that corresponds to more than one file path, indicating duplicates.

### Contributing

Found a bug or have an idea for an improvement? Feel free to open an issue or submit a pull request!
