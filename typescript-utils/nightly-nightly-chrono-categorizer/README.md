# Nightly Chrono-Categorizer

A type-safe CLI tool for the discerning survivor, the Nightly Chrono-Categorizer helps you sort your apocalyptic to-dos, scavenged treasures, or existential dread into distinct temporal urgency buckets. No more guessing what needs immediate attention versus what can wait until the next cosmic alignment!

## Features

*   **Whimsical Categorization**: Assigns tasks to "Immediate Implosion", "Near-Term Nuisance", "Future Folly", or "Cosmic Contemplation".
*   **Keyword-Driven**: Categories are determined by keywords found in your task descriptions.
*   **Type-Safe**: Built with TypeScript for robust and predictable operation.
*   **CLI Interface**: Easily categorize tasks directly from your terminal.

## Installation

1.  Ensure you have Node.js (v18 or higher) and npm/yarn installed.
2.  Navigate to the `nightly-chrono-categorizer` directory.
3.  Install dependencies:
    ```bash
    npm install
    # or
    yarn install
    ```
4.  Build the TypeScript project:
    ```bash
    npm run build
    # or
    yarn build
    ```

## Usage

Run the categorizer with a list of tasks. Each task should be a string. The tool will parse keywords within each task to assign an urgency.

```bash
node dist/cli.js "Fix the temporal rift - urgent!" "Scavenge for more sprockets (soon)" "Ponder the meaning of the void" "Repair the shelter's roof"
```

### Example Output

```
Categorized Tasks:

--- Immediate Implosion ---
- Fix the temporal rift - urgent!

--- Near-Term Nuisance ---
- Scavenge for more sprockets (soon)
- Repair the shelter's roof

--- Cosmic Contemplation ---
- Ponder the meaning of the void
```

## Development

To run tests:

```bash
npm test
# or
yarn test
```
