# Nightly Chronal Echoes

A type-safe TypeScript utility to manage 'chronal echoes' – messages or tasks from the future that manifest at their designated time, helping the community stay organized across temporal distortions.

## Overview

In the chaotic temporal landscape, it's easy to lose track of important future events or messages. The `nightly-chronal-echoes` utility provides a stable anchor, allowing you to schedule messages that will only become visible when their designated time arrives. Think of them as whispers from your future self, delivered precisely when needed.

Echoes are stored locally in a `.chronal-echoes.json` file in your current working directory, ensuring persistence across sessions.

## Installation

1.  **Ensure Node.js and npm (or yarn) are installed.**
2.  **Navigate to the utility's directory.**
3.  **Install dependencies and build the project:**

    ```bash
    npm install
    npm run build
    ```

4.  **Optionally, link the CLI tool for global access (or run directly via `node dist/index.js`):**

    ```bash
    npm link
    ```

    Now you can use `chronal-echoes` from any directory.

## Usage

The utility provides a simple command-line interface.

### 1. Schedule an Echo

To schedule a new chronal echo, provide a message and a future timestamp in ISO 8601 format.

```bash
chronal-echoes schedule "Remember to check the temporal anomaly detector." "2025-01-01T10:00:00Z"
```

-   `"<message>"`: The message you want to receive in the future.
-   `"<YYYY-MM-DDTHH:MM:SSZ>"`: The exact UTC timestamp when the echo should manifest. (e.g., `2025-01-01T10:00:00Z` for January 1st, 2025, 10:00:00 AM UTC).

### 2. Retrieve Manifested Echoes

To check for and retrieve any echoes that have reached their designated time:

```bash
chronal-echoes retrieve
```

This command will display all echoes whose timestamp is in the past or present. Once retrieved, these echoes are removed from storage, preventing them from manifesting again.

### 3. Clear All Echoes

To purge all scheduled chronal echoes from the timeline (use with caution!):

```bash
chronal-echoes clear
```

This will delete the `.chronal-echoes.json` file's contents, effectively removing all future and un-retrieved past echoes.

## Example Workflow

1.  **Schedule a few echoes:**
    ```bash
    chronal-echoes schedule "Don't forget the void-whisperer's prophecy." "2024-12-25T08:00:00Z"
    chronal-echoes schedule "Initiate phase 2 of temporal stabilization." "2024-07-15T14:30:00Z"
    chronal-echoes schedule "Check the integrity of the reality fabric." "2024-06-01T00:00:00Z"
    ```

2.  **Later, on June 1st, retrieve echoes:**
    ```bash
    chronal-echoes retrieve
    # Output might show: 
    # Chronal Echoes manifested:
    # - [2024-06-01T00:00:00Z] Check the integrity of the reality fabric. (ID: ...)
    ```

3.  **On July 15th, retrieve again:**
    ```bash
    chronal-echoes retrieve
    # Output might show: 
    # Chronal Echoes manifested:
    # - [2024-07-15T14:30:00Z] Initiate phase 2 of temporal stabilization. (ID: ...)
    ```

4.  **If you want to remove all future echoes:**
    ```bash
    chronal-echoes clear
    ```
