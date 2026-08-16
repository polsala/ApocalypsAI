# Nightly Byte-Breeze Whisperer

The digital world is vast, and sometimes, files get lost in the currents of time, accumulating "digital dust" in forgotten corners of your storage. The `Nightly Byte-Breeze Whisperer` is a whimsical utility designed to help you rediscover these long-neglected digital relics. It scans specified directories, calculates a "digital dust" score based on how long files have been untouched, and whispers their names to you, suggesting they might be ready for review, archiving, or perhaps a final, respectful deletion.

Let the Byte-Breeze guide you to a cleaner, more organized digital realm!

## Features

*   **Digital Dust Scoring**: Files are assigned a "dust score" based on their modification and access times, indicating how long they've been forgotten.
*   **Recursive Scanning**: Explores subdirectories to uncover hidden gems (or forgotten junk).
*   **Configurable Threshold**: Set a minimum "dust age" to focus only on truly ancient files.
*   **Whimsical Output**: Presents findings with a touch of ApocalypsAI charm.

## Installation

This is a Node.js utility. Ensure you have Node.js (v14 or higher recommended) installed.

1.  **Clone the repository (if not already done):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-byte-breeze-whisperer
    ```
2.  **Install dependencies (for testing, the utility itself is dependency-free):**
    ```bash
    npm install
    ```

## Usage

Run the utility from your terminal, providing the directory you wish to scan and an optional minimum dust age in days.

```bash
node src/index.js <directory_to_scan> [minimum_dust_days]
```

*   `<directory_to_scan>`: The absolute or relative path to the directory you want the Byte-Breeze to whisper through.
*   `[minimum_dust_days]`: (Optional) The minimum number of days a file must be "forgotten" to be reported. Defaults to `90` days if not specified or invalid.

### Examples

**Scan your `Documents` folder for files older than 90 days (default):**

```bash
node src/index.js ~/Documents
```

**Scan your `Downloads` folder for files older than 365 days:**

```bash
node src/index.js /Users/youruser/Downloads 365
```

**Scan the current directory for files older than 180 days:**

```bash
node src/index.js . 180
```

## Output

The utility will print a list of files that meet your specified "digital dust" threshold, sorted from most forgotten to least.

```
Scanning '/path/to/scan' for files with at least 90 days of digital dust...

The Byte-Breeze whispers about these forgotten files:

[Digital Dust: 730 days] /path/to/scan/old_project/notes.txt
[Digital Dust: 500 days] /path/to/scan/temp/backup.zip
[Digital Dust: 180 days] /path/to/scan/images/holiday_2020.jpg

Consider reviewing or archiving these digital relics.
```

If no forgotten files are found, the Byte-Breeze will assure you that "All is well!"

## Development & Testing

To run the automated tests:

1.  Ensure you have installed dependencies as per the Installation section.
2.  Run the tests from the utility's root directory:
    ```bash
    npm test
    ```

The tests use mocks for `fs.promises` to ensure they are deterministic and do not interact with the actual file system.
