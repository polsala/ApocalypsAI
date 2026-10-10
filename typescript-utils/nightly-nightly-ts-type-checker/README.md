# Nightly TypeScript Type Checker

This utility provides a whimsical yet functional way to check for type mismatches within a given TypeScript code snippet. It leverages the power of the TypeScript compiler API to analyze code and report potential type errors.

## Features

*   Analyzes provided TypeScript code for type errors.
*   Reports errors with line and character numbers.
*   Provides a clear, human-readable output of detected issues.

## Usage

1.  **Install Dependencies:**
    ```bash
    npm install typescript
    ```

2.  **Run the utility:**
    You can run this utility directly from your terminal. It expects a TypeScript code snippet as input.

    ```bash
    # Example usage (assuming you have the script saved as check_types.ts)
    # You would typically pipe code into it or modify it to read from a file.
    echo "let message: string = 123;" | ts-node src/main.ts
    ```

    Alternatively, you can modify the `src/main.ts` to read from a file path provided as a command-line argument.

## Development

This utility is built using TypeScript and Node.js. Tests are included to ensure its functionality.

## License

This project is licensed under the MIT License.
