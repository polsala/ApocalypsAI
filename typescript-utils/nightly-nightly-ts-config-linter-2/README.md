## Nightly TypeScript Configuration Linter

This utility provides a robust and type-safe way to validate JSON configuration files against a predefined schema. It's designed to catch common configuration errors early, ensuring consistency and preventing runtime issues.

### Features

*   **Type-Safe Validation**: Leverages TypeScript's type system for schema definition and validation.
*   **Clear Error Reporting**: Provides detailed, human-readable error messages for validation failures.
*   **Schema-Driven**: Configuration is validated against a JSON schema, making it flexible and extensible.
*   **Command-Line Interface**: Easy to integrate into CI/CD pipelines or use for manual checks.

### Installation

```bash
npm install --save-dev @apocalypsai/nightly-ts-config-linter
```

### Usage

To lint a configuration file:

```bash
npx ts-config-linter --config <path_to_config.json> --schema <path_to_schema.json>
```

**Arguments**:

*   `--config`: Path to the JSON configuration file to validate.
*   `--schema`: Path to the JSON schema file.

### Example

**`config.json`**:

```json
{
  "appName": "MyAwesomeApp",
  "version": "1.2.3",
  "port": 8080,
  "features": {
    "darkMode": true,
    "betaFeatures": false
  }
}
```

**`schema.json`**:

```json
{
  "type": "object",
  "properties": {
    "appName": {"type": "string"},
    "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
    "port": {"type": "integer", "minimum": 1024, "maximum": 65535},
    "features": {
      "type": "object",
      "properties": {
        "darkMode": {"type": "boolean"},
        "betaFeatures": {"type": "boolean"}
      },
      "required": ["darkMode", "betaFeatures"]
    }
  },
  "required": ["appName", "version", "port", "features"]
}
```

**Running the linter**:

```bash
npx ts-config-linter --config config.json --schema schema.json
```

**Expected Output (if valid)**:

(No output, process exits with code 0)

**Example of invalid configuration**:

If `config.json` had `"port": 80`, the output would be:

```
Configuration validation failed:
  - Property 'port' must be >= 1024 and <= 65535.
```

### Development

To build and test locally:

```bash
npm install
npm run build
npm test
```
