# nightly-ts-config-linter

A whimsical yet useful standalone utility for the ApocalypsAI community. This tool, built with TypeScript, acts as a linter for common configuration file formats (like JSON and YAML), helping to catch subtle errors and enforce best practices.

## Philosophy

"Anarchy with discipline" — this utility is designed to be flexible and easy to use, while providing robust checks to maintain order in your configuration chaos.

## Features

*   **Type-safe linting**: Leverages TypeScript's strong typing to ensure reliable checks.
*   **Configurable rules**: Easily extendable to add new linting rules.
*   **Supports JSON and YAML**: Handles common configuration formats.
*   **Whimsical error messages**: Provides helpful, yet slightly playful, feedback.

## Installation

```bash
npm install -g @apocalypsai/nightly-ts-config-linter
```

## Usage

```bash
nightly-ts-config-linter <path_to_config_file>
```

**Example**: 
```bash
nightly-ts-config-linter ./my-app-config.json
```

## Development

This project is built with TypeScript. To run locally:

1.  Clone the repository.
2.  Navigate to the `utils/nightly-ts-config-linter` directory.
3.  Run `npm install`.
4.  Run `npm run build` to compile the TypeScript code.
5.  The executable will be in the `dist` directory.

## Testing

Tests are written using Jest. Run them with:

```bash
npm test
```
