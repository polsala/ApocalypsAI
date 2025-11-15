# Nightly Data Scavenger Converter

## Overview

The 'Nightly Data Scavenger Converter' is a robust utility designed to help you salvage and repurpose data across various common formats. In a world where data integrity can be as fleeting as a whisper in the wind, this tool ensures your precious information can be transformed between JSON, YAML, and TOML with ease. Whether you're migrating configurations, integrating disparate systems, or simply tidying up your data hoard, the Scavenger Converter is your trusty companion.

## Features

*   **Multi-format Support**: Seamlessly convert between JSON, YAML, and TOML.
*   **Command-Line Interface**: Easy to use from your terminal.
*   **Self-contained**: Minimal dependencies, designed for portability.

## Installation

This utility is self-contained within its directory. To run it, you'll need Python 3.11+ and the `PyYAML`, `tomli`, and `tomli_w` libraries. These can be installed via pip:

```bash
pip install PyYAML tomli tomli_w
```

## Usage

Run the converter from the command line:

```bash
python src/converter.py --input-file <input_path> --output-file <output_path> --input-format <json|yaml|toml> --output-format <json|yaml|toml>
```

**Example: Convert a JSON file to YAML**

```bash
# Create a sample JSON file
echo '{"name": "ApocalypsAI", "version": 1.0, "active": true}' > config.json

# Convert to YAML
python src/converter.py --input-file config.json --output-file config.yaml --input-format json --output-format yaml

# Verify the output
cat config.yaml
# Expected output (order may vary slightly depending on PyYAML version):
# name: ApocalypsAI
# version: 1.0
# active: true
```

**Example: Convert a YAML file to TOML**

```bash
# Create a sample YAML file
echo 'name: "ApocalypsAI"\nversion: 1.0\nactive: true' > settings.yaml

# Convert to TOML
python src/converter.py --input-file settings.yaml --output-file settings.toml --input-format yaml --output-format toml

# Verify the output
cat settings.toml
# Expected output:
# name = "ApocalypsAI"
# version = 1.0
# active = true
```

## Development & Testing

To run the tests, navigate to the `utils/nightly-data-scavenger-converter` directory and execute:

```bash
python -m unittest tests/test_converter.py
```
