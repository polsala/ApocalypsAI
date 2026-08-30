# Nightly Temporal Task Triage

Prioritizes tasks based on urgency and a 'temporal decay' factor, ensuring critical actions are taken before they become obsolete in the ever-shifting timelines of the apocalypse.

## Overview

In the chaotic aftermath, some tasks are critical now but quickly lose relevance, while others can wait but remain important. The Nightly Temporal Task Triage helps you sort your apocalyptic to-do list by assigning a "triage score" based on a task's inherent urgency and its temporal decay rate.

## Features

*   **Urgency-based Scoring**: Assigns a base score based on a task's perceived importance (1-10).
*   **Temporal Decay Factor**: Modifies the urgency based on how quickly a task's relevance diminishes.
    *   `fast`: Task loses relevance quickly, prioritize now (multiplier: 1.5).
    *   `medium`: Standard decay, moderate priority (multiplier: 1.0).
    *   `slow`: Task remains relevant for longer, can be deferred (multiplier: 0.5).
*   **CLI Interface**: Easily process task lists from JSON files.

## Installation

1.  Navigate to the `nightly-temporal-task-triage` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

Create a JSON file (e.g., `tasks.json`) with your tasks. Each task should be an object with at least a `description` and optionally `urgency` (1-10, default 5) and `decay_rate` ('fast', 'medium', 'slow', default 'medium').

Example `tasks.json`:
```json
[
  { "id": 1, "description": "Repair temporal displacement unit", "urgency": 9, "decay_rate": "fast" },
  { "id": 2, "description": "Gather glowing mushrooms for dinner", "urgency": 3, "decay_rate": "medium" },
  { "id": 3, "description": "Archive ancient prophecies", "urgency": 7, "decay_rate": "slow" },
  { "id": 4, "description": "Calibrate Chrono-Compass", "urgency": 8, "decay_rate": "fast" },
  { "id": 5, "description": "Polish time-traveling boots", "urgency": 1, "decay_rate": "slow" },
  { "id": 6, "description": "Scavenge for spare parts (no urgency/decay specified)" }
]
```

Run the utility:
```bash
node src/index.js -f tasks.json
# Or, if installed globally (after `npm link` in the utility's root directory):
# temporal-triage -f tasks.json
```

The output will be a sorted list of tasks, highest priority first:

```
--- Triage Report ---

1. Repair temporal displacement unit (Urgency: 9, Decay: fast, Score: 13.5)
2. Calibrate Chrono-Compass (Urgency: 8, Decay: fast, Score: 12.0)
3. Scavenge for spare parts (Urgency: 5, Decay: medium, Score: 5.0)
4. Archive ancient prophecies (Urgency: 7, Decay: slow, Score: 3.5)
5. Gather glowing mushrooms for dinner (Urgency: 3, Decay: medium, Score: 3.0)
6. Polish time-traveling boots (Urgency: 1, Decay: slow, Score: 0.5)
```

## Development

### Running Tests

```bash
npm test
```

## License

MIT
