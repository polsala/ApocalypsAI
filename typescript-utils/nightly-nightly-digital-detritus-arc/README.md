# Nightly Digital Detritus Archivist

## Overview

The `nightly-digital-detritus-arch` is a whimsical-yet-useful command-line interface (CLI) utility built with TypeScript. It helps you organize your digital files (your 'digital detritus') into user-defined 'apocalyptic' categories based on a set of rules. Think of it as a post-collapse data curator, ensuring your vital information, cherished memories, and emergency logs are neatly sorted for the future.

This utility supports rules based on file name patterns, extensions, size, and even content (for text files), providing a type-safe way to define your archiving strategy.

## Features

*   **Type-Safe Configuration**: Define categories and rules using a clear, validated JSON schema.
*   **Rule-Based Classification**: Automatically classify files based on name, extension, size, or content.
*   **Dry-Run Mode**: Preview archiving actions without moving any files.
*   **Whimsical Categories**: Embrace the apocalypse with categories like "Survival Blueprints", "Emergency Broadcast Logs", or "Pre-Collapse Mementos".

## Installation

To use this utility, you need Node.js (v18 or higher) and npm installed.

1.  Navigate to the utility's directory:
    ```bash
    cd nightly-digital-detritus-arch
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Build the TypeScript project:
    ```bash
    npm run build
    ```
4.  (Optional) Link the CLI tool globally:
    ```bash
    npm link
    ```
    If not linked globally, you can run it using `node dist/index.js`.

## Usage

Run the archivist from your terminal:

```bash
nightly-digital-detritus-arch --source <source_directory> --dest <destination_directory> --config <config_file.json> [--dry-run]
```

**Arguments:**

*   `--source <path>`: The directory containing the files you want to organize.
*   `--dest <path>`: The root directory where categorized files will be moved. Subdirectories will be created for each category.
*   `--config <path>`: Path to your JSON configuration file defining categories and rules.
*   `--dry-run`: (Optional) If present, the utility will only report what it *would* do, without actually moving any files. Highly recommended for testing your configuration.
*   `--help`: Displays usage information.

### Example

```bash
nightly-digital-detritus-arch --source ./my-scraps --dest ./apocalypse-archive --config ./archivist-config.json --dry-run
```

## Configuration File (`archivist-config.json`)

The configuration file is a JSON file that defines your archiving categories and the rules for classifying files into them.

```json
{
  "defaultCategoryName": "Unclassified Scraps",
  "categories": [
    {
      "name": "Survival Blueprints",
      "description": "Critical schematics and instructions for post-collapse survival.",
      "rules": [
        { "type": "extension", "pattern": "(.pdf|.doc|.txt)$" },
        { "type": "content", "pattern": "(blueprint|schematic|manual)" }
      ],
      "destinationSubdir": "blueprints"
    },
    {
      "name": "Emergency Broadcast Logs",
      "description": "Records of vital communications and warnings.",
      "rules": [
        { "type": "name", "pattern": "^(emergency|broadcast|log)" },
        { "type": "extension", "pattern": ".log$" }
      ],
      "destinationSubdir": "broadcasts"
    },
    {
      "name": "Pre-Collapse Mementos",
      "description": "Personal photos, journals, and other nostalgic items from before.",
      "rules": [
        { "type": "extension", "pattern": "(.jpg|.png|.gif|.jpeg)$" },
        { "type": "size", "minSizeKB": 100, "maxSizeKB": 5000 }
      ],
      "destinationSubdir": "mementos"
    }
  ]
}
```

**Configuration Fields:**

*   `defaultCategoryName`: (string) The name of the category where files that don't match any specific rule will be placed.
*   `categories`: (array of objects) Each object defines a category:
    *   `name`: (string) A human-readable name for the category.
    *   `description`: (string) A brief description of the category's purpose.
    *   `rules`: (array of objects) A list of rules. A file must match *at least one* rule in a category to be classified into it.
        *   `type`: (string) The type of rule. Can be `"name"`, `"extension"`, `"size"`, or `"content"`.
        *   `pattern`: (string, optional) A regular expression string used for `"name"`, `"extension"`, and `"content"` rules. Case-insensitive matching is applied.
        *   `minSizeKB`: (number, optional) Minimum file size in kilobytes for `"size"` rules.
        *   `maxSizeKB`: (number, optional) Maximum file size in kilobytes for `"size"` rules.
    *   `destinationSubdir`: (string) The subdirectory name within the `--dest` path where files for this category will be moved.

## Development

To run tests:

```bash
npm test
```
