## Nightly TypeScript Configuration Linter

This utility provides a simple, type-safe way to lint common configuration file formats (JSON, YAML) for basic syntax errors and potential inconsistencies. It's designed to catch common mistakes before they cause runtime issues.

### Features

*   **Type-Safe Linting**: Leverages TypeScript for robust type checking.
*   **JSON Support**: Detects syntax errors in JSON files.
*   **YAML Support**: Detects basic syntax errors in YAML files (using a common library).
*   **Customizable Rules (Future)**: Placeholder for future rule expansion.

### Installation

```bash
npm install --save-dev @apocalypsai/nightly-ts-config-linter
```

### Usage

Run the linter from your terminal:

```bash
npx @apocalypsai/nightly-ts-config-linter <path_to_config_file>
```

**Example**: 

```bash
npx @apocalypsai/nightly-ts-config-linter ./config.json
```

If the file is valid, the utility will exit with code 0. If errors are found, it will print the errors and exit with a non-zero code.

### Development

To run the linter locally:

```bash
npm install
npx ts-node src/index.ts <path_to_config_file>
```

### Testing

Tests are included and can be run with:

```bash
npm test
```
