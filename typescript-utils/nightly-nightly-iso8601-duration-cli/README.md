# nightly‑iso8601‑duration‑cli

A tiny, zero‑dependency TypeScript command‑line utility that turns an ISO‑8601 duration (e.g. `P1Y2M3DT4H5M6S`) into a human‑readable English phrase.

## Features

- Parses years, months, weeks, days, hours, minutes, and seconds.
- Handles both date‑only (`P3W`) and time‑only (`PT20M`) forms.
- Returns a concise, comma‑separated description.
- Provides helpful error messages for malformed inputs.

## Installation

```bash
# Using npm (requires node >= 16)
npm install -g ts-node typescript
# Then you can run the script directly with ts-node
```

> The utility is deliberately lightweight – it only depends on the Node standard library.

## Usage

```bash
# Run with ts-node (no compilation needed)
ts-node src/index.ts <ISO‑8601‑duration>
```

Example:

```bash
$ ts-node src/index.ts P1Y2M3DT4H5M6S
1 year, 2 months, 3 days, 4 hours, 5 minutes, 6 seconds
```

If the input cannot be parsed, the tool exits with a non‑zero status and prints an error message.

## Development & Testing

```bash
# Install dev dependencies (jest is used for tests)
npm install --save-dev jest @types/jest ts-jest

# Run tests
npm test
```

## License

MIT © ApocalypsAI community
