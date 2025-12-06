# Apocalypse Prep Kit Assembler

## Overview

The `apocalypse-prep-kit-assembler` is a whimsical-yet-practical utility designed to prepare your Python projects for any digital disruption. It takes a `requirements.txt` file and downloads all specified packages into a designated local directory, creating a self-contained 'prep kit' for offline installation.

Think of it as stocking your digital pantry: even if the internet goes dark, your project's essential dependencies are safely cached and ready to be installed.

## Usage

```bash
python src/prep_kit_assembler.py --requirements <path/to/requirements.txt> --output <path/to/output_directory>
```

### Arguments:

*   `--requirements` (required): Path to your `requirements.txt` file.
*   `--output` (required): Path to the directory where downloaded packages will be stored. The directory will be created if it doesn't exist.

## Example

Given a `requirements.txt`:

```
requests==2.28.1
pyyaml==6.0
```

Run the utility:

```bash
python src/prep_kit_assembler.py --requirements my_project/requirements.txt --output ./offline_packages
```

This will download `requests` and `pyyaml` (and their transitive dependencies) into the `./offline_packages` directory.

To install from the prep kit:

```bash
pip install --no-index --find-links ./offline_packages -r my_project/requirements.txt
```

## Development

### Running Tests

```bash
python -m unittest tests/test_prep_kit_assembler.py
```
