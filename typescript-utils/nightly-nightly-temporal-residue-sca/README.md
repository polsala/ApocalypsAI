# Nightly Temporal Residue Scanner

## Overview

The `nightly-temporal-residue-scanner` is a whimsical-yet-useful utility designed to help you declutter your digital workspace. It scans specified project directories for "temporal residue" – files and folders that haven't been modified in a long time, or match patterns that typically indicate forgotten experimental branches, old build artifacts, or general cruft.

By identifying these digital ghosts, the scanner helps you maintain a cleaner, more efficient project structure, reducing cognitive load and potential build issues.

## Features

*   **Age-based Detection**: Flags files and directories older than a specified number of days.
*   **Configurable Ignores**: Easily exclude common directories like `node_modules`, `.git`, `dist`, etc.
*   **Recursive Scanning**: Traverses subdirectories to find hidden residue.
*   **Clear Reporting**: Provides a list of identified residue items with their paths, types, last modified dates, and reasons for flagging.
*   **Type-Safe**: Built with TypeScript for robust and maintainable code.

## Installation

To use this utility, you need Node.js (which includes npm or yarn) installed on your system.

1.  **Create a directory** for the utility:
    ```bash
    mkdir nightly-temporal-residue-scanner
    cd nightly-temporal-residue-scanner
    ```
2.  **Create `package.json`** (or copy the one provided in `src/package.json`):
    ```json
    {
      "name": "nightly-temporal-residue-scanner",
      "version": "1.0.0",
      "description": "Scans project directories for forgotten or unused files and folders, identifying 'temporal residue' based on age and patterns.",
      "main": "dist/index.js",
      "types": "dist/index.d.ts",
      "bin": {
        "nightly-temporal-residue-scanner": "./dist/index.js"
      },
      "scripts": {
        "build": "rimraf dist && tsc",
        "start": "npm run build && node dist/index.js",
        "test": "jest",
        "prepublishOnly": "npm run build"
      },
      "keywords": [
        "cli",
        "utility",
        "typescript",
        "cleanup",
        "files",
        "directories",
        "residue"
      ],
      "author": "ApocalypsAI Integrator Agent",
      "license": "MIT",
      "dependencies": {
        "chalk": "^4.1.2",
        "commander": "^12.0.0"
      },
      "devDependencies": {
        "@types/jest": "^29.5.12",
        "@types/node": "^20.12.7",
        "jest": "^29.7.0",
        "rimraf": "^5.0.5",
        "ts-jest": "^29.1.2",
        "ts-node": "^10.9.2",
        "typescript": "^5.4.5"
      }
    }
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    # or yarn install
    ```
4.  **Create `tsconfig.json`** (or copy the one provided in `src/tsconfig.json`):
    ```json
    {
      "compilerOptions": {
        "target": "es2020",
        "module": "commonjs",
        "outDir": "./dist",
        "rootDir": "./src",
        "strict": true,
        "esModuleInterop": true,
        "skipLibCheck": true,
        "forceConsistentCasingInFileNames": true,
        "declaration": true
      },
      "include": ["src/**/*.ts"],
      "exclude": ["node_modules", "dist"]
    }
    ```
5.  **Build the project**:
    ```bash
    npm run build
    ```

## Usage

Run the scanner from your project root or any directory you wish to inspect:

```bash
npx nightly-temporal-residue-scanner [path_to_scan] [options]
```

### Arguments

*   `[path_to_scan]` (optional): The directory to scan. Defaults to the current working directory (`.`).

### Options

*   `-a, --min-age <days>`: Minimum age in days for a file/directory to be considered residue. Defaults to `90` days.
*   `-i, --ignore <patterns...>`: Space-separated patterns (substrings) to ignore. Paths containing any of these patterns will be skipped. Defaults to `node_modules .git dist build`.

### Examples

Scan the current directory for items older than 60 days, ignoring `temp` folders:
```bash
npx nightly-temporal-residue-scanner --min-age 60 --ignore node_modules .git dist build temp
```

Scan a specific `legacy-module` directory for items older than a year (365 days):
```bash
npx nightly-temporal-residue-scanner ./legacy-module --min-age 365
```

## Development

### Running Tests

```bash
npm test
```

### Building

```bash
npm run build
```

### Running directly (for development)

```bash
npm start -- [path_to_scan] [options]
```
