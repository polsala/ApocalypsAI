# Nightly Dependency Dragon Tamer

A whimsical CLI tool to help you tame your project's outdated dependencies. This utility scans your `package.json` file, consults the mighty npm registry, and reports which of your project's dependencies are acting like unruly dragons – outdated and potentially causing chaos.

## Features

*   **Dependency Scan**: Automatically detects `dependencies` and `devDependencies` from `package.json`.
*   **Version Check**: Compares installed versions with the latest available versions on npm.
*   **Whimsical Reporting**: Provides a clear, color-coded report of outdated packages, their current versions, and the latest available versions.
*   **Cross-Platform**: Built with Node.js, runs anywhere Node.js is supported.

## Installation

To use the Dragon Tamer, ensure you have Node.js (v18 or higher) installed.

1.  Clone this repository or download the `nightly-dependency-dragon-tamer` folder.
2.  Navigate into the `node-utils/nightly-dependency-dragon-tamer` directory.
3.  Install its own dependencies:
    ```bash
    npm install
    ```

## Usage

Run the Dragon Tamer from your project's root directory (where `package.json` resides):

```bash
node src/index.js
```

You can also specify a different path to your `package.json` file:

```bash
node src/index.js --path /path/to/your/project/package.json
```

### Example Output

```
🐉 Taming the Dependency Dragons... 🐉

Scanning package.json at: /path/to/your/project/package.json

Dependencies:
  - express: Current 4.17.1 -> Latest 4.18.2 (Outdated: Major)
  - lodash: Current 4.17.20 -> Latest 4.17.21 (Outdated: Patch)
  - react: Current 17.0.1 -> Latest 18.2.0 (Outdated: Major)
  - axios: Current 0.21.1 -> Latest 1.6.8 (Outdated: Major)
  - moment: Current 2.29.1 -> Latest 2.29.4 (Outdated: Minor)

Dev Dependencies:
  - jest: Current 26.6.3 -> Latest 29.7.0 (Outdated: Major)
  - eslint: Current 7.28.0 -> Latest 8.56.0 (Outdated: Major)

Summary: 7 dragons found, 7 need taming!
Run 'npm update' or 'npm install <package>@latest' to soothe them.
```

## Development

To run tests:

```bash
npm test
```
