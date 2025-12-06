# Nightly Dust Bunny Sweeper

## Overview

The `Nightly Dust Bunny Sweeper` is a whimsical yet practical utility designed to keep your digital workspace pristine. In the chaotic aftermath, even digital spaces can accumulate clutter. This tool diligently scans a specified directory and recursively deletes any empty subdirectories it finds, much like sweeping away forgotten dust bunnies.

It's perfect for cleaning up after build processes, failed experiments, or simply maintaining a lean and organized file system.

## Usage

To run the sweeper, execute the `sweeper.py` script with the target directory as an argument:

```bash
python src/sweeper.py /path/to/your/directory
```

**Warning**: This tool performs deletion. While it only targets empty directories, always ensure you understand the target directory before running it on critical paths.

## Development

### Requirements

*   Python 3.6+

### Running Tests

Tests are self-contained and can be run using `unittest`:

```bash
python -m unittest tests/test_sweeper.py
```
