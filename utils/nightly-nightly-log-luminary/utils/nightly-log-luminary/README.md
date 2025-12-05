# Nightly Log Luminary

In the chaotic aftermath, logs can be a beacon of truth. The Nightly Log Luminary is a simple, self-contained Python utility designed to scan log files for predefined patterns, such as errors, warnings, or specific keywords. It illuminates the critical events, providing a clear summary of findings to help you navigate the digital darkness and keep your systems operational.

## Usage

Run the utility from your terminal, providing the path to the log file and one or more regex patterns to search for.

```bash
python src/luminary.py <log_file_path> [pattern1] [pattern2] ...
```

### Example

To scan `/var/log/syslog` for lines containing "ERROR", "WARNING", or "failed":

```bash
python src/luminary.py /var/log/syslog "ERROR" "WARNING" "failed"
```

## Output

The utility will print a summary report to standard output, detailing:

*   The total number of lines scanned.
*   For each pattern, the number of matches found.
*   For each match, the line number and the content of the matching line.

If no patterns are found, a message indicating this will be displayed.
