## Nightly TypeScript Configuration Linter

This utility provides a simple, type-safe way to lint common configuration files (like JSON, YAML, or TOML) for structural inconsistencies and potential typos. It's designed to catch common mistakes before they cause runtime errors.

### Features

*   **Type-Safe Linting**: Leverages TypeScript's type system to define expected configurations.
*   **Customizable Rules**: Easily extendable with new linting rules.
*   **Support for Common Formats**: Handles JSON, YAML, and TOML out of the box.
*   **Clear Error Reporting**: Provides informative messages for detected issues.

### Installation

```bash
npm install --save-dev @apocalypsai/nightly-ts-config-linter
```

### Usage

This utility is designed to be run programmatically or via a simple CLI wrapper (not included in this basic package).

**Programmatic Usage Example:**

```typescript
import { lintConfig } from './src/linter';
import { ConfigRule } from './src/types';

const myConfig = {
  "database": {
    "host": "localhost",
    "port": 5432,
    "user": "admin"
  },
  "logging": {
    "level": "info"
  }
};

const customRules: ConfigRule[] = [
  {
    path: 'database.host',
    description: 'Database host should not be empty',
    validator: (value: any) => typeof value === 'string' && value.length > 0
  },
  {
    path: 'logging.level',
    description: 'Logging level must be one of [debug, info, warn, error]',
    validator: (value: any) => ['debug', 'info', 'warn', 'error'].includes(value)
  }
];

const errors = lintConfig(myConfig, customRules);

if (errors.length > 0) {
  console.error('Configuration errors found:');
  errors.forEach(err => console.error(`- ${err.message} (Path: ${err.path})`));
} else {
  console.log('Configuration is clean!');
}
```

### Extending Rules

To add new rules, define a `ConfigRule` object with a `path` (using dot notation), a descriptive `description`, and a `validator` function that returns `true` if the value is valid, `false` otherwise.

### Development

Run tests using:

```bash
npm test
```
