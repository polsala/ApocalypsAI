## Nightly TypeScript Configuration Linter

This utility provides a simple, type-safe way to lint common configuration files (like JSON, YAML) for potential errors and inconsistencies. It's designed to be easily extensible with custom rules.

### Features

*   Type-safe parsing of configuration files.
*   Basic rule set for common issues (e.g., missing required fields, invalid data types).
*   Extensible architecture for adding new rules.

### Installation

```bash
npm install --save-dev @apocalypsai/nightly-ts-config-linter
```

### Usage

Run the linter from your terminal:

```bash
npx @apocalypsai/nightly-ts-config-linter <path_to_config_file>
```

### Example Configuration File (`config.json`)

```json
{
  "appName": "ApocalypseApp",
  "version": "1.0.0",
  "logLevel": "INFO",
  "features": {
    "newUI": true,
    "betaFeature": false
  }
}
```

### Example Usage with a JSON file:

```bash
npx @apocalypsai/nightly-ts-config-linter config.json
```

### Example Usage with a YAML file (requires `js-yaml` to be installed in the project):

```bash
npx @apocalypsai/nightly-ts-config-linter config.yaml
```

### Adding Custom Rules

To add custom rules, you can extend the `Rule` interface and register them with the `Linter` class.

### Development

To run the linter locally:

```bash
npm install
npx ts-node src/index.ts <path_to_config_file>
```

### Testing

Run the tests:

```bash
npm test
```
