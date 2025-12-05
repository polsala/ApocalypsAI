# Nightly Temporal Tangle Tamer

## Overview

The Nightly Temporal Tangle Tamer is a whimsical-yet-essential command-line utility designed to bring order to the chaotic temporal landscape of the post-apocalyptic world. Whether you're deciphering ancient timestamps from forgotten servers or coordinating rendezvous across disparate time zones, this tool helps you convert and format dates and times with ease.

It supports various input formats (Unix epoch, ISO 8601, custom strings) and allows conversion to different output formats and timezones.

## Features

*   **Flexible Input**: Parse Unix epoch, ISO 8601, or custom date/time strings.
*   **Timezone Conversion**: Convert timestamps between any IANA timezone (e.g., `UTC`, `America/New_York`, `Europe/London`).
*   **Custom Output**: Format the output timestamp using standard `strftime` directives.
*   **Self-Contained**: A single Python script with minimal dependencies.

## Installation

1.  Navigate to the `utils/nightly-temporal-tangle-tamer` directory.
2.  (Optional, but recommended) Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install pytz
    ```

## Usage

Run the utility from the command line:

```bash
python src/tamer.py --timestamp <value> [OPTIONS]
```

### Arguments:

*   `--timestamp <value>` (Required): The timestamp to convert (Unix epoch, ISO 8601, or custom string).
*   `--input-format <format_string>` (Optional): The `strftime` format string if `--timestamp` is a custom string. Not needed for epoch or ISO 8601.
*   `--input-tz <timezone_name>` (Optional): The IANA timezone name for the input timestamp (e.g., `UTC`, `America/New_York`). Defaults to `UTC` if not provided.
*   `--output-format <format_string>` (Optional): The `strftime` format string for the output. Defaults to ISO 8601 (`%Y-%m-%dT%H:%M:%S%z`).
*   `--output-tz <timezone_name>` (Optional): The IANA timezone name for the output. Defaults to `UTC` if not provided.

### Examples:

1.  **Convert Unix epoch to ISO 8601 in UTC:**
    ```bash
    python src/tamer.py --timestamp 1678886400
    # Output: 2023-03-15T12:00:00+0000
    ```

2.  **Convert ISO 8601 (UTC) to America/Los_Angeles time:**
    ```bash
    python src/tamer.py --timestamp "2023-03-15T12:00:00Z" --output-tz America/Los_Angeles
    # Output: 2023-03-15T05:00:00-0700
    ```

3.  **Convert a custom string (Europe/London) to Asia/Tokyo with a custom format:**
    ```bash
    python src/tamer.py --timestamp "2023-03-15 12:00:00" --input-format "%Y-%m-%d %H:%M:%S" --input-tz Europe/London --output-tz Asia/Tokyo --output-format "%Y/%m/%d %H:%M:%S %Z"
    # Output: 2023/03/15 21:00:00 JST
    ```

4.  **Get current UTC time in a specific format:**
    ```bash
    # (Note: For current time, you'd typically use `date` or `datetime.now()` directly.
    # This utility is for converting *given* timestamps.)
    # Example showing a different output format for an existing timestamp:
    python src/tamer.py --timestamp 1678886400 --output-format "%A, %B %d, %Y %H:%M:%S %Z"
    # Output: Wednesday, March 15, 2023 12:00:00 +0000
    ```

## Development & Testing

To run the tests:

```bash
python -m unittest tests/test_tamer.py
```
