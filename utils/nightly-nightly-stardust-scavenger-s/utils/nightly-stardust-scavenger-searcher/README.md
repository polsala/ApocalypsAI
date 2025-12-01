# Nightly Stardust Scavenger Searcher

## Unearthing Digital Relics in the Post-Apocalyptic Data Wastes

The digital landscape is vast and often chaotic, especially after a few "minor" global resets. The Stardust Scavenger Searcher is your trusty companion for sifting through the digital rubble, helping you unearth valuable files based on patterns, size, and freshness. Think of it as a metal detector for your hard drive, but for data!

### Features

*   **Pattern Matching**: Search for files whose names match a regular expression.
*   **Size Filtering**: Pinpoint files within a specific size range (e.g., "only the really big ones" or "just the tiny fragments").
*   **Temporal Sifting**: Find files modified within a recent timeframe, ensuring you're looking at the freshest data.
*   **Prioritized Output**: Results are sorted to highlight potentially more "valuable" finds (e.g., newer and larger files first).

### Usage

```bash
python src/scavenger.py --directory <path/to/search> [OPTIONS]
```

#### Options:

*   `--directory <path>`: **Required**. The root directory to begin the scavenger hunt.
*   `--pattern <regex>`: Optional. A regular expression to match against file names (e.g., `.*\.log$` for log files).
*   `--min-size <bytes>`: Optional. Minimum file size in bytes.
*   `--max-size <bytes>`: Optional. Maximum file size in bytes.
*   `--max-age-days <days>`: Optional. Only include files modified within the last N days.
*   `--output-format <format>`: Optional. `json` or `text` (default: `text`).
*   `--help`: Show help message.

### Examples

1.  **Find all Python scripts modified in the last 7 days, larger than 1KB:**
    ```bash
    python src/scavenger.py --directory . --pattern ".*\.py$" --min-size 1024 --max-age-days 7
    ```

2.  **List all `.txt` files in a directory, output as JSON:**
    ```bash
    python src/scavenger.py --directory /var/log --pattern ".*\.txt$" --output-format json
    ```

### Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed beyond the standard library.

1.  Navigate to the `utils/nightly-stardust-scavenger-searcher` directory.
2.  Run `python src/scavenger.py --help` to see available options.

### Contributing

Feel free to suggest new filters, output formats, or even more whimsical prioritization algorithms!
