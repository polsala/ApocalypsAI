# Nightly Scavenged Item Classifier

The ApocalypsAI Nightly Integrator presents the "Scavenged Item Classifier," a whimsical-yet-useful utility designed to help survivors quickly assess the potential value of their latest finds in the wasteland. Simply provide a description of your scavenged item, and this tool will categorize it, assign a whimsical utility score, and offer a brief note on its potential use.

## Features

*   **Item Classification**: Automatically sorts items into categories like `Food/Water`, `Tool/Weapon`, `Resource/Material`, `Medical/Survival`, or `Junk/Curiosity`.
*   **Whimsical Utility Scoring**: Assigns a score from 1 to 10, accompanied by a fun rating (e.g., "Dust Collector", "Apocalypse Essential").
*   **Helpful Notes**: Provides a short, context-aware note for each classified item.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.

## Installation

To use this utility, you'll need Node.js (which includes npm) and TypeScript installed.

1.  Navigate to the `nightly-scavenged-item-class` directory.
2.  Install the dependencies:
    ```bash
    npm install
    ```

## Usage

You can run the classifier directly using `ts-node` or build it first and then run the compiled JavaScript.

### Direct Execution (Recommended for quick use)

```bash
npm start "a dusty can of beans"
# Or, if you prefer to call ts-node directly:
ts-node src/index.ts "a rusty crowbar"
```

Replace `"a dusty can of beans"` with the description of your scavenged item.

### Build and Run

1.  Compile the TypeScript code:
    ```bash
    npm run build
    ```
2.  Run the compiled JavaScript:
    ```bash
    node dist/index.js "a coil of copper wire"
    ```

### Example Output

```
-- Scavenged Item Report --
Description: "a half-used first aid kit"
Category: Medical/Survival
Utility Score: 9/10
Whimsical Rating: Apocalypse Essential
Notes: Crucial for health and long-term survival.
-----------------------------
```

## Development

### Running Tests

To ensure the classifier is functioning as expected, run the automated tests:

```bash
npm test
```

The tests are deterministic, mocking `Math.random()` to ensure consistent utility scores for verification.

### Project Structure

```
.
├── README.md
├── package.json
├── tsconfig.json
├── src/
│   └── index.ts        # Main classification logic and CLI entry point
└── tests/
    └── index.test.ts   # Automated tests for the classification logic
```
