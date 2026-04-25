# nightly-voidbound-validator

A lightweight, type-safe configuration validator written in TypeScript. Ensures your deeply nested objects conform strictly to expected schemas.

## Features

- Zero runtime dependencies
- Strict type inference from schema definitions
- Helpful path-based error messages
- Works in Node.js and browser environments

## Installation

```sh
npm install nightly-voidbound-validator
```

## Usage

```ts
import { createValidator } from 'nightly-voidbound-validator';

const configSchema = {
  server: {
    port: 'number',
    host: 'string'
  },
  features: [
    {
      name: 'string',
      enabled: 'boolean'
    }
  ]
};

const validate = createValidator(configSchema);

const result = validate({
  server: { port: 3000, host: "localhost" },
  features: [{ name: "auth", enabled: true }]
});

if (!result.valid) {
  console.error(result.errors); // shows exact mismatch paths
}
```

## License
MIT
