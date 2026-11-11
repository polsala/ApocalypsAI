# Nightly TypeScript Type Checker CLI

This utility provides a command-line interface (CLI) to validate JSON data against a specified TypeScript interface. It's designed to ensure data integrity by checking if incoming JSON conforms to a predefined structure.

## Features

*   **Type Safety**: Enforces type constraints defined in TypeScript interfaces.
*   **JSON Validation**: Validates JSON data against a given interface.
*   **CLI Interface**: Easy to use from the command line.
*   **Self-Contained**: Written in TypeScript, runnable with Node.js.

## Installation

1.  Clone the repository.
2.  Navigate to the `utils/nightly-ts-type-checker-cli` directory.
3.  Install dependencies: `npm install`

## Usage

```bash
npx ts-type-checker --interface-file <path_to_interface.ts> --data-file <path_to_data.json>
```

**Arguments**:

*   `--interface-file` (required): Path to the TypeScript file containing the interface definition.
*   `--data-file` (required): Path to the JSON file containing the data to validate.

**Example**:

Assume you have `UserInterface.ts`:

```typescript
export interface User {
  id: number;
  name: string;
  isActive?: boolean;
}
```

And `userData.json`:

```json
{
  "id": 123,
  "name": "Alice",
  "isActive": true
}
```

Run the command:

```bash
npx ts-type-checker --interface-file UserInterface.ts --data-file userData.json
```

If the data is valid, the tool will exit silently or print a success message. If invalid, it will print an error message detailing the discrepancies.

## Development

To build and run locally:

1.  `npm install`
2.  `npm run build`
3.  `node dist/main.js --interface-file <path_to_interface.ts> --data-file <path_to_data.json>`

## Testing

Run tests using:

```bash
npm test
```
