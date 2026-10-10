## Nightly TypeScript Configuration Linter

This utility provides a simple yet effective way to lint common configuration files (like JSON, YAML, and potentially others) using TypeScript. It aims to catch common mistakes, enforce basic structural integrity, and ensure consistency across your project's configuration.

### Features

*   **Type-safe linting**: Leverages TypeScript's type system for robust checks.
*   **Extensible rules**: Designed to be easily extended with new linting rules.
*   **JSON and YAML support**: Built-in support for common configuration formats.
*   **Command-line interface**: Easy to integrate into CI/CD pipelines or run locally.

### Installation

```bash
npm install -g @apocalypsai/nightly-ts-config-linter
```

### Usage

Run the linter on a configuration file:

```bash
npm run lint-config -- <path_to_config_file>
```

**Example**: Linting a `package.json` file:

```bash
npm run lint-config -- ./package.json
```

**Example**: Linting a `config.yaml` file:

```bash
npm run lint-config -- ./config.yaml
```

### Development

To develop or contribute:

1.  Clone the repository.
2.  Navigate to the `typescript-utils/nightly-ts-config-linter` directory.
3.  Install dependencies: `npm install`.
4.  Build the project: `npm run build`.
5.  Run tests: `npm test`.

### Contributing

Contributions are welcome! Please follow the standard ApocalypsAI contribution guidelines.
