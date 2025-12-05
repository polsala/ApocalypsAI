# Nightly Data Glitch Rectifier

## Overview

The Nightly Data Glitch Rectifier is a whimsical yet essential utility designed to bring order to the chaotic data streams of the post-apocalyptic world. It meticulously scans and rectifies common textual inconsistencies, ensuring that your precious data remains pristine and reliable, even when sourced from the most glitch-ridden terminals. Think of it as a digital janitor, tidying up the digital rubble.

## Features

*   **Whitespace Trimming**: Eliminates leading and trailing spaces.
*   **Case Normalization**: Converts text to lowercase, uppercase, or title case.
*   **Simple String Replacement**: Fixes common typos or replaces specific substrings.
*   **Regex-based Replacement**: Offers powerful pattern-based text transformations.

## Usage

The rectifier can be used as a Python module or run directly from the command line. It takes a list of strings and a set of rectification rules, applying them sequentially.

### Command Line

```bash
python src/rectifier.py --input "data_to_clean.txt" --rules "rectification_rules.json" --output "cleaned_data.txt"
```

If no `--output` is specified, results are printed to stdout. If no `--input` is specified, it reads from stdin.

### `data_to_clean.txt` (example)

```
  HELLO WORLD  
this is a test
  another test  
```

### `rectification_rules.json` (example)

```json
[
    {"type": "trim"},
    {"type": "lower"},
    {"type": "replace", "old": "test", "new": "trial"}
]
```

### Output (`cleaned_data.txt`)

```
hello world
this is a trial
another trial
```

### As a Python Module

```python
from utils.nightly_data_glitch-rectifier.src.rectifier import rectify_string

rules = [
    {"type": "trim"},
    {"type": "upper"},
    {"type": "replace", "old": "GLITCH", "new": "FIXED"}
]

data = "  a GLITCHY string  "
cleaned_data = rectify_string(data, rules)
print(cleaned_data) # Output: "A FIXED STRING"
```

## Rectification Rules

Rules are provided as a list of dictionaries. Each dictionary defines a single rectification step.

*   **`{"type": "trim"}`**: Removes leading/trailing whitespace.
*   **`{"type": "lower"}`**: Converts the string to lowercase.
*   **`{"type": "upper"}`**: Converts the string to uppercase.
*   **`{"type": "title"}`**: Converts the string to title case.
*   **`{"type": "replace", "old": "substring_to_find", "new": "replacement_substring"}`**: Replaces all occurrences of `old` with `new`.
*   **`{"type": "regex_replace", "pattern": "regex_pattern", "replacement": "replacement_string"}`**: Replaces all matches of `pattern` with `replacement_string`. The `pattern` should be a valid regular expression.

## Installation

This utility is self-contained. Simply copy the `nightly-data-glitch-rectifier` folder into your `utils/` directory. Requires Python 3.6+.

## Development

To run tests:
```bash
python -m unittest tests/test_rectifier.py
```
