# Nightly Temporal Task Triage

A whimsical CLI tool to prioritize tasks based on their temporal resonance and urgency. Helps you sort through the echoes of the past, whispers of the present, and rumbles of the imminent future.

## Features

*   **Temporal Resonance Categorization**: Assign tasks to categories like 'Rumbles of the Imminent', 'Whispers of Now', 'Echoes of Yesteryear', 'Shadows of Tomorrow', and 'Flickers of the Distant'.
*   **Priority Levels**: Supports standard priority levels: 'critical', 'high', 'medium', 'low', 'none'.
*   **Intelligent Sorting**: Combines temporal resonance and priority to provide a weighted, actionable task list.
*   **Cross-Platform**: Built with Node.js, runs anywhere Node.js is supported.

## Installation

1.  Ensure you have Node.js (v14 or higher) installed.
2.  Clone the ApocalypsAI repository or navigate to this utility's directory:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-temporal-task-triage
    ```
3.  No external dependencies, so no `npm install` is strictly required for this utility.

## Usage

Create a JSON file (e.g., `tasks.json`) containing your tasks. Each task should have `id`, `description`, `resonance`, and `priority` fields.

**`tasks.json` example:**

```json
[
  {
    "id": "task-1",
    "description": "Repair the Chrono-Stabilizer",
    "resonance": "Rumbles of the Imminent",
    "priority": "critical"
  },
  {
    "id": "task-2",
    "description": "Archive ancient data logs",
    "resonance": "Echoes of Yesteryear",
    "priority": "low"
  },
  {
    "id": "task-3",
    "description": "Prepare for next temporal shift",
    "resonance": "Shadows of Tomorrow",
    "priority": "medium"
  },
  {
    "id": "task-4",
    "description": "Respond to current void whispers",
    "resonance": "Whispers of Now",
    "priority": "high"
  },
  {
    "id": "task-5",
    "description": "Plan for interstellar colonization",
    "resonance": "Flickers of the Distant",
    "priority": "none"
  },
  {
    "id": "task-6",
    "description": "Calibrate temporal sensors",
    "resonance": "Rumbles of the Imminent",
    "priority": "high"
  }
]
```

Run the utility from your terminal, providing the path to your task file:

```bash
node src/index.js tasks.json
```

**Expected Output:**

```
--- Temporal Task Triage Report ---

1. [55] Repair the Chrono-Stabilizer (Rumbles of the Imminent, critical)
2. [54] Calibrate temporal sensors (Rumbles of the Imminent, high)
3. [44] Respond to current void whispers (Whispers of Now, high)
4. [33] Prepare for next temporal shift (Shadows of Tomorrow, medium)
5. [22] Archive ancient data logs (Echoes of Yesteryear, low)
6. [11] Plan for interstellar colonization (Flickers of the Distant, none)

-----------------------------------
```

### Invalid Input Handling

*   If the file is not found, an error message will be displayed.
*   If the JSON is malformed, a parsing error will be reported.
*   Tasks with missing or invalid `resonance` or `priority` will be skipped with a warning.

## Development & Testing

To run the automated tests:

```bash
node tests/index.test.js
```
