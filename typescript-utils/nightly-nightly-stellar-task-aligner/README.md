# Nightly Stellar Task Aligner

## Overview
In the chaotic aftermath, every decision counts. The `nightly-stellar-task-aligner` is a whimsical-yet-useful TypeScript CLI tool designed to help you prioritize your post-apocalyptic tasks by aligning them with various "cosmic energies." Define your tasks with urgency, effort, and reward, choose a cosmic alignment (e.g., Aggressive, Balanced, Relaxed, Strategic), and let the stars guide your next move.

## Features
*   **Task Definition**: Clearly define tasks with numerical ratings for urgency, effort, and reward.
*   **Cosmic Alignments**: Choose from predefined alignment strategies to influence prioritization.
*   **Prioritization Score**: Tasks are scored and sorted based on the chosen alignment's weights.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.

## Installation
1.  **Navigate to the utility directory**:
    ```bash
    cd typescript-utils/nightly-stellar-task-aligner
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    # or yarn install
    ```

## Usage
Run the `align` command with your tasks as a JSON string and an optional alignment type.

```bash
# Example: Align tasks with a 'Balanced' cosmic alignment
npm start -- -a Balanced -t '[{"name":"Scavenge for water","urgency":5,"effort":3,"reward":4,"cosmicInfluence":"Moon"},{"name":"Repair solar panel","urgency":4,"effort":5,"reward":5,"cosmicInfluence":"Sun"},{"name":"Barter with nomads","urgency":3,"effort":2,"reward":3,"cosmicInfluence":"Jupiter"}]'

# Example: Align tasks with an 'Aggressive' cosmic alignment (default is 'Balanced')
npm start -- -a Aggressive -t '[{"name":"Secure perimeter","urgency":5,"effort":4,"reward":3},{"name":"Gather rations","urgency":4,"effort":2,"reward":4}]'

# Example: Align tasks with a 'Relaxed' cosmic alignment
npm start -- -a Relaxed -t '[{"name":"Read ancient texts","urgency":1,"effort":1,"reward":5},{"name":"Polish rusty tools","urgency":2,"effort":2,"reward":2}]'
```

### Arguments:
*   `-a, --alignment <type>`: (Optional) The cosmic alignment strategy to use. Choose from `Aggressive`, `Balanced`, `Relaxed`, `Strategic`. Defaults to `Balanced`.
*   `-t, --tasks <json>`: (Required) A JSON string representing an array of tasks. Each task object must have `name` (string), `urgency` (number 1-5), `effort` (number 1-5), and `reward` (number 1-5). An optional `cosmicInfluence` (string) can be added for flavor.

### Task Properties:
*   `name`: A brief description of the task (string).
*   `urgency`: How critical the task is (1 = low, 5 = high).
*   `effort`: How much effort the task requires (1 = low, 5 = high).
*   `reward`: How beneficial or rewarding the task is (1 = low, 5 = high).
*   `cosmicInfluence`: (Optional) A whimsical cosmic body associated with the task (e.g., "Mars", "Venus", "Moon").

## Development
### Build
```bash
npm run build
```

### Test
```bash
npm test
```
