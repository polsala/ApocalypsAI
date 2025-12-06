# Chronos-Chime Task Prioritizer

A whimsical-yet-useful utility for the discerning survivor, the Chronos-Chime Task Prioritizer helps you organize your pre- or post-apocalyptic to-do list. Input your tasks, their estimated durations, and any dependencies, and let the Chronos-Chime generate a prioritized schedule, complete with "Impending Doom!" warnings for your most critical objectives.

## Features

*   **Dependency Management**: Ensures tasks are scheduled in the correct order.
*   **Critical Path Identification**: Highlights tasks marked as critical, warning you of "Impending Doom!" if they're not prioritized.
*   **Total Time Estimation**: Provides an overall duration for your entire task list.
*   **Clear Output**: Presents a human-readable schedule in your terminal.
*   **Circular Dependency Detection**: Prevents endless loops in your planning.

## Installation

This utility is self-contained and requires Python 3.8+ (tested with 3.11). No external `pip` dependencies are needed beyond the standard library.

1.  Navigate to the `utils/chronos-chime-task-prioritizer/` directory.
2.  Ensure you have Python installed.

## Usage

The utility expects a JSON file containing your tasks.

### Task File Format (`tasks.json` example)

Create a JSON file (e.g., `my_survival_plan.json`) with an array of task objects. Each task object should have:

*   `name` (string, required): A unique name for the task.
*   `duration` (integer, required): The estimated time to complete the task in minutes.
*   `dependencies` (array of strings, optional): A list of task names that must be completed before this task can start.
*   `critical` (boolean, optional): Set to `true` if this task is vital for survival and should be highlighted with an "Impending Doom!" warning. Defaults to `false`.

```json
[
  {
    "name": "Secure perimeter",
    "duration": 120,
    "dependencies": [],
    "critical": true
  },
  {
    "name": "Scavenge for supplies",
    "duration": 180,
    "dependencies": ["Secure perimeter"]
  },
  {
    "name": "Repair comms array",
    "duration": 240,
    "dependencies": ["Secure perimeter"],
    "critical": true
  },
  {
    "name": "Cook mutated squirrel stew",
    "duration": 60,
    "dependencies": ["Scavenge for supplies"]
  },
  {
    "name": "Broadcast distress signal",
    "duration": 30,
    "dependencies": ["Repair comms array"],
    "critical": true
  },
  {
    "name": "Sharpen rusty spork",
    "duration": 15
  }
]
```

### Running the Prioritizer

Execute the `prioritizer.py` script from the command line, providing the path to your task JSON file:

```bash
python src/prioritizer.py my_survival_plan.json
```

### Example Output

```
Chronos-Chime Task Prioritizer Report

Total estimated time: 15 hours 45 minutes

--- Schedule ---
1. Secure perimeter (2 hours) [CRITICAL PATH: Impending Doom!]
2. Repair comms array (4 hours) [CRITICAL PATH: Impending Doom!]
3. Sharpen rusty spork (15 minutes)
4. Scavenge for supplies (3 hours)
5. Broadcast distress signal (30 minutes) [CRITICAL PATH: Impending Doom!]
6. Cook mutated squirrel stew (1 hour)

--- Warnings ---
- Critical tasks identified: Secure perimeter, Repair comms array, Broadcast distress signal
- Prioritize these tasks for survival!
```

## Development & Testing

To run the tests, navigate to the `utils/chronos-chime-task-prioritizer/` directory and execute:

```bash
python -m unittest tests/test_prioritizer.py
```

All tests are deterministic and offline, using mocks for file I/O and standard output capture.
