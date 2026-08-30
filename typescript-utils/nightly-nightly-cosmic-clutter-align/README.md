# Nightly Cosmic Clutter Aligner

## Overview

The `nightly-cosmic-clutter-aligner` is a whimsical-yet-useful command-line utility designed to help you bring order to your digital chaos. Instead of mundane priority levels, this tool assigns a "Cosmic Alignment" to your files, tasks, or even browser tabs, guiding you on what to tackle next based on pseudo-astrological principles.

Are your old files drifting into a "Void Resonance"? Is that urgent task in "Stellar Convergence"? Let the cosmos decide!

## Features

*   **Cosmic Alignment Scoring**: Assigns a score and a unique cosmic alignment (e.g., Stellar Convergence, Nebula Drift, Void Resonance) to your digital items.
*   **Whimsical Recommendations**: Provides a fun, thematic recommendation for each item.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.
*   **CLI Interface**: Easy to use from your terminal.

## Installation

1.  **Prerequisites**: Ensure you have Node.js (v14 or higher) and npm/yarn installed.
2.  **Clone the repository (or navigate to this utility's folder)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-cosmic-clutter-aligner
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    # or yarn install
    ```
4.  **Build the project**:
    ```bash
    npm run build
    # or yarn build
    ```

## Usage

Run the compiled JavaScript directly or use `ts-node` for development.

```bash
# Example with ts-node (for development/testing)
# npx ts-node src/index.ts --file "./my_old_report.docx" --file "./new_project_plan.txt" --task "Review PR #123" --task "Draft newsletter"

# Example with compiled JavaScript
node dist/index.js \
  --file "/path/to/your/ancient_logs.txt" \
  --file "/path/to/your/current_work.md" \
  --task "Respond to email backlog" \
  --task "Plan next sprint" \
  --tab "ApocalypsAI GitHub Issue" \
  --tab "Research paper on temporal mechanics"
```

### Arguments:

*   `--file <path>`: Specify a file path to analyze. The tool will attempt to read its last modified date and size.
*   `--task <description>`: Specify a task description. The tool will use its inherent 'newness' (current time) and a default 'size' for scoring.
*   `--tab <description>`: Specify a browser tab description. Similar to tasks, it uses current time and a default 'size'.

## Development

To run tests:

```bash
npm test
# or yarn test
```

## Contributing

Feel free to enhance the cosmic alignment algorithms, add new entity types, or expand the whimsical recommendations!
