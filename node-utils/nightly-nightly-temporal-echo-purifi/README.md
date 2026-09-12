# Nightly Temporal Echo Purifier

## Overview

The `nightly-temporal-echo-purifier` is a whimsical-yet-useful utility designed to help you identify and manage digital clutter. It scans a specified directory for "temporal echoes" – files that haven't been modified or accessed in a long time – and provides a report with suggested "purification" actions. Think of it as a digital archaeologist, unearthing forgotten data and helping you decide its fate.

This tool is non-destructive by default, operating in a dry-run mode to simply report its findings. You can then manually decide to archive, delete, or simply acknowledge the echoes.

## Features

*   **Echo Detection**: Scans a target directory for files older than a specified age.
*   **Whimsical Reporting**: Presents findings with a touch of post-apocalyptic charm.
*   **Non-Destructive**: Always runs in dry-run mode, suggesting actions without performing them.
*   **Cross-Platform**: Built with Node.js, it runs wherever Node.js is supported.

## Installation

1.  Ensure you have Node.js (v14 or higher) installed.
2.  Clone the ApocalypsAI repository or navigate to this utility's directory:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-temporal-echo-purifier
    ```
3.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

Run the utility from its directory, specifying the path to scan and the maximum age (in days) for files to be considered "echoes".

```bash
node src/index.js --path /path/to/your/directory --age 90
```

### Arguments:

*   `--path <directory>`: **Required**. The absolute or relative path to the directory to scan.
*   `--age <days>`: **Required**. Files older than this many days will be considered temporal echoes.

### Example:

To find files older than 180 days in your `~/Downloads` folder:

```bash
node src/index.js --path ~/Downloads --age 180
```

## Development & Testing

To run the automated tests:

```bash
npm test
```
