# Nightly Temporal Task Echo

A whimsical-yet-useful utility for managing tasks that recur based on their last completion date, rather than fixed calendar dates. Perfect for post-apocalyptic scheduling where "every Tuesday" might be less useful than "3 days after I last scavenged Sector 7."

## Features

*   **Event-Driven Recurrence**: Define tasks that become due a set number of days *after* they were last completed.
*   **Simple CLI**: Add, complete, list, and view upcoming tasks.
*   **Persistent Storage**: Tasks are saved to a local JSON file (`temporal_tasks.json`) in the directory where the command is executed.
*   **Type-Safe**: Built with TypeScript for robust data handling.

## Installation

1.  **Navigate to the utility directory**:
    ```bash
    cd typescript-utils/nightly-temporal-task-echo
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```
    or
    ```bash
    yarn install
    ```

## Usage

The utility operates via a command-line interface. All tasks are stored in `temporal_tasks.json` in the directory from which you run the commands.

### Commands

*   **`add <name> <recurrence_days> [description]`**: Adds a new temporal task.
    *   `<name>`: A short, descriptive name for the task (e.g., "Check Water Purifier").
    *   `<recurrence_days>`: The number of days after completion the task should next be due (e.g., `7` for weekly).
    *   `[description]` (optional): A longer description for the task.

    ```bash
    npm start add "Scavenge Sector 7" 3 "Look for canned goods and spare parts"
    npm start add "Check Perimeter Fence" 7
    ```

*   **`complete <task_id>`**: Marks a task as completed, updating its `lastCompletedAt` and recalculating its `nextDueAt`.
    *   `<task_id>`: The unique ID of the task (obtained from `list` command).

    ```bash
    npm start complete 1701234567890
    ```

*   **`list`**: Displays all registered temporal tasks, their status, and next due dates.

    ```bash
    npm start list
    ```

*   **`upcoming [days_ahead]`**: Shows tasks that are due within the next specified number of days (default: 7 days).
    *   `[days_ahead]` (optional): The number of days into the future to check.

    ```bash
    npm start upcoming
    npm start upcoming 14
    ```

## Example Workflow

1.  **Add a task**:
    ```bash
    npm start add "Forage for Berries" 2 "Check the old growth forest path"
    # Output: Added task "Forage for Berries" (ID: <some_id>) recurring every 2 days.
    ```
2.  **List tasks**:
    ```bash
    npm start list
    # Output (example, dates will vary):
    # --- All Temporal Tasks ---
    # ID: <some_id>
    #   Name: Forage for Berries
    #   Description: Check the old growth forest path
    #   Recurrence: Every 2 days
    #   Last Completed: Never
    #   Next Due: N/A
    # ---
    ```
3.  **Complete the task**:
    ```bash
    npm start complete <some_id>
    # Output (example, dates will vary): Completed task "Forage for Berries". Next due: 10/25/2077 (assuming today is 10/23/2077)
    ```
4.  **Check upcoming tasks**:
    ```bash
    npm start upcoming 3
    # Output (example, dates will vary):
    # --- Upcoming Temporal Tasks (next 3 days) ---
    # ID: <some_id>
    #   Name: Forage for Berries
    #   Next Due: 10/25/2077
    # ---
    ```

## Development

### Running Tests

```bash
npm test
```

### Building

```bash
npm run build
```
