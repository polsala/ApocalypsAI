# Nightly Void Echo Type Checker

This utility provides a type-safe mechanism to define and validate 'void echo' messages – informational outputs that are not expected to return data but should conform to a specific structure. Think of it as a guardian for your console logs, status updates, or non-critical API responses, ensuring consistency and clarity in the 'echoes from the void'.

## Features

- **Type-Safe Schema Definition**: Define schemas for string-based messages (using regular expressions) or JSON-based messages (specifying properties, types, and optionality).
- **Message Validation**: Validate incoming messages against registered schemas.
- **CLI Tool**: Easily validate messages from the command line.
- **Extensible**: Register your own custom schemas programmatically.

## Installation

1. Navigate to the utility's directory:
   ```bash
   cd typescript-utils/nightly-void-echo-type-checker
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Build the TypeScript project:
   ```bash
   npm run build
   ```

## Usage

### Command Line Interface (CLI)

The CLI tool allows you to validate messages directly. It comes with a few pre-registered schemas (`simple-status`, `structured-log`, `anomaly-report`).

```bash
# General usage
nightly-void-echo-type-checker validate <schema-name> <message-type> <message-content>

# Example: Validating a string message
nightly-void-echo-type-checker validate simple-status string "VOID ECHO: INFO: System check passed."
# Output: ✅ Message is valid against schema "simple-status".

nightly-void-echo-type-checker validate simple-status string "Just a random message."
# Output: ❌ Message is INVALID against schema "simple-status".
#         - Message does not match pattern "^VOID ECHO: (INFO|WARNING|ERROR): .+".

# Example: Validating a JSON message
nightly-void-echo-type-checker validate structured-log json '{"timestamp":1678886400000,"level":"INFO","message":"Service started."}'
# Output: ✅ Message is valid against schema "structured-log".

nightly-void-echo-type-checker validate structured-log json '{"timestamp":1678886400000,"level":"CRITICAL","message":"Service failed."}'
# Output: ❌ Message is INVALID against schema "structured-log".
#         - Property "level" value "CRITICAL" is not one of the allowed enum values: INFO, WARN, ERROR.

# Example: Validating an anomaly report
nightly-void-echo-type-checker validate anomaly-report json '{"anomalyId":"ANOM-001","severity":5,"description":"High CPU usage detected","detectedAt":"2023-03-15T10:00:00Z"}'
# Output: ✅ Message is valid against schema "anomaly-report".
```

### Programmatic Usage (as a Library)

You can import and use the `VoidEchoTypeChecker` in your TypeScript/JavaScript projects.

```typescript
import { VoidEchoTypeChecker, registerDefaultSchemas } from 'nightly-void-echo-type-checker';

const checker = new VoidEchoTypeChecker();
registerDefaultSchemas(checker); // Register the default schemas

// Register a custom schema
checker.registerSchema('custom-alert', {
  type: 'json',
  properties: {
    alertId: { type: 'string', required: true },
    severity: { type: 'string', required: true, enum: ['low', 'medium', 'high'] },
    details: { type: 'string', required: false }
  }
});

const validMessage = {
  alertId: 'CUST-001',
  severity: 'high',
  details: 'Disk space low'
};

const invalidMessage = {
  alertId: 'CUST-002',
  severity: 'critical' // Not in enum
};

console.log('Valid message check:', checker.validate('custom-alert', validMessage));
// Output: { isValid: true }

console.log('Invalid message check:', checker.validate('custom-alert', invalidMessage));
// Output: { isValid: false, errors: [ 'Property "severity" value "critical" is not one of the allowed enum values: low, medium, high.' ] }
```

## Development

### Build
```bash
npm run build
```

### Test
```bash
npm test
```

## Schemas

### `simple-status` (string)

Matches strings like `"VOID ECHO: INFO: All systems nominal."`

- **Pattern**: `^VOID ECHO: (INFO|WARNING|ERROR): .+$`

### `structured-log` (json)

Matches JSON objects with:

- `timestamp`: `number` (required)
- `level`: `string` (required, must be `INFO`, `WARN`, or `ERROR`)
- `message`: `string` (required)
- `source`: `string` (optional)

### `anomaly-report` (json)

Matches JSON objects with:

- `anomalyId`: `string` (required)
- `severity`: `number` (required, must be `1` to `5`)
- `description`: `string` (required)
- `detectedAt`: `string` (required, e.g., ISO 8601 string)
- `resolutionSteps`: `array` (optional, checks if it's an array, no item validation)
