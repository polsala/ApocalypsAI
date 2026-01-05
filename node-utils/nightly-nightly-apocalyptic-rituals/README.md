# Nightly Apocalyptic Rituals Tracker

In the desolate expanse of the post-apocalyptic world, maintaining a semblance of order and sanity is paramount. The `nightly-apocalyptic-rituals` utility helps survivors (and developers) keep track of their essential daily 'rituals' or tasks, ensuring that no crucial survival chore is forgotten.

Whether it's 'Scavenge for rations', 'Check perimeter defenses', or 'Debug the ancient server', this CLI tool provides a simple way to manage your daily regimen.

## Features

-   **Add Rituals**: Easily add new daily tasks to your survival checklist.
-   **List Status**: See which rituals are pending and which are completed for the current day.
-   **Mark Complete**: Mark a ritual as done with a simple command.
-   **Daily Reset**: Rituals automatically reset to pending at the start of a new day, ready for another cycle of survival.

## Installation

1.  Navigate to the `nightly-apocalyptic-rituals` directory.
2.  Install dependencies (for running tests):
    ```bash
    npm install
    ```

## Usage

All commands are run via `node src/ritual-tracker.js <command> [arguments]`.

### Add a new ritual

```bash
node src/ritual-tracker.js add "Scavenge for rations"
node src/ritual-tracker.js add "Fortify shelter entrance"
```

### List all rituals and their status

```bash
node src/ritual-tracker.js list
```

Example output:
```
--- Apocalyptic Rituals ---
- [⏳ PENDING] Scavenge for rations
- [✅ COMPLETED] Fortify shelter entrance
---------------------------
```

### Mark a ritual as completed for today

You can use either the full ritual name (case-insensitive) or its unique ID.

```bash
node src/ritual-tracker.js complete "Scavenge for rations"
# Or by ID (you can see IDs in the rituals.json file if needed, though name is usually easier)
node src/ritual-tracker.js complete "1678901234567" 
```

### Reset all rituals to pending

This command explicitly clears the completion status for all rituals. Rituals also implicitly reset to pending at the start of a new day.

```bash
node src/ritual-tracker.js reset
```

## Data Storage

Rituals are stored in a `rituals.json` file within the utility's root directory. This file is automatically created and managed by the script.

## Development & Testing

To run the automated tests:

```bash
npm test
```

Tests are self-contained and use `sinon` for mocking file system operations and date/time to ensure determinism and offline execution.
