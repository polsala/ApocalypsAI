# Nightly Digital Garden Guard

## Summary

The `nightly-digital-garden-guard` is a whimsical Node.js utility designed to monitor a specified directory (your "digital garden") for changes in its files. Each run generates a "Garden Report" detailing new files ("sprouts"), modified files ("blooms"), and deleted files ("wilts"), providing a charming overview of your digital landscape's evolution.

It's perfect for tracking changes in personal knowledge bases, project directories, or any folder where you want a playful summary of activity.

## How it Works

1.  **Initialization**: The first time you run the guard on a directory, it scans all files and records their `mtimeMs` (last modified timestamp) and `size` into a hidden `.garden_state.json` file within that directory.
2.  **Subsequent Runs**: On subsequent runs, it compares the current state of the files with the previously saved state.
3.  **Change Detection**: It identifies:
    *   **Sprouts**: New files that weren't present in the previous state.
    *   **Blooms**: Existing files whose `mtimeMs` or `size` has changed.
    *   **Wilts**: Files that were present in the previous state but are now missing.
4.  **Report Generation**: A whimsical report is printed to the console, summarizing these changes.
5.  **State Update**: The current state is saved, overwriting the old `.garden_state.json`, preparing for the next run.

## Usage

### Prerequisites

*   Node.js (v14 or higher) installed.

### Installation

1.  Navigate to the `node-utils/nightly-digital-garden-guard` directory.
2.  Install dependencies (if any, currently none for core functionality):
    ```bash
    npm install
    ```

### Running the Guard

Execute the script with the path to your digital garden directory as an argument:

```bash
node src/index.js /path/to/your/digital/garden
```

Replace `/path/to/your/digital/garden` with the actual path to the directory you wish to monitor.

### Example Output

```
🌿 The Digital Garden Report for 2023-10-27 🌸

--- A New Day in the Garden ---

🌱 New Sprouts (Freshly Planted):
  - notes/new_idea.md
  - images/sunrise.png

🌼 Blooming Beauties (Flourishing & Changed):
  - project/main.js
  - docs/roadmap.txt

🍂 Wilted Wonders (Faded Away):
  - old_draft.txt

--- Garden is Thriving! ---
```

## Development & Testing

To run the automated tests:

```bash
npm test
```

Tests are deterministic and use an in-memory mock file system to simulate various scenarios without touching your actual file system.
