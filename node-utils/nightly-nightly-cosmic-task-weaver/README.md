# Nightly Cosmic Task Weaver

A whimsical-yet-useful Node.js CLI tool that helps you choose your next task from a list, guided by cosmic whims and configurable probabilities. Break free from decision paralysis and let the universe guide your productivity!

## ✨ Features

*   **Cosmic Guidance**: Get a randomly selected task from your list, imbued with celestial wisdom.
*   **Weighted Probabilities**: Assign "cosmic weight" to tasks to influence their likelihood of being chosen.
*   **Stellar Alignments**: Optionally receive a "cosmic alignment" message to set the mood for your work.
*   **Multiple Selections**: Ask the cosmos for multiple tasks at once.
*   **Flexible Input**: Provide tasks directly via CLI arguments or from a JSON file.

## 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-cosmic-task-weaver
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Make it executable (optional, but recommended for global use):**
    ```bash
    # From the utility's root directory:
    npm link
    # Now you can run 'cosmic-weaver' from anywhere
    ```
    Alternatively, you can always run it with `node src/index.js`.

## 🌌 Usage

### Basic Usage

Provide tasks as arguments. Tasks with spaces should be quoted.

```bash
cosmic-weaver "Write code" "Review PRs" "Meditate on the void"
```

Output:
```
Listening to the whispers of the void...

The cosmic dice have rolled, revealing your path:
  1. Write code

May your path be illuminated by starlight!
```

### With Weights

Assign a weight to a task using `task_name:weight`. Higher weights mean higher probability. Default weight is 1.

```bash
cosmic-weaver "Urgent Bug Fix:5" "Refactor Old Code:2" "Explore New Tech:1"
```

### From a JSON File

Create a `tasks.json` file:

```json
[
  "Clean up the temporal rifts",
  { "name": "Optimize the quantum flux capacitor", "weight": 3 },
  { "name": "Document the void-whisperer API", "weight": 2 },
  "Contemplate the infinite possibilities"
]
```

Then run:

```bash
cosmic-weaver -f tasks.json
# or
cosmic-weaver --file tasks.json
```

### Get a Cosmic Alignment

Add the `-a` or `--alignment` flag to receive a guiding cosmic message.

```bash
cosmic-weaver -a "Develop new feature" "Fix critical bug"
```

Output:
```
Peering into the stellar tapestry...

The stars whisper: 'Focus on creative endeavors.'

The cosmic dice have rolled, revealing your path:
  1. Develop new feature

Embrace the cosmic flow!
```

### Multiple Tasks

Use the `-c` or `--count` flag to get multiple task suggestions. The utility will try to provide unique tasks.

```bash
cosmic-weaver -c 2 "Task Alpha" "Task Beta" "Task Gamma" "Task Delta"
```

Output:
```
Drawing from the well of cosmic possibility...

The cosmic dice have rolled, revealing your path:
  1. Task Beta
  2. Task Delta

Your destiny awaits among the stars!
```

## 🛠️ Development

### Running Tests

```bash
npm test
```

This will execute the unit tests for the core task selection logic.

## 📜 License

This project is licensed under the MIT License.
