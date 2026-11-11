# Nightly Ephemeral Task Log

A whimsical-yet-useful CLI utility to quickly log and manage ephemeral, short-lived tasks that fade away like whispers in the digital wasteland. Perfect for those fleeting thoughts, temporary reminders, or tasks that don't deserve a permanent place in your grand project management system.

## Features

*   **Quick Add**: Jot down a task with a simple command.
*   **List Whispers**: See all your current ephemeral tasks.
*   **Forget Task**: Mark a task as completed or no longer relevant, making it vanish into the digital ether.
*   **Self-contained**: Stores tasks in a local JSON file.

## Installation

1.  Navigate to the `nightly-ephemeral-task-log` directory.
2.  Install dependencies (currently none beyond Node.js built-ins):
    ```bash
    npm install
    ```
3.  (Optional) To make it globally accessible, you can link it:
    ```bash
    npm link
    ```
    Or simply run it using `node src/index.js <command>`.

## Usage

All commands start with `node src/index.js` or `nightly-ephemeral-task-log` if linked.

### Add a new ephemeral task

```bash
node src/index.js add "Remember to check the temporal anomaly detector before dawn."
```

### List all current ephemeral tasks

```bash
node src/index.js list
```

Example output:
```
Ephemeral Tasks:
- [ID: abc12] Remember to check the temporal anomaly detector before dawn.
- [ID: def34] Scavenge for spare parts in Sector 7.
```

### Forget a task (mark as done/remove)

You'll need the task ID, which is shown when listing tasks.

```bash
node src/index.js forget abc12
```

## Development

To run tests:

```bash
npm test
```
