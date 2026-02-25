# Nightly Manifest Mender

## Overview

The `nightly-manifest-mender` is a crucial utility for any survivor managing their precious resources in the post-apocalyptic wasteland. It's a high-performance command-line tool built with Rust, designed to validate and "mend" resource manifests stored in YAML, JSON, or TOML formats. 

In times of chaos, data integrity is paramount. This tool ensures your inventory manifests are consistent, complete, and free from common errors, helping you avoid critical shortages or miscalculations when it matters most.

## Features

*   **Multi-format Support**: Parses and validates YAML, JSON, and TOML manifest files.
*   **Schema Validation**: Checks for required fields and correct data types based on a predefined survival manifest schema.
*   **Whimsical Mending**: Attempts to fix common issues:
    *   Adds default values for missing optional fields (e.g., `status: "Unknown"`).
    *   Infers and adds missing units for common items (e.g., "First Aid Kit" -> `unit: "kit"`).
    *   Attempts to parse string quantities into integers (e.g., `quantity: "five"` -> `quantity: 5`).
*   **Error Reporting**: Provides clear, actionable error messages for unfixable issues.
*   **Output Flexibility**: Can output the mended manifest to a new file or stdout, preserving the original format or converting to another.

## Usage

```bash
nightly-manifest-mender <INPUT_FILE> [OPTIONS]
```

### Arguments

*   `<INPUT_FILE>`: Path to the resource manifest file (YAML, JSON, or TOML).

### Options

*   `-o, --output <OUTPUT_FILE>`: Path to write the mended manifest. If not provided, output is printed to stdout.
*   `-f, --format <FORMAT>`: Output format (yaml, json, toml). Defaults to the input file's format if not specified.
*   `-v, --verbose`: Enable verbose output, showing detailed mending actions.
*   `-c, --check-only`: Only validate and report errors, do not output a mended file.

### Examples

1.  **Validate and mend a YAML manifest, output to stdout:**
    ```bash
    nightly-manifest-mender my_cache.yaml
    ```

2.  **Mend a JSON manifest and save as a new YAML file:**
    ```bash
    nightly-manifest-mender old_stash.json -o new_stash.yaml -f yaml
    ```

3.  **Check a TOML manifest for errors without modifying:**
    ```bash
    nightly-manifest-mender bunker_inventory.toml --check-only
    ```

## Manifest Schema

The tool expects a manifest structure similar to this:

```yaml
cache_id: String # Required, unique identifier
location: String # Required, physical location
last_inspected: String # Required, ISO 8601 datetime
resources:
  - item: String # Required, name of the resource
    quantity: Integer # Required, numeric quantity
    unit: String # Required, unit of measurement (e.g., "cans", "liters", "kits")
    status: String # Optional, condition or notes (defaults to "Unknown")
```

Any deviations from this schema will be reported, and where possible, mended.
