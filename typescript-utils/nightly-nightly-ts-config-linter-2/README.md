## Nightly TypeScript Configuration Linter

This utility provides a simple, type-safe way to lint common configuration file formats (JSON, YAML) for basic errors and inconsistencies. It's designed to catch common mistakes before they cause runtime issues.

### Features

*   **Type Safety**: Leverages TypeScript for robust configuration validation.
*   **JSON & YAML Support**: Can lint both JSON and YAML configuration files.
*   **Customizable Rules**: Easily extendable with new linting rules.
*   **Error Reporting**: Provides clear, actionable error messages.

### Installation

```bash
npm install --save-dev @apocalypsai/nightly-ts-config-linter
```

### Usage

Run the linter from your project's root directory:

```bash
npx @apocalypsai/nightly-ts-config-linter <path_to_config_file>
```

**Example**: Linting a `package.json` file:

```bash
npx @apocalypsai/nightly-ts-config-linter ./package.json
```

**Example**: Linting a `config.yaml` file:

```bash
npx @apocalypsai/nightly-ts-config-linter ./config.yaml
```

### Linting Rules (Built-in)

*   **JSON**: Checks for valid JSON syntax.
*   **YAML**: Checks for valid YAML syntax.
*   **Required Fields**: Ensures essential fields are present in the configuration.
*   **Type Mismatches**: Verifies that values match expected types (e.g., string, number, boolean).

### Extending Rules

To add custom rules, you would typically modify the `src/linter.ts` file and add new validation logic to the `lintConfig` function or create separate rule modules.

### Development

To run the linter locally:

```bash
npm install
npm run build
node dist/index.js <path_to_config_file>
```

To run tests:

```bash
npm test
```
