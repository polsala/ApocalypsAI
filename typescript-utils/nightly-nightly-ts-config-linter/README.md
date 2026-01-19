# Nightly TypeScript Configuration Linter

This utility provides a type-safe way to lint common configuration file formats (JSON, YAML) for structural integrity and adherence to predefined schemas. It's designed to catch common mistakes before they cause runtime issues.

## Features

*   **Type Safety**: Leverages TypeScript for robust configuration validation.
*   **JSON & YAML Support**: Can lint both JSON and YAML configuration files.
*   **Customizable Schemas**: Define your own schemas for validation.
*   **Error Reporting**: Provides clear, actionable error messages.

## Installation

```bash
npm install -g @apocalypsai/nightly-ts-config-linter
```

## Usage

```bash
nightly-ts-config-linter <file_path> [--schema <schema_path>]
```

**Arguments**:

*   `<file_path>`: The path to the configuration file to lint.
*   `--schema <schema_path>`: (Optional) The path to a JSON schema file for validation.

## Examples

Lint a JSON file with default checks:

```bash
nightly-ts-config-linter ./my-app-config.json
```

Lint a YAML file using a custom schema:

```bash
nightly-ts-config-linter ./service.yaml --schema ./service-schema.json
```

## Development

To build and test locally:

```bash
npm install
npm run build
npm test
```
