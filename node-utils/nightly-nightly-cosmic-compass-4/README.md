# Nightly Cosmic Compass

A whimsical command-line utility that helps you find your "cosmic direction" for inspiration or decision-making. Feeling stuck? Let the universe guide your next thought with a randomly generated direction and a cryptic cosmic whisper, all based on a simple seed.

## ✨ Features

*   **Whimsical Guidance**: Get a unique direction (North, South, East, West, etc.) and a thought-provoking message.
*   **Deterministic (with seed)**: Provide a seed (any string) to get the same cosmic guidance every time. Great for sharing or revisiting specific inspirations.
*   **Random (without seed)**: If no seed is provided, it uses the current timestamp, offering fresh guidance each time.
*   **Zero Dependencies**: Pure Node.js, no external packages needed.

## 🚀 Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-cosmic-compass
    ```
2.  **Make the script executable**:
    ```bash
    chmod +x src/index.js
    ```
3.  **(Optional) Add to your PATH**: For global access, you can symlink it:
    ```bash
    # Example for ~/.local/bin, ensure it's in your PATH
    ln -s "$(pwd)/src/index.js" ~/.local/bin/cosmic-compass
    ```
    Or, if you have `npm` installed, you can use `npm link` from the `nightly-cosmic-compass` directory:
    ```bash
    npm link
    ```
    This will make `cosmic-compass` available globally.

## 💡 Usage

Run the utility from your terminal:

```bash
# Get guidance using the current timestamp as a seed
cosmic-compass

# Get guidance using a specific seed (e.g., a project name, a question)
cosmic-compass "my-next-big-idea"

# Another example with a different seed
cosmic-compass "what-should-i-eat-for-dinner"
```

### Example Output

```
-- Nightly Cosmic Compass --
Seed used: "my-next-big-idea"
Your Cosmic Direction: [1mSouthwest[0m
Cosmic Whisper: [36mThe nebulae swirl, revealing hidden paths.[0m
----------------------------
```

## 🧪 Testing

To run the automated tests:

```bash
node tests/index.test.js
```

This will execute a series of deterministic tests to ensure the cosmic guidance is consistent for given seeds and that the internal hashing works as expected.
