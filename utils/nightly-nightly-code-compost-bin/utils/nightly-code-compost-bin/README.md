# Nightly Code Compost Bin

## Overview

The `nightly-code-compost-bin` is a whimsical-yet-useful utility designed to help developers identify and 'compost' digital clutter within their Python projects. Just as a garden compost bin breaks down organic waste into rich soil, this tool helps you find and consider removing or refactoring old, unused, or commented-out code, turning digital 'waste' into a cleaner, more maintainable codebase.

It scans specified directories for common patterns of potentially 'dead' or 'stale' code, such as:

*   `if False:` or `if 0:` blocks (code that will never execute).
*   Large blocks of consecutive comments that might indicate old, unused code.
*   `# TODO:` or `# FIXME:` markers that might be lingering.

## Usage

To run the compost bin, navigate to the utility's directory and execute the main script:

```bash
python src/compost_bin.py --path /path/to/your/project --ignore venv,node_modules
```

### Arguments:

*   `--path <directory>`: The root directory to start scanning from. (Required)
*   `--ignore <comma_separated_dirs>`: A comma-separated list of directory names to ignore during the scan (e.g., `venv,build,dist`). (Optional)

## Example Output

```
Scanning /path/to/your/project for compostable code...

Found 3 compostable items:

File: my_module/feature.py
  Line 42: Type: Dead Code (if False/0:)
    Snippet: if False: # Old feature toggle

File: my_module/old_script.py
  Line 10-15: Type: Consecutive Comments
    Snippet: # This was an old attempt at parsing data
             # It's no longer used but kept for reference
             # Should probably be removed or archived

File: another_module/utility.py
  Line 78: Type: TODO/FIXME Marker
    Snippet: # TODO: Refactor this function, it's a mess

Scan complete. Consider reviewing these items for removal or refactoring.
```

## Development

### Running Tests

To ensure the compost bin is working correctly, run the provided tests:

```bash
python -m unittest tests/test_compost_bin.py
```
