# Nightly Signal Scavenger's Data Digger

A whimsical-yet-useful command-line utility for the ApocalypsAI community to scavenge and extract specific data patterns (e.g., URLs, emails, custom regex) from text files. Think of it as your digital metal detector for finding valuable signals amidst the digital rubble.

## Features

*   **Predefined Patterns**: Easily extract common patterns like URLs and email addresses.
*   **Custom Regex Support**: Define your own regular expressions for highly specific data extraction.
*   **Multiple File Processing**: Scavenge data from one or many text files in a single run.
*   **Output Options**: Print extracted data directly to the console or save it to an output file.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

1.  Navigate to the `utils/nightly-signal-scavenger-data-digger/` directory.
2.  The main script is `src/scavenger.py`.

## Usage

Run the `scavenger.py` script from your terminal.

```bash
python src/scavenger.py [OPTIONS] FILE [FILE...]
```

### Arguments

*   `FILE [FILE...]`: One or more text files to process.

### Options

*   `-t, --type {url,email}`: Predefined pattern type to extract. Choose from `url` or `email`.
*   `-r, --regex REGEX`: Custom regular expression to use for extraction. This option overrides `--type` if both are provided.
*   `-o, --output FILE`: Path to an output file where extracted data will be written. If not specified, data is printed to standard output.

### Examples

1.  **Extract all URLs from a single file and print to console:**

    ```bash
    python src/scavenger.py my_log_file.txt --type url
    ```

2.  **Extract all email addresses from multiple files and save to an output file:**

    ```bash
    python src/scavenger.py report1.txt report2.txt --type email --output extracted_emails.txt
    ```

3.  **Use a custom regex to find specific IDs (e.g., `ABC-123`) from a document:**

    ```bash
    python src/scavenger.py inventory.md --regex "[A-Z]{3}-\d{3}"
    ```

4.  **Combine multiple files with a custom regex, outputting to a file:**

    ```bash
    python src/scavenger.py data/*.txt --regex "ERROR: \d{4}" --output errors.log
    ```

## Development & Testing

To run the tests, navigate to the utility's root directory (`utils/nightly-signal-scavenger-data-digger/`) and execute:

```bash
python -m unittest tests/test_scavenger.py
```

All tests are deterministic and use mocks to simulate file system interactions, ensuring they run offline and reliably.
