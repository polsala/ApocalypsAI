# Nightly Digital Dust Bunny Collector

A whimsical-yet-useful Node.js utility to help you find, categorize, and manage those tiny, often forgotten files – "digital dust bunnies" – lurking in your directories. These small files can accumulate over time, cluttering your workspace and making it harder to find what truly matters. This tool helps you identify them, understand their types, and decide if they're worth keeping or sweeping away.

## Features

*   **Recursive Directory Scan**: Traverses directories to find all files.
*   **Size-based Filtering**: Focuses on files below a configurable size threshold (default: 10KB).
*   **Intelligent Categorization**: Groups files into common types like `logs`, `temp`, `images`, `code`, `documents`, `archives`, and `other` based on their extensions.
*   **Comprehensive Report**: Generates a detailed summary showing found files, their categories, and total sizes, helping you decide on cleanup actions.
*   **Cross-Platform**: Built with Node.js, it runs seamlessly on Windows, macOS, and Linux.

## Installation

1.  **Ensure Node.js is installed**: You need Node.js (v14 or higher recommended) to run this utility. You can download it from [nodejs.org](https://nodejs.org/).
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-digital-dust-bunny
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```
    *(Note: This utility currently has no external runtime `npm` dependencies, relying only on built-in Node.js modules like `fs` and `path`.)*

## Usage

Run the utility from the command line:

```bash
node src/index.js [directory_path] [max_size_kb]
```

*   `directory_path` (optional): The path to the directory you want to scan. Defaults to the current working directory (`.`).
*   `max_size_kb` (optional): The maximum file size in kilobytes (KB) to consider a "dust bunny". Files larger than this will be ignored. Defaults to `10` KB.

### Examples

1.  **Scan the current directory for files up to 10KB (default):**
    ```bash
    node src/index.js
    ```

2.  **Scan a specific directory (`~/my_project`) for files up to 5KB:**
    ```bash
    node src/index.js ~/my_project 5
    ```

3.  **Scan a directory with a custom max size:**
    ```bash
    node src/index.js /var/log 2
    ```

## Development & Testing

To run the automated tests:

```bash
npm test
```

The tests use mocks for file system operations (`fs.promises`) and path manipulation (`path`) to ensure they are deterministic and do not interact with the actual file system.

## Contributing

Feel free to suggest new categories, features, or improvements!
