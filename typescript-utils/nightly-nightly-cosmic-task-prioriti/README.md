# nightly-cosmic-task-prioritizer

A whimsical CLI tool to prioritize your daily tasks with a touch of cosmic guidance. Ever feel overwhelmed by your to-do list? Let the ApocalypsAI Nightly Integrator assign your tasks a "Cosmic Urgency" and a "Focus Constellation," helping you navigate your workload with celestial clarity (and a bit of fun).

## Features

*   **Cosmic Urgency Levels**: Tasks are assigned one of four urgency levels: "Nebula Nudge" (low), "Stellar Sprint" (medium), "Galactic Grind" (high), or "Void Voyage" (critical).
*   **Focus Constellations**: Each task gets a suggested "Focus Constellation" (time block) like "Orion's Hour" or "Andromeda's Apex" to help you mentally allocate time.
*   **Suggested Durations**: Get a whimsical estimate of how long a task might take in minutes.
*   **Deterministic Prioritization**: While whimsical, the prioritization is deterministic based on task details, ensuring consistent results for the same input.
*   **JSON Input/Output**: Easily integrate with other tools by providing tasks as a JSON array and receiving prioritized tasks in JSON format.

## Installation

1.  **Ensure Node.js and npm are installed.**
2.  **Clone the repository (or navigate to the utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-cosmic-task-prioritizer
    ```
3.  **Install dependencies and build the project:**
    ```bash
    npm install
    npm run build
    ```
4.  **Optionally, link the CLI tool for global access:**
    ```bash
    npm link
    ```
    Now you can run `cosmic-prioritize` from any directory.

## Usage

The `cosmic-prioritize` command accepts a JSON file as input or reads from `stdin`.

### Input Format

The input should be a JSON array of task objects, each with at least an `id` and `description`. An optional `tags` array can also be included.

**`tasks.json` example:**
```json
[
  {
    "id": "project-alpha-design",
    "description": "Finalize the schematic for the interdimensional portal stabilizer.",
    "tags": ["design", "critical", "project-alpha"]
  },
  {
    "id": "daily-report",
    "description": "Compile the daily temporal distortion report for the council.",
    "tags": ["reporting", "routine"]
  },
  {
    "id": "void-garden-watering",
    "description": "Water the Void-blossoms in the communal garden.",
    "tags": ["maintenance", "whimsical"]
  }
]
```

### Examples

1.  **Prioritize tasks from a file and print to console:**
    ```bash
    cosmic-prioritize tasks.json
    ```

2.  **Prioritize tasks from a file and save to an output file:**
    ```bash
    cosmic-prioritize tasks.json --output prioritized_tasks.json
    ```

3.  **Prioritize tasks by piping JSON from stdin:**
    ```bash
    echo '[{"id": "task-x", "description": "Investigate the anomalous energy readings."}]' | cosmic-prioritize
    ```

4.  **Prioritize tasks by typing directly into stdin (if not piped):**
    ```bash
    cosmic-prioritize
    # Enter your JSON array here, then press Ctrl+D (or Ctrl+Z on Windows)
    # Example:
    # [{"id": "task-y", "description": "Decipher the ancient star charts."}]
    ```

### Output Format

The output will be a JSON array of prioritized task objects, each containing the original task, its assigned `urgency`, `constellation`, and `suggestedDurationMinutes`.

**Example Output:**
```json
[
  {
    "task": {
      "id": "project-alpha-design",
      "description": "Finalize the schematic for the interdimensional portal stabilizer.",
      "tags": [
        "design",
        "critical",
        "project-alpha"
      ]
    },
    "urgency": "Stellar Sprint",
    "constellation": "Andromeda's Apex",
    "suggestedDurationMinutes": 120
  },
  {
    "task": {
      "id": "daily-report",
      "description": "Compile the daily temporal distortion report for the council.",
      "tags": [
        "reporting",
        "routine"
      ]
    },
    "urgency": "Galactic Grind",
    "constellation": "Cygnus' Cycle",
    "suggestedDurationMinutes": 15
  },
  {
    "task": {
      "id": "void-garden-watering",
      "description": "Water the Void-blossoms in the communal garden.",
      "tags": [
        "maintenance",
        "whimsical"
      ]
    },
    "urgency": "Void Voyage",
    "constellation": "Orion's Hour",
    "suggestedDurationMinutes": 30
  }
]
```

## Development

To run tests:
```bash
npm test
```

## Contributing

Feel free to suggest new cosmic urgencies, constellations, or even entirely new celestial prioritization algorithms!
