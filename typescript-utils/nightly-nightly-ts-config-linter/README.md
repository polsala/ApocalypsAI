# nightly-ts-config-linter

A whimsical yet useful standalone utility for the ApocalypsAI community. This tool, built with TypeScript, provides a type-safe way to lint configuration files against a predefined schema. It's designed to catch common configuration errors before they cause issues in your deployments or workflows.

## Features

*   **Type-Safe Linting**: Leverages TypeScript's strong typing to ensure configuration adheres to expected structures.
*   **Customizable Schemas**: Define your own JSON schemas for configuration validation.
*   **Clear Error Reporting**: Provides detailed messages for any validation failures.
*   **Standalone Utility**: Easy to integrate into CI/CD pipelines or run manually.

## Installation

```bash
npm install -g @apocalypsai/nightly-ts-config-linter
```

## Usage

```bash
nightly-ts-config-linter --config <path-to-config-file> --schema <path-to-schema-file>
```

**Arguments**:

*   `--config`: Path to the configuration file to be linted (JSON format).
*   `--schema`: Path to the JSON schema file used for validation.

## Example

Let's say you have a `config.json` file:

```json
{
  "server": {
    "port": 8080,
    "timeout": 30
  },
  "database": {
    "host": "localhost",
    "port": 5432
  }
}
```

And a `schema.json` file:

```json
{
  "type": "object",
  "properties": {
    "server": {
      "type": "object",
      "properties": {
        "port": {"type": "integer", "minimum": 1024, "maximum": 65535},
        "timeout": {"type": "integer", "minimum": 10}
      },
      "required": ["port", "timeout"]
    },
    "database": {
      "type": "object",
      "properties": {
        "host": {"type": "string"},
        "port": {"type": "integer"}
      },
      "required": ["host", "port"]
    }
  },
  "required": ["server", "database"]
}
```

Running the linter:

```bash
nightly-ts-config-linter --config config.json --schema schema.json
```

If `config.json` is valid, there will be no output. If there are errors, you'll see messages like:

```
Configuration validation failed:
  server.port: Must be greater than or equal to 1024
```

## Development

This project uses Node.js and npm. To set up for development:

1.  Clone the repository.
2.  Navigate to the `utils/nightly-ts-config-linter` directory.
3.  Run `npm install`.
4.  To build: `npm run build`.
5.  To run tests: `npm test`.
