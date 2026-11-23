# Nightly Doom List Prioritizer

A Node.js CLI utility to bring order (and a touch of chaos) to your most pressing apocalyptic tasks. This tool helps you prioritize your to-do list items by considering their urgency, potential impact, and a randomly generated 'Chaos Rating' and 'Doom Descriptor'.

## Features

*   **Customizable Priority & Impact**: Assign `critical`, `urgent`, `normal`, or `low` priority, and `high`, `medium`, or `low` impact to your tasks.
*   **Whimsical Chaos Factors**: Each task is imbued with a random 'Chaos Rating' (1-10) and a 'Doom Descriptor' (e.g., 'Imminent', 'Lingering') to reflect the unpredictable nature of the end times.
*   **Intelligent Prioritization**: Tasks are sorted based on a weighted score combining your defined priority, impact, and the generated chaos factor.
*   **Color-Coded Output**: Easily distinguish task priorities with ANSI color coding in your terminal.

## Installation

1.  **Navigate to the utility directory**:
    ```bash
    cd node-utils/nightly-doom-list-prioritizer
    ```
2.  **Install dependencies (if any, though this utility is dependency-free)**:
    ```bash
    npm install
    ```
3.  **Make the utility executable (optional, for global access)**:
    ```bash
    npm link
    # Or, to run directly:
    # node src/index.js
    ```

## Usage

Run the `doom-list` command (if linked) or `node src/index.js` followed by your tasks as quoted strings. You can specify `priority` and `impact` using `--priority` and `--impact` flags within each task string.

```bash
# Basic usage with default priority/impact
doom-list "Repair the temporal displacement unit" "Scavenge for spare parts"

# Specifying priority and impact for tasks
doom-list \
  "Secure the last known supply of artisanal sourdough --priority critical --impact high" \
  "Recalibrate the weather manipulation device --priority urgent --impact medium" \
  "Organize the sock drawer --priority low --impact low"

# Mixing tasks with and without explicit settings
doom-list \
  "Fortify the perimeter --priority critical" \
  "Brew more coffee" \
  "Investigate the strange humming sound --impact high"
```

### Priority Levels

*   `critical`
*   `urgent`
*   `normal` (default)
*   `low`

### Impact Levels

*   `high`
*   `medium` (default)
*   `low`

## How it Works

Each task is assigned a score based on the following formula:

`Score = (Priority_Value * 100) + (Impact_Value * 50) + Chaos_Rating`

*   **Priority Values**: `critical` (3), `urgent` (2), `normal` (1), `low` (0)
*   **Impact Values**: `high` (3), `medium` (2), `low` (1)
*   **Chaos Rating**: A random integer between 1 and 10.

The tasks are then sorted in descending order of their calculated score, presenting the most critical and chaotic tasks first.

## Example Output

```
--- Apocalyptic Doom List Prioritization ---
1. 💥 [31m[CRITICAL][0m (HIGH Impact, Chaos: 8/10, Cataclysmic): Secure the last known supply of artisanal sourdough
2. ⚡ [33m[URGENT][0m (MEDIUM Impact, Chaos: 5/10, Pressing): Recalibrate the weather manipulation device
3. ⏳ [32m[NORMAL][0m (MEDIUM Impact, Chaos: 3/10, Mildly Concerning): Brew more coffee
4. 🛸 [34m[LOW][0m (LOW Impact, Chaos: 1/10, Hypothetical): Organize the sock drawer
------------------------------------------
```
