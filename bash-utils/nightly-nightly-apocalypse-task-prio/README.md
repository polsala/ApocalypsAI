# Nightly Apocalypse Task Prioritizer

A whimsical-yet-useful bash utility for managing your critical, scavenging, morale-boosting, and temporal anomaly investigation tasks in the post-apocalyptic world. Keep your objectives clear and your priorities straight, even when the world isn't.

## Features

*   **Categorized Tasks**: Organize tasks into `CRITICAL`, `SCAVENGE`, `MORALE`, `TEMPORAL`, and `MISC` categories.
*   **Prioritization**: Assign a priority level from 1 (highest) to 5 (lowest).
*   **Status Tracking**: Mark tasks as pending `[ ]` or completed `[X]`.
*   **Wasteland Wisdom**: Get a random, inspiring (or darkly humorous) tip with every task listing.
*   **Simple CLI Interface**: Easy to use from your terminal.

## Installation

1.  **Clone the repository** (or just copy the `src/apocalypse_tasks.sh` file).
2.  **Make the script executable**:
    ```bash
    chmod +x src/apocalypse_tasks.sh
    ```
3.  **Optional: Add to your PATH**: For easier access, move or symlink the script to a directory in your `PATH` (e.g., `/usr/local/bin` or `~/bin`).
    ```bash
    # Example:
    sudo mv src/apocalypse_tasks.sh /usr/local/bin/apocalypse-tasks
    # Or for local user:
    mkdir -p ~/bin
    mv src/apocalypse_tasks.sh ~/bin/apocalypse-tasks
    export PATH="$HOME/bin:$PATH" # Add to your .bashrc or .zshrc
    ```

## Usage

The utility stores tasks in a file named `.apocalypse_tasks` in your home directory by default. You can override this by setting the `APOCALYPSE_TASK_FILE` environment variable.

```bash
apocalypse-tasks <command> [arguments]
```

### Commands:

*   **`add <CATEGORY> <PRIORITY> <DESCRIPTION>`**: Add a new task to your log.
    *   `<CATEGORY>`: One of `CRITICAL`, `SCAVENGE`, `MORALE`, `TEMPORAL`, `MISC`. (Case-insensitive)
    *   `<PRIORITY>`: A number from `1` (highest urgency) to `5` (lowest urgency).
    *   `<DESCRIPTION>`: A brief description of the task (enclose in quotes if it contains spaces).

    _Example:_
    ```bash
    apocalypse-tasks add CRITICAL 1 "Repair the main water filtration unit"
    apocalypse-tasks add SCAVENGE 3 "Search abandoned library for pre-fall tech manuals"
    apocalypse-tasks add MORALE 2 "Organize a post-apocalyptic poetry slam"
    ```

*   **`list [CATEGORY]`**: Display all current tasks, sorted by priority and then category. Optionally filter by a specific category.

    _Example:_
    ```bash
    apocalypse-tasks list
    apocalypse-tasks list CRITICAL
    apocalypse-tasks list morale
    ```

*   **`complete <TASK_ID>`**: Mark a task as completed using its unique ID.

    _Example:_
    ```bash
    apocalypse-tasks complete 1
    ```

*   **`clear`**: Remove all tasks that have been marked as completed `[X]` from the log.

    _Example:_
    ```bash
    apocalypse-tasks clear
    ```

## Task File Format

Tasks are stored in a simple text file, one task per line, with the following format:

```
ID | Status | Category | Priority | Task Description
```

Example entries:
```
1 | [ ] | CRITICAL | 1 | Secure the last can of irradiated peaches
2 | [X] | SCAVENGE | 3 | Scavenge for spare parts in Sector 7
```

## Development & Testing

To run the automated tests, navigate to the `tests/` directory and execute `test_apocalypse_tasks.sh`:

```bash
cd tests/
./test_apocalypse_tasks.sh
```

The tests use a temporary file for task storage, ensuring they are deterministic and do not interfere with your actual task list.
