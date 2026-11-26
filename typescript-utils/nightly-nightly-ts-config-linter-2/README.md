A whimsical yet useful utility to ensure your configuration files are in tip-top shape!

This tool, `nightly-ts-config-linter`, is built with TypeScript and provides a simple way to check common configuration file formats (like JSON and YAML) for basic errors and potential issues.

## Features

*   **Type Safety**: Leverages TypeScript for robust code.
*   **JSON Linting**: Checks for syntax errors and common pitfalls in JSON files.
*   **YAML Linting**: Basic checks for YAML file validity.
*   **Customizable Rules (Future)**: Designed for easy expansion with custom linting rules.

## Installation

```bash
npm install -g @apocalypsai/nightly-ts-config-linter
```

## Usage

```bash
nightly-ts-config-linter <path_to_config_file>
```

**Example:**

```bash
nightly-ts-config-linter ./my-app-config.json
```

## How it Works

The linter reads the specified configuration file, attempts to parse it as JSON or YAML, and then applies a set of predefined checks. It reports any detected issues to the console.

## Development

To develop or contribute:

1.  Clone the repository.
2.  Navigate to the `utils/nightly-ts-config-linter` directory.
3.  Install dependencies: `npm install`
4.  Build the project: `npm run build`
5.  Run tests: `npm test`

## License

This project is licensed under the MIT License.
