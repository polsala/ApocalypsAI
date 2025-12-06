# Nightly Chronicle Checksum Calculator

## Overview
In the chaotic aftermath, the integrity of your digital chronicles is paramount. The `Nightly Chronicle Checksum Calculator` is a robust utility designed to verify the authenticity and consistency of your files and directories by generating SHA256 checksums. Whether you're safeguarding critical data fragments or just ensuring your last remaining cat memes haven't been corrupted, this tool provides peace of mind.

## Features
- Calculate SHA256 checksum for individual files.
- Recursively calculate SHA256 checksums for all files within a specified directory.
- Output results in a clear, human-readable format.

## Installation
This utility is self-contained and requires Python 3.8+.

```bash
# No special installation needed. Just ensure you have Python 3.8+.
python3 -c "import sys; assert sys.version_info >= (3, 8)"
```

## Usage

### Calculate checksum for a single file:
```bash
python3 src/checksum_calculator.py --path /path/to/your/important_file.txt
```

### Calculate checksums for all files in a directory:
```bash
python3 src/checksum_calculator.py --path /path/to/your/data_archive/
```

### Example Output:
```
Calculating checksums for: /path/to/your/data_archive/

File: /path/to/your/data_archive/document.txt
  SHA256: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2

File: /path/to/your/data_archive/images/cat_meme.jpg
  SHA256: f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9

Summary: 2 files processed.
```

## Development

### Running Tests
To ensure the calculator is functioning correctly, navigate to the utility's root directory and run:

```bash
python3 -m unittest tests/test_checksum_calculator.py
```
