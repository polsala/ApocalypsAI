# Nightly Cosmic Choice Oracle

Feeling adrift in the sea of decisions? The Nightly Cosmic Choice Oracle is here to guide your next step with a touch of celestial wisdom! This whimsical Node.js CLI tool takes a simple input (like your current mood or a vague query) and consults the cosmos to offer a unique, inspiring, or delightfully absurd suggestion for your next action.

## Features

*   **Cosmic Guidance**: Get a unique suggestion based on your input.
*   **Decision Alleviator**: Breaks through analysis paralysis with a fun, low-stakes prompt.
*   **Whimsical & Inspiring**: Suggestions range from creative endeavors to unexpected explorations.
*   **Cross-Platform**: Runs wherever Node.js is supported.

## Installation

1.  Navigate to the `node-utils/nightly-cosmic-choice-oracle` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

Run the oracle with your query as an argument:

```bash
node src/index.js "feeling stuck"
```

Or, for a more general cosmic nudge:

```bash
node src/index.js "what next?"
```

The oracle will then reveal its cosmic wisdom:

```
✨ The Nebula's Embrace whispers: 'Draft a manifesto for a squirrel revolution.'
```

### Examples

```bash
node src/index.js "bored"
# Output: 🌬️ The Stellar Winds whispers: 'Map out the secret pathways of your local park.'

node src/index.js "need inspiration"
# Output: 🌕 The Lunar Glow whispers: 'Compose a haiku about the silence between stars.'

node src/index.js "overwhelmed"
# Output: ☄️ The Comet's Trail whispers: 'Embark on a spontaneous quest for the perfect pebble.'
```

## Development

### Running Tests

```bash
npm test
```

## License

MIT
