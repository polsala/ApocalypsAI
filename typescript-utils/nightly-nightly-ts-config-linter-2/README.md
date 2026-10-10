## Nightly TypeScript Configuration Linter

This utility provides a simple yet effective way to lint common configuration files (like JSON, YAML, and TOML) for basic syntax errors and potential inconsistencies. It's built with TypeScript for type safety and ease of extension.

### Features

*   **Type-Safe Linting**: Leverages TypeScript for robust code.
*   **Multiple Formats**: Supports JSON, YAML, and TOML.
*   **Customizable Rules**: Easily extendable with new linting rules.
*   **Clear Error Reporting**: Provides informative messages for detected issues.

### Installation

```bash
npm install --save-dev @apocalypsai/nightly-ts-config-linter
```

Or, if you're using Yarn:

```bash
yarn add --dev @apocalypsai/nightly-ts-config-linter
```

### Usage

Run the linter from your terminal:

```bash
npx @apocalypsai/nightly-ts-config-linter <path-to-config-file>
```

**Example**: Linting a `package.json` file:

```bash
npx @apocalypsai/nightly-ts-config-linter ./package.json
```

**Example**: Linting a `config.yaml` file:

```bash
npx @apocalypsai/nightly-ts-config-linter ./config.yaml
```

### Development

To build and test the utility locally:

```bash
npm install
npm run build
npm test
```

### Contributing

Contributions are welcome! Please refer to the main ApocalypsAI repository for contribution guidelines.
