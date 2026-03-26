# Nightly Chrono-Echo Terminal

A whimsical-yet-useful Node.js CLI utility that echoes your terminal input with configurable temporal distortions: character delays, random glitches, and even small segment reversals. Perfect for simulating network latency, adding dramatic flair to your scripts, or just having a bit of fun with your terminal output.

## Features

*   **Configurable Delay**: Set the time between each character's appearance.
*   **Character Glitches**: Introduce random character substitutions with a specified probability.
*   **Temporal Reversals**: Occasionally reverse small segments of your message for a truly distorted effect.
*   **Cross-Platform**: Runs anywhere Node.js is supported.

## Installation

1.  **Ensure Node.js is installed**: If you don't have Node.js, download it from [nodejs.org](https://nodejs.org/).
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-chrono-echo-terminal
    ```
3.  **Install dependencies (for testing)**:
    ```bash
    npm install
    ```
4.  **Make the script executable (optional, if running directly)**:
    ```bash
    chmod +x src/index.js
    ```
    (You can also run it directly with `node src/index.js` or, after `npm link` or global install, as `chrono-echo`)

## Usage

If you installed it globally (e.g., `npm install -g .` from the utility's directory):

```bash
chrono-echo "Your message here" [options]
```

Otherwise, run it directly:

```bash
./src/index.js "Your message here" [options]
```

Or with `node`:

```bash
node src/index.js "Your message here" [options]
```

### Options

*   `<message>`: The string you want to echo. **Required.**
*   `-d, --delay <milliseconds>`: The delay in milliseconds between each character.
    *   Default: `50`
    *   Example: `-d 100` for 100ms delay per character.
*   `-g, --glitch-probability <probability>`: The probability (a number between 0 and 1) that any given character will be replaced by a random character.
    *   Default: `0.05` (5% chance)
    *   Example: `-g 0.1` for a 10% glitch chance.
*   `-r, --reverse-probability <probability>`: The probability (a number between 0 and 1) that a small 3-character segment will be reversed.
    *   Default: `0.01` (1% chance)
    *   Example: `-r 0.05` for a 5% reversal chance.

### Examples

**Basic Echo with Default Delay:**

```bash
./src/index.js "Hello, ApocalypsAI community!"
```
*(Output will appear character by character with a 50ms delay, and a small chance of glitches/reversals)*

**Faster Echo with More Glitches:**

```bash
./src/index.js "Data stream corrupted... attempting re-sync." -d 20 -g 0.2
```
*(Faster output, 20ms delay, 20% chance of character glitches)*

**Slow Echo with High Reversal Probability:**

```bash
./src/index.js "Temporal anomaly detected. Proceed with caution." --delay 150 --reverse-probability 0.1
```
*(Very slow output, 150ms delay, 10% chance of 3-character segments reversing)*

**No Effects (just a slow echo):**

```bash
./src/index.js "Pure echo." -d 100 -g 0 -r 0
```
*(100ms delay, no glitches, no reversals)

## Development

To run tests:

```bash
npm test
```
