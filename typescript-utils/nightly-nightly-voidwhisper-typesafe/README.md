# nightly-voidwhisper-typesafe-config-validator

A lightweight, zero-dependency TypeScript utility that validates environment variables against a defined schema with full type inference.

## Features

- Type-safe validation of environment variables
- Zero external dependencies
- Easy-to-use fluent API
- Comprehensive error reporting

## Usage

```ts
import { createConfigSchema } from './src/main';

const schema = createConfigSchema({
  PORT: { type: 'number', required: true },
  NODE_ENV: { type: 'string', required: false, default: 'development' }
});

const config = schema.parse(process.env);
console.log(config.PORT); // strongly typed number
```

## Installation

Just copy the files into your project!

## License

MIT
