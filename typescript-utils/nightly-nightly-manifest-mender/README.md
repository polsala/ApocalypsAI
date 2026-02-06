# Nightly Manifest Mender

## Overview

The `nightly-manifest-mender` is a whimsical-yet-useful command-line interface (CLI) tool designed to help survivors (and their AI assistants) maintain pristine and optimized inventory manifests. It validates your JSON or YAML manifest files against a specified JSON Schema and provides 'mending' suggestions based on a set of pre-defined apocalyptic survival rules.

Ensure your survival caches are logically sound, critically stocked, and free from redundant clutter with the wisdom of the ApocalypsAI.

## Features

*   **Schema Validation**: Validate your inventory manifests against a JSON Schema to ensure structural integrity and data types.
*   **Apocalyptic Mending Suggestions**: Receive actionable (and sometimes quirky) advice to optimize your manifest, such as:
    *   **Hydration Imperative**: Critical warnings if essential water sources are missing.
    *   **Tool Redundancy Protocol**: Suggestions to consolidate similar tools.
    *   **Luxury Overload Directive**: Gentle nudges to balance comfort items with survival necessities.
*   **Type-Safe**: Built with TypeScript for robust data handling and developer confidence.

## Installation

1.  Navigate to the `nightly-manifest-mender` directory.
2.  Install dependencies:
    ```bash
npm install
    ```
3.  Build the TypeScript project:
    ```bash
npm run build
    ```

## Usage

Run the utility from the command line:

```bash
npm start -- <path_to_manifest.json_or_yaml> [options]
```

### Arguments

*   `<path_to_manifest.json_or_yaml>`: The path to your inventory manifest file (JSON or YAML).

### Options

*   `-s, --schema <path>`: Path to a custom JSON Schema file for validation. If not provided, a basic default schema is used.
*   `-h, --help`: Display help for command.

### Examples

1.  **Validate a manifest with the default schema:**
    ```bash
npm start -- ./examples/my_survival_cache.json
    ```

2.  **Validate a manifest with a custom schema:**
    ```bash
npm start -- ./examples/my_bunker_inventory.yaml -s ./schemas/bunker_schema.json
    ```

## Manifest Structure (Default Schema)

By default, the utility expects a manifest structure similar to this:

```json
{
  "items": [
    {
      "name": "Water Bottle",
      "quantity": 5,
      "category": "Hydration"
    },
    {
      "name": "First Aid Kit",
      "quantity": 1,
      "category": "Medical"
    }
  ],
  "location": "Sector 7G",
  "lastUpdated": "2024-07-20T10:00:00Z"
}
```

## Development & Testing

To run tests:

```bash
npm test
```
