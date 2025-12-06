# Nightly-Nightly-Wasteland-Log-Scrambler

A whimsical-yet-useful Bash utility for the post-apocalyptic community. This script "scrambles" sensitive patterns in your log files, replacing them with cryptic, whimsical wasteland jargon. It's perfect for anonymizing logs before sharing, archiving, or simply reducing digital clutter while retaining the "flavor" of your data. Think of it as a digital sandstorm for your secrets!

## Features

*   **Sensitive Data Scrambling**: Replaces common sensitive patterns (IPs, emails, UUIDs, dates, times) with random, pre-defined wasteland words.
*   **Customizable Patterns**: Define your own regex patterns via an environment variable to target specific data.
*   **Flexible Output**: Scramble logs to a new file or directly to standard output.
*   **Whimsical Jargon**: Infuses your logs with terms like "Glimmer", "Echo", "Dust", and "Temporal Rift".

## Installation

This is a standalone Bash script. No special installation is required beyond having Bash available on your system.

1.  Clone the repository or download the `nightly-wasteland-log-scrambler` directory.
2.  Navigate into the directory: `cd nightly-wasteland-log-scrambler`
3.  Make the script executable: `chmod +x src/scrambler.sh`

## Usage

```bash
./src/scrambler.sh <input_file> [output_file]
```

### Arguments:

*   `<input_file>`: Path to the log file you want to scramble.
*   `[output_file]`: (Optional) Path where the scrambled content will be saved. If omitted, the scrambled content will be printed to standard output (stdout).

### Environment Variables:

*   `SCRAMBLE_PATTERNS`: A comma-separated list of extended regular expressions (regex) to match and scramble. If this variable is not set, the script uses a set of default patterns.

### Examples:

1.  **Scramble a log file with default patterns and save to a new file:**
    ```bash
    ./src/scrambler.sh my_server.log scrambled_server.log
    ```

2.  **Scramble a log file and print to stdout:**
    ```bash
    ./src/scrambler.sh access.log
    ```
    You can then pipe this output:
    ```bash
    ./src/scrambler.sh access.log | less
    ./src/scrambler.sh access.log > archived_access.log
    ```

3.  **Scramble with custom patterns (e.g., specific API keys or user IDs):**
    ```bash
    export SCRAMBLE_PATTERNS='API_KEY_[A-Z0-9]{16},user_id=[0-9]{5}'
    ./src/scrambler.sh sensitive_data.log anonymized_data.log
    unset SCRAMBLE_PATTERNS # Good practice to unset after use
    ```
    *Note: Ensure your regex patterns are valid extended regular expressions.*

## Default Scrambling Patterns

If `SCRAMBLE_PATTERNS` is not set, the script will target the following common sensitive data types:

*   IPv4 Addresses (e.g., `192.168.1.1`)
*   Email Addresses (e.g., `user@example.com`)
*   UUID/GUIDs (e.g., `a1b2c3d4-e5f6-7890-1234-567890abcdef`)
*   Dates (YYYY-MM-DD, MM/DD/YYYY)
*   Timestamps (HH:MM:SS)

## Development & Testing

To run the automated tests:

```bash
./tests/test_scrambler.sh
```

The tests are designed to be deterministic and offline. They achieve this by setting the `RANDOM` shell variable to `0` before executing the main script, ensuring that the `get_random_word` function always selects the first word from the `REPLACEMENT_WORDS` array ("Glimmer"). This allows for consistent verification of the scrambling logic.
