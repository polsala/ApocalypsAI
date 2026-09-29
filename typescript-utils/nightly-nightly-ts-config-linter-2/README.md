## Nightly TypeScript Configuration Linter

This utility provides a robust and type-safe way to lint various configuration files using TypeScript. It aims to catch common errors, enforce best practices, and ensure consistency across your project's configurations.

### Features

*   **Type-Safe Linting**: Leverages TypeScript's type system to validate configuration structures.
*   **Customizable Rules**: Easily extendable with new linting rules.
*   **Support for Common Formats**: Currently supports JSON and YAML configuration files.
*   **Clear Error Reporting**: Provides detailed messages for detected issues.

### Installation

```bash
npm install --save-dev @apocalypsai/nightly-ts-config-linter
```

### Usage

Run the linter from your terminal:

```bash
npx @apocalypsai/nightly-ts-config-linter --file path/to/your/config.json
```

Or, programmatically:

```typescript
import { lintConfig } from '@apocalypsai/nightly-ts-config-linter';

async function runLint() {
  const configContent = '{ "port": 8080, "database": { "host": "localhost" } }';
  const filePath = 'config.json';
  const errors = await lintConfig(configContent, filePath);

  if (errors.length > 0) {
    console.error('Configuration errors found:');
    errors.forEach(err => console.error(`- ${err.message} (at ${err.location})`));
  } else {
    console.log('Configuration is valid!');
  }
}

runLint();
```

### Configuration

Create a `.ts-config-linterrc.json` file in your project root to define custom rules or specify files to ignore.

```json
{
  "rules": {
    "require-port": "error",
    "valid-database-host": "warn"
  },
  "ignore": [
    "**/deprecated-config.json"
  ]
}
```

### Developing New Rules

To add a new rule, create a new file in the `rules/` directory and export a function that takes the configuration object and returns an array of `LintError` objects.

### Testing

Run tests using:

```bash
npm test
```
