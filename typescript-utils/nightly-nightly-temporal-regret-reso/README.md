# Nightly Temporal Regret Resolver

A whimsical-yet-useful TypeScript CLI utility to help the community manage and find closure for their "temporal echoes" – those lingering past regrets or missed opportunities that echo through the digital void. Log them, acknowledge them, and then resolve them to clear your mental cache!

## Features

*   **Log Temporal Echoes**: Add new regrets with a description and timestamp.
*   **List Active Echoes**: View all unresolved temporal echoes.
*   **Resolve Echoes**: Mark a regret as resolved, providing a sense of digital closure.
*   **View Resolved Echoes**: See your history of conquered regrets.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.
*   **Persistent Storage**: All echoes are saved to a local JSON file (`temporal_echoes.json`).

## Installation

1.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-temporal-regret-resolver
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Build the TypeScript project:**
    ```bash
    npm run build
    ```

## Usage

After installation and building, you can run the CLI using `npm run cli <command>`.

### Add a new Temporal Echo

Log a new regret or missed opportunity.

```bash
npm run cli add "Forgot to backup my data before the temporal anomaly."
# Output: Added new temporal echo: "Forgot to backup my data before the temporal anomaly." (ID: <some-uuid>)
```

### List Active Temporal Echoes

See all your unresolved echoes.

```bash
npm run cli list active
# Output:
# --- Active Temporal Echoes ---
# ID: <some-uuid>
#   Description: "Forgot to backup my data before the temporal anomaly."
#   Logged: 3/15/2024, 10:30:00 AM
# ------------------------------
# ...
```

### List Resolved Temporal Echoes

Review the echoes you've successfully brought to closure.

```bash
npm run cli list resolved
# Output:
# --- Resolved Temporal Echoes ---
# ID: <another-uuid>
#   Description: "Didn't learn to juggle temporal paradoxes."
#   Logged: 3/10/2024, 09:00:00 AM
#   Resolved: 3/15/2024, 11:45:00 AM
# --------------------------------
# ...
```

### Resolve a Temporal Echo

Mark an echo as resolved using its unique ID.

```bash
npm run cli resolve <ID_OF_THE_REGRET>
# Example:
# npm run cli resolve 123e4567-e89b-12d3-a456-426614174000
# Output: Temporal echo "Forgot to backup my data before the temporal anomaly." (ID: 123e4567-e89b-12d3-a456-426614174000) resolved!
```

### Get Help

```bash
npm run cli help
```

## Development

### Running Tests

To run the automated tests:

```bash
npm test
```

The tests use `jest` and mock the file system to ensure they are deterministic and do not interact with actual files.

### Project Structure

```
.
├── README.md
├── package.json
├── tsconfig.json
├── jest.config.js
├── src/
│   ├── index.ts          # Main CLI entry point
│   ├── regretManager.ts  # Core logic for managing temporal echoes
│   └── types.ts          # TypeScript type definitions
└── tests/
    └── regretManager.test.ts # Unit tests for RegretManager
```
