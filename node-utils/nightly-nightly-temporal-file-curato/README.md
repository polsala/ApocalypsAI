# Nightly Temporal File Curator

A Node.js CLI utility designed to help survivors (and their digital archives) manage the inevitable temporal decay of files. This tool scans a specified directory, identifies files based on their last modified date (their "temporal signature"), and provides whimsical-yet-actionable recommendations for archival, review, or purge.

Think of it as your personal digital archaeologist, helping you sort through the digital detritus of the past to preserve what truly matters for the future.

## Features

*   **Temporal Decay Analysis**: Categorizes files into "Freshly Manifested," "Moderately Decayed," and "Deeply Decayed" based on a configurable age threshold.
*   **Curator's Report**: Generates a detailed report with recommendations for each category, guiding your archival strategies.
*   **Cross-Platform**: Built with Node.js, it runs wherever Node.js runs (Windows, macOS, Linux).
*   **Whimsical Theming**: Embraces the ApocalypsAI aesthetic with themed output and recommendations.

## Installation

1.  **Ensure Node.js is installed**: You need Node.js (v14 or higher recommended) to run this utility. Download it from [nodejs.org](https://nodejs.org/).
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-temporal-file-curator
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```
    (Note: This utility uses only built-in Node.js modules for its core functionality. `jest` is a dev dependency for testing. `npm install` is primarily for `jest` if you want to run tests.)

## Usage

Run the utility from your terminal, providing the directory path to scan and the age threshold in days.

```bash
node src/index.js <directory_path> <age_threshold_in_days>
```

### Arguments

*   `<directory_path>`: The absolute or relative path to the directory you wish to scan.
*   `<age_threshold_in_days>`: An integer representing the number of days. Files older than this threshold will be considered "decayed." Files older than *twice* this threshold will be "deeply decayed."

### Examples

1.  **Scan your current directory for files older than 90 days:**
    ```bash
    node src/index.js . 90
    ```

2.  **Scan a specific archive directory for files older than 365 days:**
    ```bash
    node src/index.js /path/to/your/archives 365
    ```

## Curator's Report Interpretation

The report will categorize files and offer recommendations:

*   **Freshly Manifested Artifacts**: Files within the `age_threshold_in_days`.
    *   *Recommendation*: "No immediate action. Continue monitoring temporal integrity."
*   **Moderately Decayed Artifacts**: Files older than `age_threshold_in_days` but younger than `2 * age_threshold_in_days`.
    *   *Recommendation*: "Review for 'Archive' to 'Stasis Chamber' or 'Re-evaluation'."
*   **Deeply Decayed Artifacts**: Files older than `2 * age_threshold_in_days`.
    *   *Recommendation*: "Immediate Archival to 'Temporal Vault' or 'Void Purge'."

## Development & Testing

To run the automated tests:

```bash
npm test
```

The tests use `jest` and mock the file system (`fs.promises`) and `Date.now()` to ensure deterministic and isolated execution without actual file system interaction.

## Contributing

Contributions are welcome! If you have ideas for new temporal decay categories, archival strategies, or general improvements, please open an issue or submit a pull request.
