# Nightly TypeScript Type Checker

This utility provides a robust way to validate JSON data against a TypeScript interface definition. It helps ensure that incoming data conforms to expected types, preventing runtime errors and improving data integrity.

## Features

*   Type-safe validation of JSON objects.
*   Uses TypeScript interfaces for schema definition.
*   Clear error reporting for validation failures.

## Installation

```bash
npm install --save-dev typescript ts-node @types/node
```

## Usage

1.  **Define your TypeScript interface (schema):**
    ```typescript
    // src/schema.ts
    export interface UserProfile {
      id: number;
      username: string;
      email?: string; // Optional field
      isActive: boolean;
      roles: string[];
    }
    ```

2.  **Create your JSON data:**
    ```json
    // data.json
    {
      "id": 123,
      "username": "apocalypse_ai",
      "email": "ai@example.com",
      "isActive": true,
      "roles": ["admin", "user"]
    }
    ```

3.  **Run the type checker:**
    ```bash
    npx ts-node src/main.ts --schema src/schema.ts --data data.json
    ```

    Or, if you have compiled the TypeScript code:
    ```bash
    node dist/main.js --schema src/schema.ts --data data.json
    ```

## Command Line Arguments

*   `--schema <path>`: Path to the TypeScript file defining the interface.
*   `--data <path>`: Path to the JSON file containing the data to validate.

## Example Output (Success)

```
Data is valid according to the schema.
```

## Example Output (Failure)

```
Validation failed:
- Property 'username' is missing.
- Property 'isActive' is missing.
```
