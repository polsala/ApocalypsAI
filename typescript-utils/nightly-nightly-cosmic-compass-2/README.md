# Nightly Cosmic Compass

A type-safe CLI utility that generates a daily "cosmic guidance" message, focus, and a thematic color palette based on the current date. Navigate the post-apocalyptic landscape with a touch of cosmic insight!

## Features

*   **Daily Guidance:** Get a unique focus, message, and color palette for each day.
*   **Deterministic:** The guidance for any given date is always the same, ensuring consistent cosmic wisdom.
*   **Type-Safe:** Built with TypeScript for robust and predictable behavior.
*   **CLI Interface:** Easily run from your terminal.

## Installation

1.  **Prerequisites:** Ensure you have Node.js (v14 or higher) and npm/yarn installed.
2.  **Clone the repository (or navigate to this utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-cosmic-compass
    ```
3.  **Install dependencies:**
    ```bash
    npm install
    # or yarn install
    ```
4.  **Build the utility:**
    ```bash
    npm run build
    # or yarn build
    ```

## Usage

Run the utility from the command line:

```bash
node dist/index.js [YYYY-MM-DD]
```

*   If no date is provided, it will use the current system date.
*   If a date is provided (e.g., `2024-07-21`), it will generate guidance for that specific date.

### Examples

**Get today's guidance:**
```bash
node dist/index.js
```

**Get guidance for a specific date:**
```bash
node dist/index.js 2024-12-25
```

## Output Example

```
🌌 Cosmic Guidance for 2024-07-21 🌌

Focus: Strategic Scavenge
Message: "Prioritize your resources. Every scrap counts in the grand scheme of survival."
Color Palette:
  - #006400 (Dark Green)
  - #228B22 (Forest Green)
  - #3CB371 (Medium Sea Green)
  - #90EE90 (Light Green)
```

## Development

To run tests:
```bash
npm test
# or yarn test
```
