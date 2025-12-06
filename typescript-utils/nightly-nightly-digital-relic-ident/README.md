# Nightly Digital Relic Identifier

## Summary

The `nightly-digital-relic-ident` is a whimsical-yet-useful command-line utility that scans a specified directory and classifies its files based on their age, last access time, and size. It helps you identify 'digital relics' – files that might be ancient, forgotten, or simply taking up space, suggesting potential cleanup or archiving actions.

## Whimsical Categories

Files are categorized into:

*   **Ancient Relic**: Very old and untouched files.
*   **Forgotten Artifact**: Old but perhaps recently accessed or modified files.
*   **Recent Find**: Relatively new files that are not actively used.
*   **Active Data**: Recently modified or accessed files.

## Installation

1.  Ensure you have Node.js (v18+) and npm (or yarn) installed.
2.  Navigate to the `nightly-digital-relic-ident` directory.
3.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

Run the utility with `ts-node` followed by the path to the directory you want to scan.

```bash
# Scan the current directory with default thresholds
npx ts-node src/index.ts .

# Scan a specific directory with custom thresholds (e.g., 730 days for 'ancient', 180 days for 'forgotten', min size 100KB)
npx ts-node src/index.ts /path/to/your/data --ancient-days 730 --forgotten-days 180 --min-size-kb 100
```

### Command Line Arguments

*   `<directory>`: The path to the directory to scan. (Required)
*   `--ancient-days <number>`: Files older than this many days are considered 'Ancient Relics'. Default: `365`.
*   `--forgotten-days <number>`: Files older than this many days (but newer than `ancient-days`) are 'Forgotten Artifacts'. Default: `90`.
*   `--min-size-kb <number>`: Only classify files larger than this size in KB. Default: `0`.

## Example Output

```
Scanning directory: /home/user/documents
Configuration: Ancient > 365 days, Forgotten > 90 days, Min Size > 0 KB

--- Digital Relic Report ---

[Ancient Relic] /home/user/documents/old_thesis.pdf
    Reason: File is very old (750 days) and has not been modified or accessed recently.
[Forgotten Artifact] /home/user/documents/project_notes.txt
    Reason: File is old (120 days) but not ancient, and has not been modified or accessed recently.
[Active Data] /home/user/documents/current_work.docx
    Reason: File is recent (5 days) and actively used.
[Recent Find] /home/user/documents/downloaded_image.jpg
    Reason: File is relatively new (45 days) but has not been actively modified or accessed in the last 30 days.

--- Scan Complete ---
```
