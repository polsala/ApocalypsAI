# Nightly Digital Dust Bunny Duster

A whimsical Node.js CLI utility designed to help survivors organize their digital hoard. It scans a specified directory for text-based files, extracts relevant keywords, and compiles them into a simple, searchable JSON index. Perfect for when the internet is just a distant memory, but your data isn't!

## Features

- **Directory Scanning**: Recursively scans a target directory for common text file types.
- **Keyword Extraction**: Simple, robust keyword extraction from file contents.
- **Offline Indexing**: Generates a `dust-bunny-index.json` file, making your data searchable without external dependencies.
- **CLI Search**: Quickly find files based on keywords from your generated index.

## Installation

1.  Navigate to the `nightly-digital-dust-bunny-duster` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

### 1. Indexing Your Digital Hoard

To create an index of your files, run the `index` command, providing the path to the directory you want to scan. The index will be saved as `dust-bunny-index.json` in the current working directory.

```bash
node src/cli.js index <path/to/your/hoard>
# Example: node src/cli.js index ./my-survival-notes
```

This will create a `dust-bunny-index.json` file containing entries like:
```json
[
  {
    "path": "my-survival-notes/recipes/radroach-stew.txt",
    "snippet": "Ingredients: 3 radroaches, 1 mutated potato...",
    "keywords": ["radroaches", "stew", "recipes", "potato"]
  },
  // ... more entries
]
```

### 2. Searching Your Index

Once you have an index, you can search it using the `search` command and a keyword.

```bash
node src/cli.js search <keyword> [path/to/index.json]
# Example: node src/cli.js search radroach
# Example: node src/cli.js search map ./my-custom-index.json
```

If no index path is provided, it defaults to `dust-bunny-index.json` in the current directory.

## Supported File Types

The duster currently processes files with the following extensions: `.txt`, `.md`, `.json`, `.js`, `.html`, `.css`, `.xml`, `.log`.

## Development & Testing

To run the tests:

```bash
npm test
```
