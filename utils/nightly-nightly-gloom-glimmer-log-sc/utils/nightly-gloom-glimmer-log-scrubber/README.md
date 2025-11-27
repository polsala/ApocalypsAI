# Nightly Gloom-Glimmer Log Scrubber

## Overview

The ApocalypsAI Nightly Integrator presents the Gloom-Glimmer Log Scrubber – your essential tool for sifting through the digital detritus of the wasteland. In a world of constant system failures and cryptic error messages, this utility helps you find the 'glimmers' of critical information amidst the 'gloom' of irrelevant noise.

It's designed to make debugging and monitoring less of a chore by filtering out specified log entries and highlighting others, bringing clarity to chaos.

## Features

*   **Gloom Filtering**: Suppress log lines containing specified keywords or phrases.
*   **Glimmer Highlighting**: Mark important log lines with a clear `[GLIMMER]` prefix for easy identification.
*   **Flexible Input/Output**: Process log content from a file and output to stdout or a new file.

## Usage

```bash
python src/scrubber.py <input_log_file> [--output <output_log_file>] [--glimmers <keyword1> <keyword2> ...] [--glooms <keyword1> <keyword2> ...]
```

### Arguments:

*   `<input_log_file>`: Path to the log file you want to scrub.
*   `--output <output_log_file>`: (Optional) Path to the file where the scrubbed log will be written. If not provided, output goes to stdout.
*   `--glimmers <keyword1> <keyword2> ...`: (Optional) Space-separated list of keywords. Lines containing any of these will be prefixed with `[GLIMMER]`.
*   `--glooms <keyword1> <keyword2> ...`: (Optional) Space-separated list of keywords. Lines containing any of these will be entirely filtered out.

### Examples:

1.  **Basic scrubbing, output to console:**
    ```bash
    python src/scrubber.py my_app.log --glimmers ERROR CRITICAL --glooms DEBUG INFO
    ```

2.  **Scrubbing and saving to a new file:**
    ```bash
    python src/scrubber.py server.log --output server_scrubbed.log --glimmers 'failed to connect' 'data corruption' --glooms 'heartbeat' 'ping'
    ```

3.  **Only highlighting, no filtering:**
    ```bash
    python src/scrubber.py system.log --glimmers 'resource exhausted'
    ```

4.  **Only filtering, no highlighting:**
    ```bash
    python src/scrubber.py access.log --glooms '200 OK' 'static file'
    ```

## Development & Testing

To run the tests, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_scrubber.py
```
