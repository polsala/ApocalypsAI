# Nightly Cosmic Compass

A whimsical command-line utility that reveals the day's unique cosmic alignment and its cryptic influence, guiding your journey through the known and unknown universe. Perfect for daily inspiration, creative prompts, or just a moment of cosmic reflection.

## Features

*   **Daily Cosmic Alignment**: Get a unique, whimsical cosmic event and its associated influence for any given day.
*   **Location-Aware Flavor**: Optionally specify a location to personalize your cosmic reading.
*   **Deterministic Readings**: For a given date, the cosmic alignment will always be the same, ensuring consistent cosmic guidance.

## Installation

1.  **Ensure Node.js is installed**: This utility requires Node.js (v14 or higher). You can download it from [nodejs.org](https://nodejs.org/).
2.  **Clone the repository**: If you haven't already, clone the ApocalypsAI repository.
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-cosmic-compass
    ```
3.  **Install dependencies**: Navigate into the utility's directory and install its dependencies.
    ```bash
    npm install
    ```

## Usage

Run the utility from the command line:

```bash
node src/index.js [options]
```

### Options

*   `--date <YYYY-MM-DD>`: Specify a date for the cosmic reading (e.g., `2024-07-20`). Defaults to the current date if not provided.
*   `--location <string>`: Specify a location for a personalized touch (e.g., `"Andromeda Galaxy"`, `"My Secret Bunker"`). Defaults to `"the known universe"`.
*   `-h`, `--help`: Display the help message.

### Examples

**1. Get today's cosmic alignment:**

```bash
node src/index.js
```

**2. Get the cosmic alignment for a specific date:**

```bash
node src/index.js --date 2025-12-25
```

**3. Get the cosmic alignment for a specific location:**

```bash
node src/index.js --location "The Whispering Peaks"
```

**4. Get the cosmic alignment for a specific date and location:**

```bash
node src/index.js --date 2024-04-01 --location "Deep Space Outpost 7"
```

## Development

### Running Tests

To run the automated tests, navigate to the utility's directory and execute:

```bash
npm test
```

This will run the `compass.test.js` file using Node.js's built-in `assert` module.

### Project Structure

```
.
├── README.md
├── package.json
├── src/
│   ├── index.js    # CLI entry point
│   └── compass.js  # Core logic for cosmic alignment calculation
└── tests/
    └── compass.test.js # Unit tests for the core logic
```
