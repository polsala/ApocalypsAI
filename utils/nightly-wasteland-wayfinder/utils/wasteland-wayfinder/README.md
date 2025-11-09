# Wasteland Wayfinder

## Navigate the Desolate Future with Purpose!

The `Wasteland Wayfinder` is a command-line utility designed to help you prioritize your daily tasks in a world where every decision counts. Whether you're scavenging for supplies, fortifying your shelter, or just trying to remember to hydrate, this tool brings a post-apocalyptic flair to your task management.

Assign 'urgency' and 'resource cost' to your tasks, and let the Wayfinder guide your path to survival.

## Features

*   **Add Tasks**: Log new survival objectives with descriptions, urgency levels, and associated resource needs.
*   **List Tasks**: View your current objectives, sorted by priority.
*   **Complete Tasks**: Mark tasks as done when you've successfully navigated a challenge.
*   **Prioritize**: Automatically sorts tasks based on their critical importance to your survival.

## Installation

Simply copy the `wasteland-wayfinder` folder into your `utils/` directory. No complex dependencies, just pure survival logic.

## Usage

Run the `wayfinder.py` script directly from its `src/` directory.

```bash
# Add a critical task requiring specific resources
python3 src/wayfinder.py add "Secure perimeter fence" --urgency critical --resources ScrapMetal Tools

# Add a high urgency task
python3 src/wayfinder.py add "Scavenge for canned goods" --urgency high --resources Food Water

# Add a medium urgency task with default resources
python3 src/wayfinder.py add "Organize medical supplies" --urgency medium

# List all active tasks, sorted by urgency
python3 src/wayfinder.py list

# Mark a task as completed (use the ID from the list command)
python3 src/wayfinder.py complete 1

# List all tasks, including completed ones
python3 src/wayfinder.py list --completed
```

### Commands:

*   `add <description>`: Adds a new task.
    *   `--urgency <level>`: `critical`, `high`, `medium`, `low` (default: `medium`)
    *   `--resources <resource1> <resource2> ...`: Space-separated list of resources (e.g., `Food Water Ammo`)
*   `list`: Lists all active tasks, sorted by priority.
    *   `--completed`: Include completed tasks in the list.
*   `complete <task_id>`: Marks a task as completed. Use the ID from the `list` command.
*   `help`: Displays usage information.
