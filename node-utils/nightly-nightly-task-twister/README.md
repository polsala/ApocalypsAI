# Nightly Task Twister

## ✨ Your Daily Dose of Coding Destiny ✨

The `nightly-task-twister` is a whimsical Node.js CLI utility designed to inject a bit of fun and serendipity into your coding routine. Feeling stuck? Can't decide what small task to tackle next? Let the Task Twister reveal your coding destiny for the moment!

It randomly selects a small, productive coding task from a predefined list (or your own custom list), helping you overcome decision paralysis and encouraging exploration of your codebase.

## Installation

To use the Task Twister, you need Node.js installed on your system.

1.  **Navigate to the utility's directory:**
    ```bash
    cd node-utils/nightly-task-twister
    ```
2.  **Install dependencies and link the CLI tool:**
    ```bash
    npm install
    npm link # This makes 'task-twister' command globally available
    ```
    Alternatively, you can run it directly without global installation using `npx`:
    ```bash
    npx node src/index.js
    ```

## Usage

Simply run the `task-twister` command in your terminal:

```bash
task-twister
```

The utility will output a randomly chosen task, along with some encouraging words.

### Using a Custom Task File

YouYou can provide your own list of tasks using the `--file` option. The custom file should be a JSON array of strings, where each string is a task.

1.  **Create your custom tasks file** (e.g., `my-tasks.json`):
    ```json
    [
      "Refactor the 'calculateTotal' function for better readability.",
      "Add JSDoc comments to all functions in 'utils.js'.",
      "Explore the new feature branch and provide feedback."
    ]
    ```
2.  **Run the Task Twister with your custom file:**
    ```bash
    task-twister --file ./my-tasks.json
    ```
    The path to your custom file can be absolute or relative to where you run the command.

## Development & Testing

To run the tests for this utility:

```bash
cd node-utils/nightly-task-twister
npm test
```

This will execute the tests using Node.js's built-in test runner.
