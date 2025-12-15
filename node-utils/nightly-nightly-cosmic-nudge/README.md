# Nightly Cosmic Nudge

A whimsical command-line utility designed to help you overcome decision paralysis by offering a random "cosmic nudge" from a predefined list of actions or your own custom suggestions. When the void of choices feels overwhelming, let the cosmos whisper your next step!

## Usage

### Prerequisites

Ensure you have Node.js installed on your system.

### Installation

1.  Navigate to the `node-utils/nightly-cosmic-nudge` directory.
2.  Run `npm install` to install dependencies (if any).

### Running the Nudge

#### With Default Suggestions

If you're feeling truly lost, just run the script without any arguments:

```bash
node src/index.js
```

Example Output:
```
🌌 The cosmos whispers: Organize your survival stash.
```

#### With Custom Suggestions

Provide your own list of options as command-line arguments. Each argument will be treated as a separate suggestion.

```bash
node src/index.js "Explore the ruins" "Barter with traders" "Fortify the shelter" "Rest and recuperate"
```

Example Output:
```
🌌 The cosmos whispers: Fortify the shelter.
```

## Development

### Running Tests

To ensure the cosmic nudges are truly random (or deterministically random for testing purposes!), run the tests:

```bash
npm test
# or directly:
node tests/index.test.js
```

## Contributing

Feel free to expand the cosmic wisdom or improve the celestial mechanics!
