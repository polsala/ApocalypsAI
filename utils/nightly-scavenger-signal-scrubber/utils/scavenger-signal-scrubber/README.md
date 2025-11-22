# Scavenger's Satellite Signal Scrubber

## Overview

In the post-apocalyptic wasteland, data signals are often garbled, riddled with static, and full of redundant noise. The Scavenger's Satellite Signal Scrubber is your trusty tool for cleaning up those precious text files, making them legible and useful for further analysis or archival. Whether it's a salvaged log, a fragmented message, or a corrupted data stream, this scrubber will help you make sense of the digital debris.

## Features

*   **Remove Empty Lines**: Discard lines that contain no characters or only whitespace.
*   **Remove Duplicate Lines**: Ensure each unique line appears only once.
*   **Strip Excessive Whitespace**: Clean leading/trailing whitespace and normalize internal whitespace.
*   **Custom Pattern Removal**: Define specific regex patterns to eliminate unwanted "static" or junk characters.

## Usage

### Command Line Interface

```bash
python src/scrubber.py <input_file> <output_file> [options]
```

**Options:**

*   `-d`, `--no-duplicates`: Do not remove duplicate lines.
*   `-e`, `--no-empty`: Do not remove empty lines.
*   `-s`, `--no-strip`: Do not strip leading/trailing whitespace or normalize internal whitespace.
*   `-p PATTERN`, `--pattern PATTERN`: Add a custom regex pattern to remove. Can be specified multiple times.
*   `-h`, `--help`: Show help message.

**Example:**

```bash
python src/scrubber.py raw_signal.txt cleaned_signal.txt --pattern "\[JUNK\]" --pattern "ERROR:\d+"
```

This will clean `raw_signal.txt`, remove lines containing `[JUNK]` or `ERROR:123` (and similar), and save the result to `cleaned_signal.txt`.

### As a Module

```python
from src.scrubber import scrub_file

input_path = "path/to/raw_data.txt"
output_path = "path/to/clean_data.txt"

scrub_file(
    input_path,
    output_path,
    remove_duplicates=True,
    remove_empty_lines=True,
    strip_whitespace=True,
    custom_patterns_to_remove=[r"\[ADVERTISEMENT\]", r"\[SPAM\]"]
)
```

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed.

1.  Navigate to the `utils/scavenger-signal-scrubber` directory.
2.  Run directly using `python src/scrubber.py`.

## Development & Testing

To run the tests:

```bash
python -m unittest tests/test_scrubber.py
```
