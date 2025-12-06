# Nightly Data De-Crufter

## Purge Digital Detritus and Streamline Textual Data

In the digital wasteland, data often accumulates 'cruft' – unnecessary whitespace, empty lines, duplicates, or irrelevant entries. The Nightly Data De-Crufter is your essential tool for tidying up these textual anomalies, ensuring your data streams are clean, concise, and ready for analysis.

### Features:

*   **Whitespace Trimming**: Removes leading and trailing whitespace from each line.
*   **Empty Line Removal**: Eliminates lines that are entirely empty or contain only whitespace.
*   **Duplicate Line Purge**: Removes identical lines, preserving the order of their first appearance.
*   **Pattern-Based Filtering**: Discard lines that match a specified regular expression pattern (e.g., comments, specific log entries).
*   **Case Normalization**: Convert all text to lowercase, uppercase, or title case for consistency.

### Usage:

The `decrufter.py` script can read from an input file or `stdin` and write to an output file or `stdout`.

```bash
python src/decrufter.py [INPUT_FILE] [-o OUTPUT_FILE] [--no-trim] [--no-empty-lines] [--no-duplicates] [-p PATTERN] [-c CASE]
```

**Arguments:**

*   `INPUT_FILE`: Path to the input file. If omitted, reads from `stdin`.
*   `-o, --output-file OUTPUT_FILE`: Path to the output file. If omitted, writes to `stdout`.
*   `--no-trim`: Do not remove leading/trailing whitespace from lines.
*   `--no-empty-lines`: Do not remove empty lines.
*   `--no-duplicates`: Do not remove duplicate lines.
*   `-p, --pattern PATTERN`: Regex pattern to remove lines matching it.
*   `-c, --case {lower,upper,title}`: Convert text to specified case.

### Examples:

1.  **Clean a file with default options (trim, empty lines, duplicates) and print to stdout:**
    ```bash
    python src/decrufter.py my_messy_log.txt
    ```

2.  **Clean from stdin, remove comment lines, convert to lowercase, and save to a new file:**
    ```bash
    cat raw_data.txt | python src/decrufter.py -p "^#" -c lower -o cleaned_data.txt
    ```

3.  **Only remove empty lines, preserving whitespace and duplicates:**
    ```bash
    python src/decrufter.py input.txt --no-trim --no-duplicates --no-empty-lines=False -o output.txt
    ```

4.  **Remove lines containing 'ERROR' and convert to uppercase:**
    ```bash
    python src/decrufter.py system_report.log -p "ERROR" -c upper
    ```
