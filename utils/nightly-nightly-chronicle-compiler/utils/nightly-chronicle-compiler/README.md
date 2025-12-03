# Nightly Chronicle Compiler

## Overview

The `nightly-chronicle-compiler` is a whimsical-yet-useful command-line utility designed to help you make sense of fragmented records. In a world where information might be scattered across numerous text files (daily logs, scavenged notes, system reports), this tool compiles them into a single, chronologically ordered narrative.

It works by scanning a specified directory for `.txt` files, attempting to extract a date from their filenames (e.g., `YYYY-MM-DD_event.txt`), and then concatenating their contents into a single output file, sorted by date.

## Usage

```bash
python src/compiler.py <input_directory> <output_file>
```

### Arguments:

*   `<input_directory>`: The path to the directory containing the text files to be compiled.
*   `<output_file>`: The path where the compiled chronicle will be saved.

### Example:

Let's say you have a directory `my_logs/` with the following files:

```
my_logs/
├── 2023-10-27_radio_chatter.txt
├── 2023-10-25_supply_run.txt
└── 2023-10-26_strange_lights.txt
```

Running the command:

```bash
python src/compiler.py my_logs/ compiled_chronicle.txt
```

Will produce `compiled_chronicle.txt` with content ordered by date:

```
--- 2023-10-25 ---
Content of 2023-10-25_supply_run.txt

--- 2023-10-26 ---
Content of 2023-10-26_strange_lights.txt

--- 2023-10-27 ---
Content of 2023-10-27_radio_chatter.txt

```

## Development

This utility is written in Python 3.11 and uses only standard library modules, ensuring it's self-contained and easy to run.

## Testing

To run the tests, navigate to the `utils/nightly-chronicle-compiler` directory and execute:

```bash
python -m unittest tests/test_compiler.py
```
