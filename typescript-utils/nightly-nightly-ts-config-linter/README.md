## nightly-ts-config-linter

A whimsical yet useful TypeScript utility designed to scan and lint various configuration files for common syntax errors, potential pitfalls, and adherence to basic structural sanity. It's like a tiny, digital inspector for your config files, ensuring they don't have any 'loose wires' or 'misplaced furniture' before they cause trouble.

### Philosophy

Configuration files are the unsung heroes of software. When they're messy, everything else can fall apart. This linter aims to catch those small, annoying errors before they escalate into full-blown apocalyptic scenarios.

### Features

*   **Type-Safe Linting**: Leverages TypeScript's type system for robust error detection.
*   **Extensible Rules**: Designed to be easily extendable with new linting rules.
*   **JSON & YAML Support**: Currently supports linting of JSON and YAML configuration files.
*   **Customizable Rulesets**: (Future enhancement) Allow users to define their own linting rules.

### Installation

```bash
npm install -g @polsala/nightly-ts-config-linter
```

### Usage

To lint a configuration file:

```bash
nightly-ts-config-linter <path_to_config_file>
```

**Example**: Linting a `package.json` file:

```bash
nightly-ts-config-linter ./package.json
```

**Example**: Linting a `docker-compose.yml` file:

```bash
nightly-ts-config-linter ./docker-compose.yml
```

### Development

To run the linter locally:

```bash
npm install
npm run build
node dist/index.js <path_to_config_file>
```

### Testing

Tests are included and can be run using Jest:

```bash
npm test
```

### Contributing

Contributions are welcome! Please follow the standard ApocalypsAI contribution guidelines.
