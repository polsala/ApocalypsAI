# Nightly Cosmic Task Aligner

A whimsical TypeScript CLI tool that helps you overcome decision paralysis by suggesting a "cosmically aligned" task from a predefined list. Let the universe guide your next step!

## ✨ Features

*   **Whimsical Guidance**: Receive a daily task suggestion with a unique "cosmic alignment" message.
*   **Deterministic Alignment**: Tasks are chosen based on a seed (defaulting to current time), ensuring consistent results for the same input.
*   **Extensible Task List**: Easily add or modify the list of cosmic tasks.
*   **Simple CLI**: Easy to use from your terminal.

## 🚀 Installation

1.  **Clone the repository (or navigate to the utility's directory):**
    ```bash
    git clone https://https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-cosmic-task-aligner
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Build the TypeScript project:**
    ```bash
    npm run build
    ```

## 🌌 Usage

Run the `cosmic-align` command from your terminal.

### Basic Usage (uses current date/time as seed)

```bash
npm start
# Or, if you've linked the binary (npm link or global install):
# cosmic-align
```

Example Output:
```
✨ Your Cosmic Alignment for today ✨
------------------------------------
Task: Tidy up your immediate workspace.
Guidance: The cosmic dust settles. Bring order to your realm.
Tags: action, productivity
------------------------------------

May your path be clear and your energy aligned!
```

### Using a Custom Seed

You can provide a custom seed to influence the task alignment. This is useful if you want a specific "vibe" for your task or want to get the same task consistently for a given seed.

```bash
npm start -- --seed "feeling energetic"
# Or:
# cosmic-align -s "monday morning vibes"
```

### Getting Help

```bash
npm start -- --help
# Or:
# cosmic-align -h
```

## 🛠️ Development

### Project Structure

```
.
├── README.md
├── package.json
├── tsconfig.json
├── jest.config.js
├── src/
│   ├── index.ts      # Core logic for task alignment
│   ├── cli.ts        # Command-line interface
│   ├── tasks.ts      # Defines the list of cosmic tasks
│   └── types.ts      # TypeScript type definitions
└── tests/
    └── index.test.ts # Unit tests for the core logic
```

### Running Tests

```bash
npm test
```

## 📝 Customizing Tasks

You can modify the `src/tasks.ts` file to add, remove, or change the `CosmicTask` entries. Each task has:

*   `id`: A unique identifier (string).
*   `description`: The main description of the task.
*   `alignmentMessage`: A whimsical message related to the task.
*   `tags`: An array of strings for categorization.

After modifying `src/tasks.ts`, remember to rebuild the project: `npm run build`.

## License

This project is licensed under the MIT License.
