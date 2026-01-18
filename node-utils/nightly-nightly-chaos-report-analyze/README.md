# nightly-chaos-report-analyzer

A Node.js utility that parses and analyzes chaos engineering reports to extract key metrics like failure patterns, system resilience score, and error distribution.

## Features

- Parses structured chaos reports (YAML or JSON)
- Computes resilience score based on failure rate
- Identifies top failure categories
- CLI and programmatic interfaces

## Usage

```bash
npx nightly-chaos-report-analyzer --input report.yaml
```

## Programmatic Usage

```js
const analyze = require('nightly-chaos-report-analyzer');
const result = analyze({ failures: [...] });
console.log(result);
```
