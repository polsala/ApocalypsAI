# Nightly Echo Reframe CLI

## Overview

The `nightly-echo-reframe-cli` is a whimsical-yet-useful command-line interface (CLI) tool designed to help you process and learn from past 'temporal echoes' – those moments of regret, mistakes, or negative experiences that linger in your mind. Instead of dwelling on them, this tool encourages you to log these echoes and then actively reframe them into positive lessons and concrete future actions.

It's built with TypeScript, ensuring type-safe data handling for your echoes.

## Features

*   **Log Temporal Echoes**: Record a past event, its negative impact, and a timestamp.
*   **Reframe Echoes**: Transform a raw, logged echo into a positive lesson and a specific action plan.
*   **List Echoes**: View all your temporal echoes, distinguishing between raw and reframed ones.
*   **Persistence**: All echoes are stored locally in a `data/echoes.json` file.

## Installation

1.  **Navigate to the utility directory**:
    ```bash
    cd typescript-utils/nightly-echo-reframe-cli
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```
3.  **Build the TypeScript project**:
    ```bash
    npm run build
    ```

## Usage

Run the CLI using `npm start` followed by a command.

### 1. Log a new Temporal Echo

Record a past event and its negative impact.

```bash
npm start log "<description_of_echo>" "<negative_impact_or_feeling>"
```

**Example**:
```bash
npm start log "Forgot to save my work before a crash" "Lost 3 hours of progress"
```

### 2. Reframe an existing Temporal Echo

Take a raw echo (identified by its ID) and transform it into a positive lesson and a future action.

```bash
npm start reframe <echo_id> "<lesson_learned>" "<concrete_action_to_take>"
```

**Example** (replace `your-echo-id` with an actual ID from `list` command):
```bash
npm start reframe your-echo-id "Always save frequently" "Set up auto-save every 5 minutes"
```

### 3. List Temporal Echoes

View all logged echoes, optionally filtering by status.

```bash
npm start list [raw|reframed]
```

*   `npm start list`: Lists all echoes (raw and reframed).
*   `npm start list raw`: Lists only raw (unreframed) echoes.
*   `npm start list reframed`: Lists only reframed echoes.

**Example**:
```bash
npm start list
```

### 4. Get Help

```bash
npm start help
```

## Development

To run tests:

```bash
npm test
```

This will execute the Jest test suite, ensuring the core logic for managing echoes is functioning correctly. File system operations are mocked to ensure deterministic and offline testing.
