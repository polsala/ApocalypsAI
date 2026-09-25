# Nightly Digital Dust Bunny Sweeper

## 🧹 Overview

Welcome, digital archivist! The `nightly-digital-dust-bunny-sweeper` is a whimsical-yet-useful command-line interface (CLI) tool designed to help you keep your digital realm tidy. It scans specified directories for "digital dust bunnies" – files that are either significantly old or whose names match common patterns associated with temporary, backup, or forgotten data. Think of it as a friendly, automated broom for your file system.

This utility provides a report of potentially clutter-inducing files, allowing you to review them for archiving, deletion, or further action, helping you reclaim precious digital space and mental clarity.

## ✨ Features

*   **Age-based Detection**: Identifies files older than a configurable threshold.
*   **Pattern Matching**: Flags files whose names contain specified "dust bunny" patterns (e.g., `temp`, `backup`, `copy`).
*   **Recursive Scanning**: Option to delve into subdirectories for a thorough sweep.
*   **Configurable Thresholds**: Customize age and pattern lists to suit your needs.
*   **Clear Reporting**: Outputs a sorted list of dusty files with suggestions.
*   **Type-Safe**: Built with TypeScript for robust and maintainable code.

## 🚀 Installation

To use the Digital Dust Bunny Sweeper, you'll need Node.js (which includes npm) installed on your system.

1.  Navigate to the `typescript-utils/nightly-digital-dust-bunny-sweeper` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Build the TypeScript project:
    ```bash
    npm run build
    ```

## 💡 Usage

Run the sweeper from the utility's root directory, specifying the target directory you wish to clean.

```bash
node dist/cli.js <directory_to_scan> [options]
```

### Arguments

*   `<directory_to_scan>`: The path to the directory you want to sweep. This is a required argument.

### Options

*   `-a, --age <days>`: Minimum age in days for a file to be considered dusty. Files older than this will be flagged. (Default: `90`)
*   `-p, --patterns <list>`: A comma-separated list of filename substrings (patterns) to look for. Files containing any of these patterns will be flagged. (Default: `temp,backup,copy,old`)
*   `-r, --recursive`: Scan directories recursively. If not set, only the top-level directory will be scanned. (Default: `false`)
*   `-f, --format <type>`: Output format for the report. Can be `text` or `json`. (Default: `text`)
*   `-s, --min-score <score>`: Minimum "dust score" for a file to be reported. Each matching pattern adds 1 to the score. (Default: `1`)

### Examples

1.  **Basic sweep of current directory, default options:**
    ```bash
    node dist/cli.js .
    ```

2.  **Scan a specific directory recursively, flagging files older than 180 days:**
    ```bash
    node dist/cli.js /path/to/my/documents --recursive --age 180
    ```

3.  **Find files with custom patterns and output as JSON:**
    ```bash
    node dist/cli.js ~/Downloads --patterns "archive,legacy,draft" --format json
    ```

4.  **Find files with a high dust score (e.g., matching multiple patterns):**
    ```bash
    node dist/cli.js /var/log --min-score 2
    ```

## ⚙️ Configuration

The default configuration can be overridden using command-line options. The `dustPatterns` are simple substring matches for whimsy and simplicity. For more complex pattern matching, consider enhancing the `calculateDustScore` method in `src/index.ts`.

## 🧪 Development & Testing

To run the automated tests:

```bash
npm test
```

This will execute the Jest test suite, which uses mocks for file system operations to ensure deterministic and offline testing.
