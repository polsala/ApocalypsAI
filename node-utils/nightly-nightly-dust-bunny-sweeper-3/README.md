# Nightly Temporal Dust Bunny Sweeper

## Overview

The `Nightly Temporal Dust Bunny Sweeper` is a whimsical-yet-useful utility designed to help you identify and manage "temporal dust bunnies" – files in your project directories that haven't been touched in a long, long time. Just like physical dust bunnies accumulate in forgotten corners, digital files can become stale, forgotten, and contribute to clutter. This tool scans your specified directory, recursively, and reports files based on their last modification date, categorizing their "dustiness" to help you decide what to review, archive, or delete.

Keep your digital workspace sparkling clean and free of ancient relics!

## Features

*   **Recursive Scanning**: Traverses subdirectories to find all hidden dust bunnies.
*   **Dustiness Classification**: Categorizes files into "Mildly Dusty", "Very Dusty", and "Ancient Relic" based on configurable thresholds.
*   **Clear Reporting**: Provides a list of identified files with their last modification date and dustiness level.
*   **Cross-Platform**: Built with Node.js, it runs wherever Node.js is supported.

## Installation

1.  **Ensure Node.js is installed**: If you don't have Node.js, download and install it from [nodejs.org](https://nodejs.org/).
2.  **Clone the repository (or copy the utility)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-dust-bunny-sweeper
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```

## Usage

Run the utility from your terminal.

```bash
npm start [directory_path] [threshold_days]
```

*   `directory_path` (optional): The path to the directory you want to scan. Defaults to the current directory (`.`).
*   `threshold_days` (optional): The number of days after which a file is considered "Very Dusty". Defaults to `90` days.

### Examples

**Scan the current directory with default thresholds (90 days for 'Very Dusty'):**

```bash
npm start
```

**Scan a specific project directory, considering files older than 60 days as 'Very Dusty':**

```bash
npm start /path/to/your/project 60
```

**Scan your home directory for files older than a year (365 days):**

```bash
npm start ~/ 365
```

### Dustiness Levels Explained

The utility uses the `threshold_days` parameter to define the "Very Dusty" level.
*   **Fresh (not dusty)**: Files modified within `threshold_days / 2` (e.g., 45 days if threshold is 90).
*   **Mildly Dusty**: Files modified between `threshold_days / 2` and `threshold_days` (e.g., 45-90 days).
*   **Very Dusty**: Files modified between `threshold_days` and `threshold_days * 3` (e.g., 90-270 days).
*   **Ancient Relic (very dusty)**: Files modified more than `threshold_days * 3` ago (e.g., over 270 days).

## Development & Testing

To run the automated tests:

```bash
npm test
```

This utility uses `jest` for testing. The tests are deterministic and offline, mocking the file system operations to ensure consistent results.
