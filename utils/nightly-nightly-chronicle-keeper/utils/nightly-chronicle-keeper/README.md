# Nightly Chronicle Keeper

## Overview

The Nightly Chronicle Keeper is a whimsical-yet-useful utility designed to help you understand the 'archaeology' of your codebase. It scans a specified directory for common code files, counts total lines, comment lines, and identifies files that haven't been touched in a long time – your 'ancient' scrolls of crumbling code.

This tool is perfect for: 
- Getting a quick overview of a project's size and comment density.
- Discovering forgotten files that might need attention or archiving.
- Fueling your inner code archaeologist.

## Usage

```bash
python src/chronicle_keeper.py <path_to_directory>
```

Example:

```bash
python src/chronicle_keeper.py ../..
```

## Features

- **Line Counting**: Total lines and comment lines for supported file types.
- **Ancient File Detection**: Flags files not modified in the last 365 days.
- **Summary Report**: Provides an overall count and a list of ancient files.
- **Supported File Types**: `.py`, `.js`, `.md`, `.sh`, `.yml`, `.json`, `.txt`, `.xml`, `.html`, `.css`, `.go`, `.java`, `.c`, `.cpp`, `.h`.

## Development

To run tests:

```bash
python -m unittest tests/test_chronicle_keeper.py
```
