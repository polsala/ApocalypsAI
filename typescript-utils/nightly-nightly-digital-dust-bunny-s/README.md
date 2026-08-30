# Nightly Digital Dust Bunny Sweeper

A whimsical-yet-useful CLI tool to help you keep your project directories tidy by identifying and reporting "digital dust bunnies" – stale files and directories that haven't been modified in a long time. Sweep away the clutter and keep your digital workspace sparkling clean!

## Features

*   **Stale File Detection**: Scans a specified directory for files and folders older than a configurable threshold.
*   **Recursive Scanning**: Traverses subdirectories to find hidden dust bunnies.
*   **Ignore Patterns**: Exclude specific files or directories (e.g., `node_modules`, `.git`) using regex patterns.
*   **Type-Safe**: Built with TypeScript for robust and maintainable code.
*   **Flexible Output**: Reports findings in human-readable text or machine-parseable JSON format.

## Installation

To use the Digital Dust Bunny Sweeper, you'll need Node.js (v16 or higher) and npm/yarn installed.

1.  **Clone the repository (or copy this utility's folder):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-digital-dust-bunny-sweeper
    ```
    *(If you're just using this utility, you can copy the `nightly-digital-dust-bunny-sweeper` folder to your desired location.)*

2.  **Install dependencies:**
    ```bash
    npm install
    # or yarn install
    ```

3.  **Build the TypeScript project:**
    ```bash
    npm run build
    # or yarn build
    ```

4.  **(Optional) Link the CLI tool for global access:**
    ```bash
    npm link
    # or yarn link
    ```
    This will allow you to run `dust-bunny-sweeper` from any directory.

## Usage

Run the `dust-bunny-sweeper` command followed by the path you want to scan.

```bash
dust-bunny-sweeper <path_to_scan> [options]
```

### Arguments

*   `<path_to_scan>`: The root directory to start scanning for dust bunnies.

### Options

*   `-t, --threshold <days>`: Minimum age in days for a file/directory to be considered a dust bunny. Defaults to `90` days.
*   `-i, --ignore <patterns...>`: Space-separated regex patterns to ignore files/directories. For example, `".git" "node_modules" "temp_files_.*"`.
*   `-o, --output <format>`: Output format for the report. Can be `"text"` (default) or `"json"`.

### Examples

1.  **Scan the current directory for files older than 90 days (default):**
    ```bash
    dust-bunny-sweeper .
    ```

2.  **Scan a specific project directory for files older than 180 days:**
    ```bash
    dust-bunny-sweeper /path/to/my/old/project -t 180
    ```

3.  **Scan, ignoring `node_modules` and `.git` directories, and output as JSON:**
    ```bash
    dust-bunny-sweeper . -i "node_modules" ".git" "temp_files_.*" -o json
    ```

4.  **Scan your home directory (be careful!):**
    ```bash
    dust-bunny-sweeper ~/ -t 365 -i "Library" "Downloads"
    ```

## Development

### Running Tests

To run the automated tests:

```bash
npm test
# or yarn test
```

The tests use `jest` and mock the file system (`fs.promises`) to ensure determinism and avoid actual file operations.

### Linting

To lint the TypeScript code:

```bash
npm run lint
# or yarn lint
```

## Contributing

Feel free to sweep in with improvements or new features! Open an issue or submit a pull request.
