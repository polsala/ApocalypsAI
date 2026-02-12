# Nightly Digital Diviner

## Overview

The `nightly-digital-diviner` is a whimsical Node.js CLI utility designed to offer cryptic, apocalypse-themed prophecies based on your system's current CPU and memory utilization. Feeling overwhelmed by digital toil? Or perhaps adrift in a sea of underutilized resources? Let the Diviner guide your next steps with a touch of post-apocalyptic wisdom.

## Features

*   **CPU Prophecies**: Receive guidance based on your system's processing load.
*   **Memory Visions**: Gain insight into your digital mind's state from memory usage.
*   **Whimsical & Useful**: A fun way to encourage breaks, optimize resource management, or simply ponder your digital existence.

## Installation

1.  **Navigate to the utility directory:**
    ```bash
    cd node-utils/nightly-digital-diviner
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```

## Usage

Run the diviner from your terminal:

```bash
node src/index.js
```

### Example Output

```
🌌 The Nightly Digital Diviner speaks! 🌌

CPU Prophecy: The computational gears turn with a steady, purposeful rhythm. The Oracle of Efficiency nods: 'Your efforts are well-paced, survivor. Maintain this balance.'
Memory Vision: Memory flows like a well-tended spring. The Oracle of Clarity smiles: 'Your digital mind is sharp and ready. Proceed with purpose.'
```

## Development & Testing

To run the automated tests:

```bash
npm test
```

Tests are deterministic and mock the `os` module to simulate various system resource states without relying on actual system performance.
