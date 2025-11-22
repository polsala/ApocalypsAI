# Nightly Scrap-Heap Schema Scrubber

## 🧹 Overview

In the chaotic aftermath, data often becomes... well, a scrap-heap. The Nightly Scrap-Heap Schema Scrubber is your trusty tool for bringing order to the digital rubble. This Python CLI utility helps you clean up messy JSON or YAML files by intelligently removing empty objects, empty arrays, null values, and even specific keys you deem obsolete. Keep your data lean, mean, and ready for whatever the apocalypse throws at it!

## ✨ Features

*   **JSON & YAML Support**: Handles both common data formats.
*   **Automatic Cleanup**: Removes empty objects (`{}`), empty arrays (`[]`), and `null` values by default.
*   **Key Extermination**: Optionally specify a list of keys to completely remove from your data.
*   **Recursive Cleaning**: Dives deep into nested structures to ensure thorough scrubbing.
*   **Self-Contained**: No external dependencies beyond standard Python libraries (`json`, `yaml`, `argparse`).

## 🚀 Usage

```bash
python src/scrubber.py --input <input_file> --output <output_file> [--remove-keys key1 key2 ...]
```

### Arguments:

*   `--input <file_path>`: **Required**. Path to the input JSON or YAML file.
*   `--output <file_path>`: **Required**. Path where the cleaned output file will be saved.
*   `--remove-keys <key1> [<key2> ...]`: **Optional**. A space-separated list of keys to remove from the data.

### Examples:

1.  **Clean a JSON file, removing empty structures and nulls:**
    ```bash
    python src/scrubber.py --input data.json --output cleaned_data.json
    ```

2.  **Clean a YAML file, also removing 'metadata' and 'temp_id' keys:**
    ```bash
    python src/scrubber.py --input config.yaml --output cleaned_config.yaml --remove-keys metadata temp_id
    ```

## 🛠️ Development

### Prerequisites

*   Python 3.8+
*   `PyYAML` (install with `pip install PyYAML` if not already present)

### Running Tests

Navigate to the `nightly-scrap-heap-schema-scrubber` directory and run:

```bash
python -m pytest tests/
```
