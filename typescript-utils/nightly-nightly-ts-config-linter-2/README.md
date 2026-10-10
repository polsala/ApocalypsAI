## nightly-ts-config-linter

A whimsical yet useful utility built with TypeScript to help you keep your configuration files in tip-top shape. This linter checks for common structural issues and stylistic inconsistencies in JSON and YAML configuration files, ensuring your settings are as robust as a well-fortified bunker.

### Features

*   **Type Safety**: Leverages TypeScript for robust code and predictable behavior.
*   **JSON & YAML Support**: Can lint both JSON and YAML configuration files.
*   **Customizable Rules**: Easily extendable with new linting rules.
*   **Clear Error Reporting**: Provides informative messages for detected issues.

### Installation

```bash
npm install -g @apocalypsai/nightly-ts-config-linter
```

### Usage

To lint a configuration file:

```bash
nightly-ts-config-linter <path_to_config_file>
```

**Example**: 

```bash
nightly-ts-config-linter ./my-app-config.json
```

### Development

This project is built with TypeScript and uses Jest for testing.

1.  Clone the repository.
2.  Navigate to the `utils/nightly-ts-config-linter` directory.
3.  Run `npm install` to install dependencies.
4.  Run `npm run build` to compile TypeScript to JavaScript.
5.  Run `npm test` to execute the test suite.

### Contributing

Contributions are welcome! Please follow the standard ApocalypsAI contribution guidelines.
