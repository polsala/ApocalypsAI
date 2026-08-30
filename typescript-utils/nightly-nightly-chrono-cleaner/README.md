# Nightly Chrono-Cleaner

A TypeScript CLI tool designed to help the community maintain a pristine project timeline by identifying and reporting 'temporal echoes' – files that are stale, unused, or explicitly marked as deprecated/archived.

## Summary
In the ever-shifting sands of the digital wasteland, codebases can accumulate digital detritus. The Nightly Chrono-Cleaner scans your project for files that haven't been touched in ages or contain specific markers indicating they're past their prime. It then provides a clear report, allowing you to decide whether to archive, refactor, or simply delete these echoes from the past.

## Features
*   **Staleness Detection**: Identifies files not modified within a configurable number of days.
*   **Deprecated Marker Scan**: Finds files containing common 'DEPRECATED' or 'ARCHIVED' comments/annotations.
*   **Configurable**: Set scan paths, staleness thresholds, and ignore patterns.
*   **Output Formats**: Get reports in human-readable text or machine-parseable JSON.
*   **Type-Safe**: Built with TypeScript for robust and predictable operation.

## Installation
To use the Nightly Chrono-Cleaner, you'll need Node.js (v16 or higher) and npm/yarn installed.

1.  Navigate to the `nightly-chrono-cleaner` directory.
2.  Install dependencies:
    ```bash
    npm install
    # or
    yarn install
    ```
3.  Build the TypeScript project:
    ```bash
    npm run build
    # or
    yarn build
    ```

## Usage
Run the utility directly using `npx` or by executing the compiled JavaScript.

```bash
npx nightly-chrono-cleaner [options]
```

### Options
*   `--path <dir>`: The directory to scan (default: current working directory `.`).
*   `--stale-days <num>`: Number of days after which a file is considered stale (default: `365`).
*   `--ignore <pattern>`: Comma-separated patterns to ignore (e.g., `node_modules,dist,.git`).
*   `--format <type>`: Output format: `'text'` or `'json'` (default: `text`).
*   `--help`: Display the help message.

### Examples

Scan the current directory for files older than 180 days:
```bash
npx nightly-chrono-cleaner --stale-days 180
```

Scan a specific source directory, ignoring common build/dependency folders, and output as JSON:
```bash
npx nightly-chrono-cleaner --path ./src --ignore "node_modules,dist,.git,coverage" --format json
```

Get help:
```bash
npx nightly-chrono-cleaner --help
```

## Development

### Running Tests
```bash
npm test
# or
yarn test
```

### Project Structure
```
nightly-chrono-cleaner/
├── README.md
├── package.json
├── tsconfig.json
├── jest.config.js
├── src/
│   ├── index.ts      # CLI entry point and argument parsing
│   ├── scanner.ts    # Core logic for scanning files and detecting echoes
│   └── types.ts      # TypeScript interfaces for configuration and results
└── tests/
    └── scanner.test.ts # Unit tests for the scanner logic
```

## Contributing
Feel free to contribute to the Nightly Chrono-Cleaner by opening issues or submitting pull requests. Let's keep our digital timelines clean!
