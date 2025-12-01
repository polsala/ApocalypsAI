# Nightly Quantum Quirk Quibbler

A whimsical utility to scan for and report common file and content "quirks" that can subtly degrade repository hygiene and consistency. Think of it as a digital dust bunny sweeper for your codebase!

## Features

*   **Trailing Whitespace Detection**: Identifies lines in text files that end with unnecessary whitespace.
*   **Inconsistent Casing for Key Files**: Checks if important files like `README.md`, `LICENSE`, `AGENTS.md`, and `.gitignore` adhere to their canonical casing.
*   **Empty File Identification**: Flags files that exist but contain no content, which might indicate an oversight or an incomplete task.

## Why use it?

Even small inconsistencies can lead to:
*   **Developer Friction**: Different casing for `README.md` across branches can cause confusion or build issues on case-sensitive file systems.
*   **Code Style Drift**: Trailing whitespace is a common linting issue that can be easily overlooked.
*   **Clutter**: Empty files can be remnants of refactoring or incomplete work.

The Quantum Quirk Quibbler helps you maintain a pristine and disciplined repository, aligning with the ApocalypsAI philosophy of "Anarchy with discipline."

## Usage

To run the Quibbler, simply provide the path to the directory you wish to scan:

```bash
python src/quibbler.py /path/to/your/repository
```

### Example Output (No Quirks)

```
Scanning '/path/to/your/repository' for quirks...
No quantum quirks detected! Your repository is pristine.
```

### Example Output (With Quirks)

```
Scanning '/path/to/your/repository' for quirks...

--- Inconsistent Casing ---
  - /path/to/your/repository/readme.md: Expected 'README.md', found 'readme.md'

--- Trailing Whitespace ---
  - /path/to/your/repository/src/main.py:5: Trailing whitespace: '    print("Hello, World!")  '

--- Empty Files ---
  - /path/to/your/repository/data/temp.txt

Quantum quirks detected! Time to quibble.
```

The utility will exit with code `0` if no quirks are found, and `1` if any quirks are detected, making it suitable for CI/CD pipelines.

## Development

The `quibbler.py` script is written in Python 3.11 and uses only standard library modules (`os`, `argparse`, `pathlib`, `typing`).

### Running Tests

To ensure the Quibbler is working as expected, run its self-contained tests:

```bash
python tests/test_quibbler.py
```
